import logging
import random
import time
import unittest

import requests

from api.approveAPI import approveAPI
from api.loginAPI import loginAPI
from utils import assert_utils

class approve(unittest.TestCase):
    phone1="315313"
    phone2="135464564"
    realname="张三"
    cardID="43018152545254544444"

    def setUp(self) -> None:
        self.login_api=loginAPI()
        self.approve_api=approveAPI()
        self.session=requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    def test01_approve_success(self):

        response = self.login_api.login(self.session)
        logging.info("login response={}".format(response.json()))
        assert_utils(self,response,200,200,"登录成功")

        response = self.approve_api.approve(self.session,self.realname,self.cardID)
        assert_utils(self,response,200,200,"提交成功")

    def test02_approve_realname_is_null(self):
        response = self.login_api.login(self.session)
        logging.info("login response={}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")

        response = self.approve_api.approve(self.session,"", self.cardID)
        assert_utils(self, response, 100, 200, "姓名不能为空")

    def test03_approve_cardID_is_null(self):
        response = self.login_api.login(self.session)
        logging.info("login response={}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")

        response = self.approve_api.approve(self.session,self.realname, "")
        assert_utils(self, response, 100, 200, "身份证号不能为空")

    def test04_get_approve(self):
        response = self.login_api.login(self.session,self.phone1)
        logging.info("login response={}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")

        response = self.approve_api.approve(self.session)
        self.assertEqual(200,response.status_code)

    def test05_fsfsf(self):
        response = self.login_api.login(self.session)
        logging.info("login response={}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")

        response = self.approve_api.approve(self.session, self.realname, self.cardID)
        assert_utils(self, response, 200, 100, "身份证号格式不正确")

