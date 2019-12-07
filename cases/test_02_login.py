import unittest
import json

from libs.ddt import ddt, data
from scripts.handle_excel import HandleExcel
from scripts.handle_yaml import do_yaml
from scripts.handle_log import do_log
from scripts.handle_parameterize import Parameterize
from scripts.handle_request import HandleRequest


@ddt
class TestLogin(unittest.TestCase):
    """
    登录接口测试
    """
    excel = HandleExcel('login')  # 创建HandleExcel对象
    cases = excel.read_data_obj()  # 获取excel中login表单下的所有数据

    @classmethod
    def setUpClass(cls):  # 所有用例执行前, 会被调用一次
        cls.do_request = HandleRequest()  # 创建HandleRequest对象
        cls.do_request.add_headers(do_yaml.read("api", "header"))  # 添加公共的请求头

    @classmethod
    def tearDownClass(cls):  # 所有用例执行结束之后, 会被调用一次
        cls.do_request.close()  # 释放session会话资源

    @data(*cases)
    def test_login(self, case):
        # 1.参数化
        new_data = Parameterize.to_param(case.data)
        # 2.拼接完整的url
        new_url = do_yaml.read("api", "url_prefix") + case.url
        # 3.向服务器发起请求
        res = self.do_request.send(url=new_url,
                                   data=new_data
                                   )
        # 将响应报文中的数据转换为字典
        actual_value = res.json()
        # 获取用例的行号
        row = case.case_id + 1
        # 获取预期结果，转化为字典
        expected_result = json.loads(case.expected, encoding='utf-8')

        msg = case.title  # 获取标题
        success_msg = do_yaml.read('msg', 'success_result')  # 获取用例执行成功的提示
        fail_msg = do_yaml.read('msg', 'fail_result')  # 获取用例执行失败的提示

        try:
            # 先断言code，再断言msg
            self.assertEqual(expected_result['code'], actual_value['code'], msg=msg)
            self.assertEqual(expected_result['msg'], actual_value['msg'], msg=msg)
        except AssertionError as e:
            # 将响应实际值写入到actual_col列
            self.excel.write_data(row=row,
                                  column=do_yaml.read("excel", "actual_col"),
                                  value=res.text)
            # 将用例执行结果写入到result_col
            self.excel.write_data(row=row,
                                  column=do_yaml.read("excel", "result_col"),
                                  value=fail_msg)
            do_log.error(f"{msg}, 执行的结果为: {fail_msg}\n具体异常为: {e}\n")
            raise e
        else:
            # 将响应实际值写入到actual_col列
            self.excel.write_data(row=row,
                                  column=do_yaml.read("excel", "actual_col"),
                                  value=res.text)
            # 将用例执行结果写入到result_col
            self.excel.write_data(row=row,
                                  column=do_yaml.read("excel", "result_col"),
                                  value=success_msg)

            do_log.info(f"{msg}, 执行的结果为: {success_msg}\n")
