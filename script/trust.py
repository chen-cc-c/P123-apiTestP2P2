import unittest,logging,requests
from random import random

from api.loginAPI import loginAPI
from bs4 import BeautifulSoup

from api.trustAPI import trustAPI
from utils import assert_utils, request_third_api


class trust(unittest.TestCase):
    def setUp(self) -> None:
        self.login_api=loginAPI()
        self.trust_api=trustAPI()
        self.session=requests.Session()

    def  tearDown(self) -> None:
        self.session.close()

    def test01_trust_request(self):
       #1.
        response = self.login_api.login(self.session)
        logging.info("login response={}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
       #2.
        response=self.trust_api.trust_regoster(self.session)
        logging.info("trust register response={}".format(response.json()))
        self.assertEqual(200,response.status_code)
        self.assertEqual(200,response.json().get("status"))
       #3.
        form_data=response.json().get("form")
        logging.info('form response={}'.format(form_data))
        #调用第三方接口
        response=request_third_api(form_data)
        self.assertEqual(200,response.status_code)
        self.assertEqual('userregister ok',response.text)
    def recharge(self):
        response = self.login_api.login(self.session)
        logging.info("login response={}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        #2.
        r=random()
        response=self.trust_api.get_recharge_verify_code(self.session,str(r))
        logging.info("get recharge verify code response={}".format(response.json()))
        self.assertEqual(200,response.status_code)

        response=self.trust_api.recharge(self.session,'10000')
        logging.info("recharge response={}".format(response.json()))
        self.assertEqual(200,response.status_code)
        self.assertEqual(200,response.json().get("status"))

        form_data=response.json().get("description").get("form")
        logging.info('={}'.format(form_data))
        response=request_third_api(form_data)
        self.assertEqual('NetSave ok',response.text)





