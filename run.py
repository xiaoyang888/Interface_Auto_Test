import unittest
import os
from datetime import datetime

# from cases import test_05_invest
from libs.HTMLTestRunnerNew import HTMLTestRunner
from scripts.handle_yaml import do_yaml
from scripts.handle_path import REPORTS_DIR, USER_ACCOUNTS_FILE_PATH, CASES_DIR
from scripts.handle_user import generate_users_config

# 如果用户账号所在文件不存在, 则创建用户账号, 否则不创建
if not os.path.exists(USER_ACCOUNTS_FILE_PATH):
    generate_users_config()

# 创建测试套件
suite = unittest.TestSuite()

# 将一个模块中的所有测试用例，加载到测试套件
# loader = unittest.TestLoader()
# suite.addTest(loader.loadTestsFromModule(test_05_invest))

# 将目录下所有模块中的测试用例，加载到测试套件
loader = unittest.TestLoader()
suite.addTest(loader.discover(CASES_DIR))

result_full_path = do_yaml.read('report', 'name') + '_' + \
                   datetime.strftime(datetime.now(), '%Y%m%d%H%M%S') + '.html'
result_full_path = os.path.join(REPORTS_DIR, result_full_path)
with open(result_full_path, 'wb') as fb:
    # 创建测试运行程序
    runner = HTMLTestRunner(stream=fb,
                            title=do_yaml.read('report', 'title'),
                            description=do_yaml.read('report', 'description'),
                            tester=do_yaml.read('report', 'tester'))
    # 执行测试套件中的用例
    runner.run(suite)
