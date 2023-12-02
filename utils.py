import json
import logging

import pymysql
import requests
from bs4 import BeautifulSoup

import app


def assert_utils(self,response,status_code,status,desc):
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertEqual(desc, response.json().get("description"))
    
def request_third_api(form_data):
    soup = BeautifulSoup(form_data, "html.parser")
    third_url = soup.form['action']
    logging.info('third_url={}'.format(third_url))
    data = []
    for input in soup.find_all('input'):
        data.setdefault(input['name'], input['value'])
    logging.info("={}".format(data))
    response = requests.post(third_url, data=data)
    return response

class DButils:
    @classmethod #类方法
    def get_conn(self, db_name):
        conn=pymysql.connect(app.DB_URL,app.DB_USERNAME,app.DB_PASSWORD,db_name,autocommit=True)
        return  conn

    @classmethod
    def close(cls,cursor,conn):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    @classmethod
    def delete(cls,db_name,sql):
        try:
            conn=cls.get_conn(db_name)
            cursor=conn.cursor()
            cursor.execute(sql)
        except Exception as e:
            conn.rollback()
        finally:
            cls.close(conn,cursor)
def read_imgVerify_data(file_name):
    file=app.BASE_DIR+"/data/"+file_name
    test_case_data=[]
    with open(file,encoding="utf-8") as f:
        verify_data=json.load(f)
        test_data_list=verify_data.get("test_get_img_verify_code")
        for test_data in test_data_list:
            test_case_data.append((test_data.get("type"),test_data.get("status_code")))
    print("json data={}".format(test_case_data))
    return test_case_data

def read_register_data(file_name):
    file=app.BASE_DIR+"/data/"+file_name
    test_case_data=[]
    with open(file,encoding="utf-8") as f:
        register_data = json.load(f)
        test_data_list = register_data.get("test_register")
        for test_data in test_data_list:
            test_case_data.append((test_data.get("phone"), test_data.get("pwd"),test_data.get("imgVerifyCode"),
                                   test_data.get("phoneCode"),test_data.get("dyServer"),test_data.get("invite_phone"),
                                   test_data.get("status_code"),test_data.get("status"),test_data.get("description")))
        print("test_case_data={}".format(test_case_data))
    return test_case_data

def read_param_data(file_name,method_name,params_name):
    #filename: 参数数据文件的文件名
    #method_name:参数数据文件中定义的测试数据列表的名称，如：test_get_img_verify_code、test_register
    #params:参数数据文件一组测试数据中所有的参数组成的字符串，如：“type,status_code”
    file = app.BASE_DIR + "/data/" + file_name
    test_case_data = []
    with open(file, encoding="utf-8") as f:
        #将json字符串转换为字典格式
        file_data = json.load(f)
        test_data_list=file_data.get(method_name)
        for test_data in test_data_list:
            test_params=[]
            for param in params_name.split(","):
                test_params.append(test_data.get(param))
            test_case_data.append(test_params)
    print("={}".format(test_case_data))
    return  test_case_data




