import unittest
import json

from libs.ddt import ddt, data
from scripts.handle_excel import HandleExcel
from scripts.handle_yaml import do_yaml
from scripts.handle_log import do_log
from scripts.handle_parameterize import Parameterize
from scripts.handle_request import HandleRequest
from scripts.handle_mysql import HandleMysql


@ddt
class TestInvest(unittest.TestCase):
    """
    投资接口测试
    """
    excel = HandleExcel('invest')  # 创建HandleExcel对象
    cases = excel.read_data_obj()  # 获取excel中invest表单下的所有数据

    @classmethod
    def setUpClass(cls):  # 所有用例执行前, 会被调用一次
        cls.do_request = HandleRequest()  # 创建HandleRequest对象
        cls.do_request.add_headers(do_yaml.read("api", "header"))  # 添加公共的请求头
        cls.do_mysql = HandleMysql()

    @classmethod
    def tearDownClass(cls):  # 所有用例执行结束之后, 会被调用一次
        cls.do_request.close()  # 释放session会话资源
        cls.do_mysql.close()

    @data(*cases)
    def test_invest(self, case):
        # 1.参数化
        new_data = Parameterize.to_param(case.data)
        # 2.拼接完整的url
        new_url = do_yaml.read("api", "url_prefix") + case.url
        # 3.获取用例method
        method = case.method

        # 4.向服务器发起请求
        res = self.do_request.send(url=new_url,
                                   method=method,
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
            # 先断言code
            self.assertEqual(expected_result.get("code"), actual_value.get("code"), msg=msg)

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
            # 如果登录接口断言成功, 则取出token, 并添加到公共请求头中
            if 'token_info' in res.text:
                token = actual_value['data']['token_info']['token']
                token_header = {"Authorization": "Bearer " + token}
                self.do_request.add_headers(token_header)

            # 取借款人的标id：loan_id
            check_sql = case.check_sql  # 从表单取出check_sql
            if check_sql:
                check_sql = Parameterize.to_param(check_sql)  # 将check_sql参数化
                mysql_data = self.do_mysql.run(check_sql)  # 执行sql
                loan_id = mysql_data["id"]
                # 动态创建属性的机制, 来解决接口依赖的问题
                setattr(Parameterize, 'loan_id', loan_id)

            # 将响应实际值写入到actual_col列
            self.excel.write_data(row=row,
                                  column=do_yaml.read("excel", "actual_col"),
                                  value=res.text)
            # 将用例执行结果写入到result_col
            self.excel.write_data(row=row,
                                  column=do_yaml.read("excel", "result_col"),
                                  value=success_msg)
            do_log.info(f"{msg}, 执行的结果为: {success_msg}\n")
