from http.server import CGIHTTPRequestHandler, HTTPServer
import threading
import webbrowser


class OAuthRequestHandler(CGIHTTPRequestHandler):

    def do_GET(self):
        p = str(self.path)
        if p == "/":
            # write out js which filters the hash part of the url and redirects to /auth
            self.write_out("../res/redirect.html")
        elif p.startswith("/auth?"):
            # parse parameters
            pstrings = p[6:].split("&")
            pdict = {}
            for pstring in pstrings:
                param = pstring.split("=")
                pdict[param[0]] = param[1]
            self.server._access_token = (
                pdict["access_token"],
                pdict["token_type"],
                pdict["expires_in"]
            )
            # write out success page
            self.write_out("../res/completed.html")
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
            except:
                continue
            else:
                break
        self._access_token = None  # (access_token, token_type, expires_in)

    def wait_for_redirect(self):
        """
        Waits until the client is sent to localhost to complete the implicit flow.
        :return: (access_token, token_type, expires_in)
        """
        self.serve_forever()
        return self._access_token


def implicit_flow(base_url, client_id, scopes: list):
    """
    Executes the OAuth2 implicit flow for the given base url and client id.
    :param base_url:
    :param client_id:
    :return: (access_token, token_type, expires_in)
    """
    s = OAuthServer()
    callback_url = "http://localhost:{}/".format(s.server_port)

    url = "{0}?response_type=token&client_id={1}&redirect_uri={2}&scope={3}".format(
        base_url, client_id, callback_url, "%20".join(scopes)
    )
    webbrowser.open(url)
    return s.wait_for_redirect()

""" Test:
print(implicit_flow(
    "https://accounts.google.com/o/oauth2/auth",
    "774886165931-ks0ntcb32p1mhi0nnv8tcmob81e0oetj.apps.googleusercontent.com",
    ["https://www.googleapis.com/auth/drive"]
))
"""