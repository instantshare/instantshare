import threading
import webbrowser
from http.server import CGIHTTPRequestHandler, HTTPServer


class OAuthRequestHandler(CGIHTTPRequestHandler):

    def do_GET(self):
        p = str(self.path)
        if p == "/":
            # write out js which filters the hash part of the url and redirects to /auth
            self.write_out("res/redirect.html")
        elif p.startswith("/auth?"):
            # parse return parameters
            pstrings = p[6:].split("&")
            pdict = {}
            for pstring in pstrings:
                param = pstring.split("=")
                pdict[param[0]] = param[1]

            self.server._access_token = pdict

            # write out success page
            self.write_out("res/completed.html")
            # kill the server from a seperate thread
            killer = threading.Thread(target=self.server.shutdown)
            killer.daemon = True
            killer.start()

    def write_out(self, filepath):
        """
        Writes the given file out to the client.
        :param filepath: path to file
        """
        with open(filepath, "rb") as file:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(file.read())


class OAuthServer(HTTPServer):

    def __init__(self):
        # try to open http server on a free port
        ports = range(4795, 4800)
        for port in ports:
            try:
                super().__init__(("", port), OAuthRequestHandler)
            except OSError:
                # Address already in use, try next
                continue
            else:
                break
        self._access_token = None

    def wait_for_redirect(self):
        """
        Waits until the client is sent to localhost to complete the implicit flow.
        :return: (access_token, token_type, expires_in)
        """
        self.serve_forever()
        return self._access_token


def implicit_flow(base_url, client_id, state=None, scope: list = None):
    """
    Executes the OAuth2 implicit grant flow for the given base url and client id.
    :param base_url: The base URL of OAuth provider
    :param client_id: The client identifier for OAuth provider
    :param state: OPTIONAL An opaque value used by the client to maintain state between the request and callback. The
    authorization server includes this value when redirecting the user-agent back to the client.
    :param scope: OPTIONAL The scope of the access request
    :return:
    """

    # Start local OAuthServer to pass redirect to
    oauth_server = OAuthServer()
    redirect_uri = "http://localhost:{}/".format(oauth_server.server_port)

    # Create URL
    url = "{0}?response_type=token&client_id={1}&redirect_uri={2}".format(base_url, client_id, redirect_uri)

    # Add optional GET parameters to URL based on given optional function parameters
    # scope
    if scope is not None:
        url += str("&scope={0}".format("%20".join(scope)))
    # state
    if state is not None:
        url += str("&state={0}".format(state))

    webbrowser.open(url)
    return oauth_server.wait_for_redirect()
