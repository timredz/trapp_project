import os
import requests as re
from io import StringIO
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

full_path = Path(os.getenv('util_path'))
file_with_cookies = full_path / "iss_cookie.txt"

f = open(file_with_cookies, "r")
iss_cookie = f.read()

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}
cookies = {'MicexPassportCert': iss_cookie}

def get_df(url):
    req = re.get(url, headers=headers, cookies = cookies)
    return StringIO(req.text)
