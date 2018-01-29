from time import time

import requests
from requests.models import RequestEncodingMixin as REM


def time_dc():
    return (repr(time())[:14]).replace('.', '')


# robi ecare api
HOST = 'https://ecare-app.robi.com.bd'
LOGIN = '/airtel_sc/index.php?r=/accounts/login&_dc='
MY_PACKAGES = '/airtel_sc/index.php?r=/data-packages/my-data-packages&_dc='
PACKAGES = '/airtel_sc/index.php?r=/data-packages/get-data-packages&_dc='
BUY_PACKAGE = '/airtel_sc/index.php?r=/data-packages/activate-data-package&_dc='

session = requests.Session()
# session.verify = False
# requests.packages.urllib3.disable_warnings()

session.headers = {
    'Connection': 'keep-alive',
    'Origin': 'file://',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': '*/*',
    'x-wap-profile': 'http://218.249.47.94/Xianghe/MTK_Phone_JB_UAprofile.xml',
    'X-Requested-With': 'net.omobio.airtelsc',
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; Symphony W68 Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Accept-Encoding': 'gzip,deflate',
    'Accept-Language': 'en-US',
    'Accept-Charset': 'utf-8, utf-16, *;q=0.7'
}

data = {
    'app_type': 'mobile_app',
    'conn_type': '',
    'language': '',
    'force_loging': '0',
    'device_model': 'Symphony w68',
    'device_platform': 'Android',
    'device_uuid': 'b86e58c13a7aae35',
    'device_imsi': 'b86e58c13a7aae35',
    'device_version': '4.2.2',
    'operator': '',
    'network_type': 'mobile',
    'app_version': '4.0.1'

}

num = raw_input('number: ')
_pass = raw_input('password: ')

data.update({
    'conn': str(num),
    'password': str(_pass)
    })
resp = session.post(HOST + LOGIN + time_dc(), data=REM._encode_params(data))
del data['password'], data['force_loging']
data.update({
    'session_key': resp.json()['sessionKey'],
    'conn_type': resp.json()['connections'][0]['conn_type'],
    'operator': resp.json()['connections'][0]['operator'],
    'conn': resp.json()['connections'][0]['conn'],
    'ref_number': resp.json()['user']['mobile'],
    'lang': 'en',
    'page': '1',
    'start': '0',
    'limit': '15'
    })
resp = session.post(HOST + PACKAGES + time_dc(), data=data)
del data['page'], data['start'], data['limit']

for index, item in enumerate(resp.json()['data']):
    print index, ':', item.get('plan_id'), item.get('tariff_with_vat')

select = input('select pack no: ')
data.update({
      'plan_id': resp.json()['data'][select]['plan_id'],
      'name': resp.json()['data'][select]['name']
      })
print 'be careful: check your pack, please.'
print data['plan_id']
total_num = input('buy times: ')

for _ in range(total_num):
    resp = session.post(HOST + BUY_PACKAGE + time_dc(), data=data)
    print resp.text
    data.update({'secret_code': raw_input('secrete: ')})
    resp = session.post(HOST + BUY_PACKAGE + time_dc(), data=data)
    print resp.text
    del data['secret_code']
    # input()
