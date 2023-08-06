from dli.client.dli_client import DliClient


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
    return DliClient(api_key, root_url, host, debug=debug)
