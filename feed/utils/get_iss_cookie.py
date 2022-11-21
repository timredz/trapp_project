import os
import requests as re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

iss_auth_url = os.getenv('iss_auth_path')
iss_login = os.getenv('iss_login')
iss_pass = os.getenv('iss_pass')

full_path = Path(os.getenv('util_path'))
file_with_cookies = full_path / "iss_cookie.txt"

s = re.Session()

s.get(iss_auth_url, auth=(iss_login, iss_pass))

with open(file_with_cookies, "w") as f:
    f.write(s.cookies['MicexPassportCert'])
