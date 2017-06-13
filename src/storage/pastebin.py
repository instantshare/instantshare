from urllib import request, parse

from tools.config import config, general

_name = "pastebin"


def upload(file: str) -> str:
    data = {
        "api_dev_key": config[_name]["app_key"],
        "api_option": "paste",
        "api_paste_code": open(file, "r").read()
    }
    post_data = parse.urlencode(data).encode("ascii")
    response = request.urlopen("https://pastebin.com/api/api_post.php", post_data)
    public_url = str(response.read(), encoding="ascii")
    return public_url
