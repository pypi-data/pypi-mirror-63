import click
import multiprocessing
from multiprocessing.dummy import Pool
import os
import requests
import sys
import timeit

from bonsai_ai import Config
from bonsai_ai.logger import Logger
from bonsai_cli import __version__
from bonsai_cli.api import BonsaiAPI, BrainServerError
from bonsai_cli.dotbrains import DotBrains
from bonsai_cli.projfile import ProjectFile
from click._compat import get_text_stderr
from configparser import NoSectionError
from json import decoder

log = Logger()


def api(use_aad):
    """
    Convenience function for creating and returning an API object.
    :return: An API object.
    """
    bonsai_config = Config(argv=sys.argv[0],
                           use_aad=use_aad)
    verify_required_configuration(bonsai_config)

    # Several commands call this function before instantiating a new Config
    # object. Write the cache now to avoid requiring a second login later.
    bonsai_config.write_aad_cache()

    return BonsaiAPI(access_key=bonsai_config.accesskey,
                     user_name=bonsai_config.username,
                     api_url=bonsai_config.url,
                     ws_url=bonsai_config._websocket_url(),
                     )


def brain_fallback(brain, project):
    """
    Implements the fallback options for brain name.
    If a brain is given directly, use it.
    If a project is specified, check that for a brain.
    If neither is given, use .brains locally.
    """
    if brain:
        return brain
    if project:
        pf = ProjectFile.from_file_or_dir(project)
        db = DotBrains(pf.directory())
        b = db.get_default()
        if b:
            return b.name
        else:
            raise click.ClickException(
                "No Brains found with the given project")
    return get_default_brain()


def click_echo(text, fg=None, bg=None):
    """
     Wraps click.echo to print in color if color is enabled in config
     Currently only supports color printing. Update this function if you
     wish to add blinking, underline, reverse, and etc...

     param fg: foreground color,
     param bg: background color
    """
    try:
        config = Config(argv=sys.argv[0], use_aad=False)
        color = config.use_color
    except ValueError:
        color = False

    if color:
        click.secho(text, fg=fg, bg=bg)
    else:
        click.echo(text)


def check_dbrains(project=None):
    """ Utility function to check if the dbrains file has been
        modified. A valid dbrains file is in proper json format
    """
    try:
        if project:
            pf = ProjectFile.from_file_or_dir(project)
            db = DotBrains(pf.directory())
        else:
            db = DotBrains()
    except ValueError as err:
        if project:
            file_location = DotBrains.find_file(os.path.dirname(project))
        else:
            file_location = DotBrains.find_file(os.getcwd())
        msg = "Bonsai Command Failed." \
              "\nFailed to load .brains file '{}'".format(file_location)
        raise_as_click_exception(msg, err)


class CliVersionCheckerInterface(object):
    """
    Checks the latest CLI version.

    This interface is purposefully not a context manager - it's annoying and
    unnecessary to spam version upgrades when commands are failing to run.
    """

    def check_cli_version(self, wait=False, print_up_to_date=True):
        raise NotImplementedError('check_cli_version not implemented')


class AsyncCliVersionChecker(CliVersionCheckerInterface):
    """
    Checks the latest CLI version, asynchronously.
    """

    # When asked to produce a version check at the end of a command, we are
    # willing to let the command wait up to this amount of time total before
    # abandoning the version check.
    #
    # This is a balance between timely version notifications, and adding more
    # latency to our own commands if PyPi is slow or unavailable.
    #
    # TODO: PyPi does not have have a latency SLA. Perform a long-running
    # measurement experiment and back this up with actual percentiles.
    _GIVE_UP_TIME_SECONDS = 0.5

    def __init__(self):
        """
        Construct the checker.

        Kicks off a background task to determine the latest CLI version.
        """
        # Counter-intuitively a dummy multiprocessing Pool is actually
        # a thread pool, not a process pool. This is the fastest way of
        # spawning a worker thread, that works in both Python 2 and 3.
        #
        # This will never be closed - the threads are daemonic.
        self._pool = Pool(1)
        self._result = self._pool.apply_async(self._query_version)

    def check_cli_version(self, wait, print_up_to_date=True):
        """
        Compares local cli version with the one on PyPi.

        If latest version is not yet known and wait is False, this function
        blocks for a brief period of time to allow it to complete. If wait is
        instead True, this function blocks indefinitely for a response.
        """
        pypi_version, err = self._get_version_result(wait)

        # If we lack a latest version, only continue to print what we do know
        # when waitiing was a requirement. When it wasn't, this appears as
        # unexpected error output spam for an otherwise-innocent command.
        if pypi_version is None and not wait:
            return

        user_cli_version = __version__

        if not pypi_version:
            click_echo('You are using bonsai-cli version ' + user_cli_version,
                       fg='yellow')
            click_echo(
                'Unable to connect to PyPi and determine if CLI is up to date.',
                fg='red')
            if isinstance(err, requests.exceptions.SSLError):
                click_echo(
                    'The following SSL error occured while attempting to obtain'
                    ' the version information from PyPi. \n\n{}\n\n'.format(err) +
                    'SSL errors are usually a result of an out of date version of'
                    ' OpenSSL and/or certificates that may need to be updated.'
                    ' We recommend updating your python install to a more'
                    ' recent version. If this is not possible, \'pip install'
                    ' requests[security]\' may fix the problem.',
                    fg='red')
            elif err:
                click_echo(
                    'The following error occured while attempting to obtain the'
                    ' version information from PyPi.\n\n{}\n'.format(err),
                    fg='red')
        elif user_cli_version != pypi_version:
            click_echo('You are using bonsai-cli version ' + user_cli_version,
                       fg='yellow')
            click_echo('Bonsai update available. The most recent version is ' +
                       pypi_version + '.', fg='yellow')
            click_echo(
                'Upgrade via pip using \'pip install --upgrade bonsai-cli\'',
                fg='yellow')
        elif print_up_to_date:
            click_echo('You are using bonsai-cli version ' + user_cli_version +
                       ', Everything is up to date.', fg='green')

    def _query_version(self):
        log.debug('Checking latest CLI version...')
        start_time = timeit.default_timer()

        pypi_url = 'https://pypi.org/pypi/bonsai-cli/json'
        pypi_version = get_pypi_version(pypi_url)

        end_time = timeit.default_timer()
        elapsed = end_time - start_time
        log.debug('Checked latest CLI version in {} seconds.'.format(elapsed))

        return pypi_version

    def _get_version_result(self, wait):
        if wait:
            timeout = None
        else:
            timeout = self._GIVE_UP_TIME_SECONDS

        pypi_version = None
        err = None
        try:
            pypi_version = self._result.get(timeout)
        except multiprocessing.TimeoutError:
            log.debug('CLI version check has not completed')
        except requests.exceptions.SSLError as e:
            err = e
        except requests.exceptions.RequestException as e:
            err = e
        except (decoder.JSONDecodeError, KeyError) as e:
            err = e

        return pypi_version, err


class NullCliVersionChecker(CliVersionCheckerInterface):
    """
    Performs no CLI version checking, does nothing.
    """

    def check_cli_version(self, wait=False, print_up_to_date=True):
        pass


class CustomClickException(click.ClickException):
    """ Custom click exception that prints exceptions in color """
    def __init__(self, message, color):
        click.ClickException.__init__(self, message)
        self.color = color

    def show(self, file=None):
        """ Override ClickException function show() to print in color """
        if file is None:
            file = get_text_stderr()

        if self.color:
            click.secho(
                'ERROR: %s' % self.format_message(), file=file, fg='red')
        else:
            click.echo('ERROR: %s' % self.format_message(), file=file)


def get_pypi_version(pypi_url):
    """
    This function attempts to get the package information
    from PyPi. It returns None if the request is bad, json
    is not decoded, or we have a KeyError in json dict

    param pypi_url: Url of pypi package
    """
    pkg_request = requests.get(pypi_url)
    pkg_json = pkg_request.json()
    pypi_version = pkg_json['info']['version']
    return pypi_version


def get_default_brain():
    """
    Look up the currently selected brain.
    :return: The default brain from the .brains file
    """
    dotbrains = DotBrains()
    brain = dotbrains.get_default()
    if brain is None:
        raise click.ClickException(
            "Missing brain name. Specify a name with `--brain NAME`.")
    return brain.name


def list_profiles(config):
    """
      Lists available profiles from configuration

      param config: Bonsai_ai.Config
    """
    profile = config.profile
    click.echo(
        "\nBonsai configuration file(s) found at {}".format(
            config.file_paths))
    click.echo("\nAvailable Profiles:")
    if profile:
        if profile == "DEFAULT":
            click.echo("  DEFAULT" + " (active)")
        else:
            click.echo("  DEFAULT")

        # Grab Profiles from bonsai config and list each one
        sections = config._section_list()
        for section in sections:
            if section == profile:
                click.echo("  " + section + " (active)")
            else:
                click.echo("  " + section)
    else:
        click.echo("No profiles found please run 'bonsai configure'.")


def print_profile_information(config):
    """ Print current active profile information """
    try:
        profile_info = config._section_items(config.profile)
    except NoSectionError as e:
        profile_info = config._defaults().items()

    click.echo(
        "\nBonsai configuration file(s) found at {}".format(
            config.file_paths))
    click.echo("\nProfile Information")
    click.echo("--------------------")
    if profile_info:
        for key, val in profile_info:
            click.echo(key + ": " + str(val))
    else:
        click.echo("No profiles found please run 'bonsai configure'.")


def raise_as_click_exception(*args):
    """This function raises a ClickException with a message that contains
    the specified message and the details of the specified exception.
    This is useful for all of our commands to raise errors to the
    user in a consistent way.

    This function expects to be handed a BrainServerError, an Exception (or
    one of its subclasses), or a message string followed by an Exception.
    """
    try:
        config = Config(argv=sys.argv[0], use_aad=False)
        color = config.use_color
    except ValueError:
        color = False

    if args and len(args) == 1:
        if isinstance(args[0], BrainServerError):
            raise CustomClickException(str(args[0]), color=color)
        else:
            raise CustomClickException('An error occurred\n'
                                       'Details: {}'.format(str(args[0])),
                                       color=color)
    elif args and len(args) > 1:
        raise CustomClickException("{}\nDetails: {}".format(args[0], args[1]),
                                   color=color)
    else:
        raise CustomClickException("An error occurred", color=color)


def verify_required_configuration(bonsai_config):
    """This function verifies that the user's configuration contains
    the information required for interacting with the Bonsai BRAIN api.
    If required configuration is missing, an appropriate error is
    raised as a ClickException.
    """
    messages = []
    missing_config = False

    if (not bonsai_config.use_aad and not bonsai_config.accesskey):
        messages.append("Your access key is not configured.")
        missing_config = True

    if not bonsai_config._aad_client and not bonsai_config.username:
        messages.append("Your username is not confgured.")
        missing_config = True

    if missing_config:
        messages.append(
            "Run 'bonsai configure' to update required configuration.")
        raise click.ClickException("\n".join(messages))
