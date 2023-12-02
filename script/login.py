import logging
import random
import time
import unittest

import requests

from api.loginAPI import loginAPI
from utils import assert_utils

class login(unittest.TestCase):
    phone1='13077447777'
    phone2 = '13077447777'
    phone3 = '13077447777'
    phone4 = '13077447777'
    pwd='test123'
    imgCoge='8888'
    smsCode='8888'

    def setUp(self) -> None:
        self.login_api=loginAPI()
        self.session=requests.Session()



    def tearDown(self) -> None:
        self.session.close()

    def  test01_get_img_code_random_float(self):
         r=random.random()

         response=self.login_api.getImgCode(self.session,str(r))
         self.assertEqual(200,response.status_code)

    def  test02_get_img_code_random_int(self):
         r = random.random()/10000
         response = self.login_api.getImgCode(self.session, str(r))
         self.assertEqual(200, response.status_code)

    def  test03_get_img_code_random_null(self):

         response = self.login_api.getImgCode(self.session,"")
         self.assertEqual(404, response.status_code)

    def test04_get_img_code_random_char(self):
        r = random.sample("abcdefgikjloyueiorqrwetrt",8)
        rand=''.join(r)
        logging.info(rand)
        response = self.login_api.getImgCode(self.session, rand)
        self.assertEqual(400, response.status_code)

    def test05_get_sms_code_susscee(self):
        #获取图片验证码
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        #
        response = self.login_api.getSmsCode(self.session, self.phone1,self.imgCoge)
        logging.info("get sms code response={}".format(response.json()))
        assert_utils(self, response, 200, 200, "短信发送成功")

    def test06_get_sms_code_wrong_img_code(self):
        # 获取图片验证码
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        #
        response = self.login_api.getSmsCode(self.session, self.phone1, '8889')
        assert_utils(self,response,200,100,"图片验证码错误")

    def test07_get_sms_code_img_code_is_null(self):
        # 获取图片验证码
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        #
        response = self.login_api.getSmsCode(self.session,'', self.imgCoge)
        assert_utils(self, response, 200, 100, "手机号不能为空")

    def test08_get_sms_code_phone_is_null(self):
        # 获取图片验证码
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        #
        response = self.login_api.getSmsCode(self.session, self.phone1, '')
        assert_utils(self, response, 200, 100, "图片验证码错误")

 # 获取短信验证码失败——未调用获取图片验证码错接口
    def test09_get_sms_code_no_img_Verify(self):
        #1、未获取图片验证码
        #2、获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session,self.phone1,self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        #对收到的响应结果，进行断言
        assert_utils(self,response,200,100,"图片验证码错误")

    #输入必填项，注册成功
    def test10_register_success_param_must(self):
        #1、成功获取图片验证码
        r = random.random()
        #调用接口类中的接口
        response = self.login_api.getImgCode(self.session,str(r))
        #接收接口的返回结果，进行断言
        self.assertEqual(200,response.status_code)
        #2、成功获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session,self.phone1,self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        #对收到的响应结果，进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        #3、成功注册——输入必填项
        # 调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session,self.phone1,self.pwd)
        logging.info("register response = {}".format(response.json()))
        #对结果进行断言
        assert_utils(self,response,200,200,"注册成功")

    #输入所有项，注册成功
    def test11_register_success_param_all(self):
        #1、成功获取图片验证码
        r = random.random()
        #调用接口类中的接口
        response = self.login_api.getImgCode(self.session,str(r))
        #接收接口的返回结果，进行断言
        self.assertEqual(200,response.status_code)
        #2、成功获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session,self.phone2,self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        #对收到的响应结果，进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        #3、发送注册请求
        response = self.login_api.register(self.session,self.phone2,self.pwd,invite_phone='13012345678')
        logging.info("register response = {}".format(response.json()))
        #对结果进行断言
        assert_utils(self,response,200,200,"注册成功")

    #手机号已存在时，注册失败
    def test12_register_phone_is_exist(self):
        #1、成功获取图片验证码
        r = random.random()
        #调用接口类中的接口
        response = self.login_api.getImgCode(self.session,str(r))
        #接收接口的返回结果，进行断言
        self.assertEqual(200,response.status_code)
        #2、成功获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session,self.phone1,self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        #对收到的响应结果，进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        #3、注册失败——手机号以重复
        # 调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session,self.phone1,self.pwd)
        logging.info("register response = {}".format(response.json()))
        #对结果进行断言
        assert_utils(self,response,200,100,"手机已存在!")

    #注册失败——密码为空
    def test13_register_password_is_null(self):
        #1、成功获取图片验证码
        r = random.random()
        #调用接口类中的接口
        response = self.login_api.getImgCode(self.session,str(r))
        #接收接口的返回结果，进行断言
        self.assertEqual(200,response.status_code)
        #2、成功获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session,self.phone3,self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        #对收到的响应结果，进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        #3、注册失败——手机号以重复
        # 调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session,self.phone3,"")
        logging.info("register response = {}".format(response.json()))
        #对结果进行断言
        assert_utils(self,response,200,100,"密码不能为空")

    #注册失败——图片验证码错误
    def test14_register_img_code_is_wrong(self):
        #1、成功获取图片验证码
        r = random.random()
        #调用接口类中的接口
        response = self.login_api.getImgCode(self.session,str(r))
        #接收接口的返回结果，进行断言
        self.assertEqual(200,response.status_code)
        #2、成功获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session,self.phone4,self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        #对收到的响应结果，进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        #3、注册失败——图片验证码错误
        # 调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session,self.phone4,self.pwd,'1234')
        logging.info("register response = {}".format(response.json()))
        #对结果进行断言
        assert_utils(self,response,200,100,"验证码错误!")

    #注册失败——短信验证码错误
    def test15_register_sms_code_is_wrong(self):
        #1、成功获取图片验证码
        r = random.random()
        #调用接口类中的接口
        response = self.login_api.getImgCode(self.session,str(r))
        #接收接口的返回结果，进行断言
        self.assertEqual(200,response.status_code)
        #2、成功获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session,self.phone4,self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        #对收到的响应结果，进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        #3、注册失败——短信验证码错误
        # 调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session,self.phone4,self.pwd,self.imgCode,'123456')
        logging.info("register response = {}".format(response.json()))
        #对结果进行断言
        assert_utils(self,response,200,100,"验证码错误")

    #注册失败——不同注册协议
    def test16_register_no_agree_protocol(self):
        #1、成功获取图片验证码
        r = random.random()
        #调用接口类中的接口
        response = self.login_api.getImgCode(self.session,str(r))
        #接收接口的返回结果，进行断言
        self.assertEqual(200,response.status_code)
        #2、成功获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session,self.phone4,self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        #对收到的响应结果，进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        #3、注册失败——不同意注册协议
        # 调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session,self.phone4,self.pwd,dyServer='off')
        logging.info("register response = {}".format(response.json()))
        #对结果进行断言
        assert_utils(self,response,200,100,"请同意我们的条款")

    #登录成功
    def test17_login_success(self):
        #准备参数
        #调用接口类中的发送登录的接口
        response = self.login_api.login(self.session,self.phone1,self.pwd)
        #对结果进行断言
        assert_utils(self,response,200,200,"登录成功")

    #登录失败——用户名不存在
    def test18_login_phone_not_exist(self):
        #准备参数
        Wphone = '13000000000'
        #调用接口类中的发送登录的接口
        response = self.login_api.login(self.session,Wphone,self.pwd)
        logging.info("login response = {}".format(response.json()))
        #对结果进行断言
        assert_utils(self,response,200,100,"用户不存在")

    #登录失败——密码为空
    def test19_login_pwd_is_null(self):
        #调用接口类中的发送登录的接口
        response = self.login_api.login(self.session,self.phone1,"")
        logging.info("login response = {}".format(response.json()))
        #对结果进行断言
        assert_utils(self,response,200,100,"密码不能为空")

    #登录失败——密码错误
    def test20_login_wrong_pwd(self):
        wrong_pwd = 'error'
        #1、输入错误密码，提示错误一次
        response = self.login_api.login(self.session,self.phone1,wrong_pwd)
        logging.info("login response = {}".format(response.json()))
        #对结果进行断言
        assert_utils(self,response,200,100,"密码错误1次,达到3次将锁定账户")
        # 2、输入错误密码，提示错误两次次
        response = self.login_api.login(self.session,self.phone1,wrong_pwd)
        logging.info("login response = {}".format(response.json()))
        #对结果进行断言
        assert_utils(self,response,200,100,"密码错误2次,达到3次将锁定账户")
        # 3、输入错误密码，提示错误三次被锁定
        response = self.login_api.login(self.session,self.phone1,wrong_pwd)
        logging.info("login response = {}".format(response.json()))
        #对结果进行断言
        assert_utils(self,response,200,100,"由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        #4、 输入正确密码，提示被锁定
        response = self.login_api.login(self.session,self.phone1,self.pwd)
        logging.info("login response = {}".format(response.json()))
        #对结果进行断言
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        #5、等待60s，再输入正确密码，提示登录成功
        time.sleep(60)
        response = self.login_api.login(self.session,self.phone1,self.pwd)
        logging.info("login response = {}".format(response.json()))
        #对结果进行断言
        assert_utils(self,response,200,200,"登录成功")






