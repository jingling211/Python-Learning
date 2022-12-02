import requests
from urllib.parse import urljoin

BASE_URL = 'https://www.xx.com/'
LOGIN_URL = urljoin(BASE_URL, '/new/admin.php?act=login')
INDEX_URL = urljoin(BASE_URL, '/new/admin.php?ctl=network')
USERNAME = 'admin'
PASSWORD = 'xx'

# initial session obj
session = requests.Session()

# login site with user account
response_login = session.post(LOGIN_URL, data={
    'u': USERNAME,
    'p': PASSWORD
}, verify='C:\\Users\\z0064529\\Desktop\\ca\\zf_chain_ca.crt')

print(response_login.url)

# user credential has been saved in session obj
cookies = session.cookies
print('Cookies', cookies)

# use existed session obj to access other site page which is need user credential
response_index = session.get(INDEX_URL, verify='C:\\Users\\z0064529\\Desktop\\ca\\zf_chain_ca.crt')
print('Response Status', response_index.status_code)
print('Response URL', response_index.url)
print(session.headers)
print(session.cookies)
print(response_index.text)

# we can export the site CA file from browser, please select "BASE64 encoded ASCII, certificated chain(.crt, .pem)"
# C:\\Users\\z0064529\\Desktop\\ca\\zf_chain_ca.crt
