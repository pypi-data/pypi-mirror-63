import warnings

from dli.client.dli_client import DliClient
from dli import __version__
from distutils.version import StrictVersion
import requests
import json

DEPRECATED_AGE = 1

def version_check(package_name):
    url = "https://pypi.python.org/pypi/%s/json" % (package_name,)
    data = requests.get(url).json()
    versions = list(data["releases"].keys())
    versions.reverse()

    try:
        offset = versions.index(__version__)
        if offset > DEPRECATED_AGE:
            warnings.warn("You are using an old version of the SDK, please upgrade"
                          "using `pip install [dli] --upgrade` "
                          "before the SDK no longer functions as expected",
                          PendingDeprecationWarning)
    except ValueError:
        pass

def start_session(
    api_key,
    root_url="https://catalogue.datalake.ihsmarkit.com/__api",
    host=None,
    debug=False
):
    """
    Entry point for the Data Lake SDK, returns a client instance that
    can be used to consume or register datasets.

    Example for starting a session:

        from dli.client import session
        dl = session.start_session(api_key)

    :param str api_key: Your API key, can be retrieved from your dashboard in
                        the Catalogue UI.
    :param str root_url: Optional. The environment you want to point to. By default it
                        points to Production.
    :param str host: Optional. Advanced usage, meant to force a hostname when DNS resolution
                     is not reacheable from the user's network.
                     This is meant to be used in conjunction with an
                     IP address as the root url.
                     Example: catalogue.datalake.ihsmarkit.com

    :param bool debug: Optional. Log SDK operations to a file in the current working
                       directory with the format "sdk-{end of api key}-{timestamp}.log"

    :returns: Data Lake interface client
    :rtype: dli.client.dli_client.DliClient

    """

    version_check('dli')
    return DliClient(api_key, root_url, host, debug=debug)
