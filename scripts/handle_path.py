import os

# 项目根路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 获取配置文件目录路径
CONFIGS_DIR = os.path.join(BASE_DIR, "configs")

# 获取配置文件路径
CONFIGS_FILE_PATH = os.path.join(CONFIGS_DIR, "testcase.yaml")

# 获取日志文件目录路径
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# 获取报告文件目录路径
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# 获取excel文件目录路径
DATAS_DIR = os.path.join(BASE_DIR, "datas")

# 获取用户账号所在配置文件的路径
USER_ACCOUNTS_FILE_PATH = os.path.join(CONFIGS_DIR, 'user_account.yaml')

# 测试用例模块所在目录路径
CASES_DIR = os.path.join(BASE_DIR, 'cases')
