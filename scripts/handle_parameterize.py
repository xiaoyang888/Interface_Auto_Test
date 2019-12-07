import re

from scripts.handle_mysql import HandleMysql
from scripts.handle_yaml import HandleYaml
from scripts.handle_path import USER_ACCOUNTS_FILE_PATH


class Parameterize:
    """
    参数化类
    """
    # 不存在的数据正则表达式
    not_existed_mobile_pattern = r'{not_existed_mobile}'  # 未注册的手机号
    not_user_id_pattern = r'{not_user_id}'  # 不存在的用户id
    not_loan_id_pattern = r'{not_loan_id}'  # 不存在的标id

    # 投资人正则表达式
    invest_user_id_pattern = r'{invest_user_id}'  # 投资人用户id
    invest_user_mobile_pattern = r'{invest_user_mobile}'  # 投资人手机号
    invest_user_pwd_pattern = r'{invest_user_pwd}'  # 投资人密码

    # 借款人正则表达式
    borrow_user_id_pattern = r'{borrow_user_id}'  # 借款人用户id
    borrow_user_mobile_pattern = r'{borrow_user_mobile}'  # 借款人手机号
    borrow_user_pwd_pattern = r'{borrow_user_pwd}'  # 借款人密码

    # 管理员正则表达式
    admin_user_id_pattern = r'{admin_user_id}'  # 管理员用户id
    admin_user_mobile_pattern = r'{admin_user_mobile}'  # 管理员手机号
    admin_user_pwd_pattern = r'{admin_user_pwd}'  # 管理员密码

    # 其他正则表达式
    loan_id_pattern = r'{loan_id}'  # 标id

    do_user_account = HandleYaml(USER_ACCOUNTS_FILE_PATH)

    @classmethod
    def not_existed_replace(cls, data):
        do_mysql = HandleMysql()

        # 不存在的手机号替换
        if cls.not_existed_mobile_pattern in data:
            data = re.sub(cls.not_existed_mobile_pattern, do_mysql.create_not_existed_mobile(), data)

        # 不存在的用户id替换
        if cls.not_user_id_pattern in data:
            sql = "SELECT id FROM member ORDER BY id DESC LIMIT 0,1;"  # 获取最大的用户id
            not_user_id = do_mysql.run(sql=sql).get('id') + 1  # 最大用户id加1
            data = re.sub(cls.not_user_id_pattern, str(not_user_id), data)

        # 不存在的标id替换
        if cls.not_loan_id_pattern in data:
            sql = "SELECT id FROM loan ORDER BY create_time DESC LIMIT 0,1;"
            not_loan_id = do_mysql.run(sql=sql).get('id') + 1
            data = re.sub(cls.not_loan_id_pattern, str(not_loan_id), data)

        do_mysql.close()
        return data

    @classmethod
    def invest_user_replace(cls, data):
        # 投资人用户id替换
        if cls.invest_user_id_pattern in data:
            invest_user_id = cls.do_user_account.read('invest', 'id')
            data = re.sub(cls.invest_user_id_pattern, str(invest_user_id), data)

        # 投资人手机号替换
        if cls.invest_user_mobile_pattern in data:
            invest_user_mobile = cls.do_user_account.read('invest', 'mobile_phone')
            data = re.sub(cls.invest_user_mobile_pattern, invest_user_mobile, data)

        # 投资人密码替换
        if cls.invest_user_pwd_pattern in data:
            invest_user_pwd = cls.do_user_account.read('invest', 'pwd')
            data = re.sub(cls.invest_user_pwd_pattern, invest_user_pwd, data)

        return data

    @classmethod
    def borrow_user_replace(cls, data):
        # 借款人用户id替换
        if cls.borrow_user_id_pattern in data:
            borrow_user_id = cls.do_user_account.read('borrow', 'id')
            data = re.sub(cls.borrow_user_id_pattern, str(borrow_user_id), data)

        # 借款人手机号替换
        if cls.borrow_user_mobile_pattern in data:
            borrow_user_mobile = cls.do_user_account.read('borrow', 'mobile_phone')
            data = re.sub(cls.borrow_user_mobile_pattern, borrow_user_mobile, data)

        # 借款人密码替换
        if cls.borrow_user_pwd_pattern in data:
            borrow_user_pwd = cls.do_user_account.read('borrow', 'pwd')
            data = re.sub(cls.borrow_user_pwd_pattern, borrow_user_pwd, data)

        return data

    @classmethod
    def admin_user_replace(cls, data):
        # 管理员用户id替换
        if cls.admin_user_id_pattern in data:
            admin_user_id = cls.do_user_account.read('admin', 'id')
            data = re.sub(cls.admin_user_id_pattern, str(admin_user_id), data)

        # 管理员手机号替换
        if cls.admin_user_mobile_pattern in data:
            admin_user_mobile = cls.do_user_account.read('admin', 'mobile_phone')
            data = re.sub(cls.admin_user_mobile_pattern, admin_user_mobile, data)

        # 管理员密码替换
        if cls.admin_user_pwd_pattern in data:
            admin_user_pwd = cls.do_user_account.read('admin', 'pwd')
            data = re.sub(cls.admin_user_pwd_pattern, admin_user_pwd, data)

        return data

    @classmethod
    def other_replace(cls, data):
        # 标id替换
        if cls.loan_id_pattern in data:
            loan_id = getattr(cls, 'loan_id')
            data = re.sub(cls.loan_id_pattern, str(loan_id), data)

        return data

    @classmethod
    def to_param(cls, data):
        data = cls.not_existed_replace(data)
        data = cls.invest_user_replace(data)
        data = cls.borrow_user_replace(data)
        data = cls.admin_user_replace(data)
        data = cls.other_replace(data)

        return data


if __name__ == '__main__':
    # 未注册的手机号参数化
    one_str = '{"mobile_phone":"{not_existed_mobile}","pwd":"12345678","type":0,"reg_name":"xiaoyang"}'
    print(f"未注册的手机号参数化：{Parameterize.to_param(one_str)}")

    # 投资人id、手机号、密码参数化
    two_str = '{"member_id": "{invest_user_id}"},{"mobile_phone":"{invest_user_mobile}","pwd":"{invest_user_pwd}"}'
    print(f"投资人id、手机号、密码参数化：{Parameterize.to_param(two_str)}")

    # 借款人id、手机号、密码参数化
    three_str = '{"member_id": "{borrow_user_id}"},{"mobile_phone":"{borrow_user_mobile}","pwd":"{borrow_user_pwd}"}'
    print(f"借款人id、手机号、密码参数化：{Parameterize.to_param(three_str)}")

    # 管理员id、手机号、密码参数化
    four_str = '{"member_id": "{admin_user_id}"},{"mobile_phone":"{admin_user_mobile}","pwd":"{admin_user_pwd}"}'
    print(f"管理员id、手机号、密码参数化：{Parameterize.to_param(four_str)}")

    # 不存在的用户id参数化
    five_str = '{"member_id": "{not_user_id}"}'
    print(f"不存在的用户id参数化：{Parameterize.to_param(five_str)}")

    # 不存在的标id参数化
    six_str = '{"loan_id": "{not_loan_id}"}'
    print(f"不存在的标id参数化：{Parameterize.to_param(six_str)}")
