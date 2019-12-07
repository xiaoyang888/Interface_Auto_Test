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
class TestRecharge(unittest.TestCase):
    """
    充值接口测试
    """
    excel = HandleExcel('recharge')  # 创建HandleExcel对象
    cases = excel.read_data_obj()  # 获取excel中recharge表单下的所有数据

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
    def test_recharge(self, case):
        # 1.参数化
        new_data = Parameterize.to_param(case.data)
        # 2.拼接完整的url
        new_url = do_yaml.read("api", "url_prefix") + case.url

        # 获取check_sql
        check_sql = case.check_sql
        if check_sql:  # 如果check_sql不为空, 则代表当前用例需要进行数据校验
            check_sql = Parameterize.to_param(check_sql)  # 将check_sql进行参数化
            mysql_data = self.do_mysql.run(check_sql)  # 执行sql
            amount_before = float(mysql_data['leave_amount'])  # 查询结果为decimal类型，需要转换为float
            amount_before = round(amount_before, 2)  # 使用round保留2位小数

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
            # 先断言code
            self.assertEqual(expected_result['code'], actual_value['code'], msg=msg)
            # 如果code断言成功, 且check_sql不为空, 则获取充值之后的金额
            if check_sql:
                mysql_data = self.do_mysql.run(check_sql)  # 执行sql
                amount_after = float(mysql_data['leave_amount'])  # 查询结果为decimal类型，需要转换为float
                amount_after = round(amount_after, 2)  # 使用round保留2位小数

                one_dict = json.loads(new_data, encoding='utf-8')
                currrent_recharge_amount = one_dict['amount']
                actual_amount = round(amount_before + currrent_recharge_amount, 2)
                self.assertEqual(actual_amount, amount_after, msg="数据库中充值的金额有误")

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
            # 将响应实际值写入到actual_col列
            self.excel.write_data(row=row,
                                  column=do_yaml.read("excel", "actual_col"),
                                  value=res.text)
            # 将用例执行结果写入到result_col
            self.excel.write_data(row=row,
                                  column=do_yaml.read("excel", "result_col"),
                                  value=success_msg)
            do_log.info(f"{msg}, 执行的结果为: {success_msg}\n")
