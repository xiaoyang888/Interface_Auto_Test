import random
import pymysql

from scripts.handle_yaml import do_yaml


class HandleMysql:
    def __init__(self):
        self.conn = pymysql.connect(host=do_yaml.read("mysql", "host"),  # mysql服务器ip或者域名
                                    user=do_yaml.read("mysql", "user"),  # 用户名
                                    password=do_yaml.read("mysql", "password"),  # 密码
                                    db=do_yaml.read("mysql", "db"),  # 要连接的数据库名
                                    port=do_yaml.read("mysql", "port"),  # 数据库端口号, 默认为3306
                                    charset='utf8',  # 数据库编码为utf8, 不能设为utf-8
                                    # 默认返回的结果为元祖或者嵌套元祖的列表
                                    # 可以指定cursorclass为DictCursor, 那么返回的结果为字典或者嵌套字典的列表
                                    cursorclass=pymysql.cursors.DictCursor
                                    )
        self.cursor = self.conn.cursor()

    def run(self, sql, param=None, is_more=False):
        self.cursor.execute(sql, param)
        self.conn.commit()
        if is_more:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.conn.close()

    @staticmethod
    def create_mobile():
        """
        随机生成11位手机号
        :return:
        """
        return '188' + ''.join(random.sample('0123456789', 8))

    def is_existed_mobile(self, mobile):
        """
        判断手机号是否被注册
        :param mobile: 待查询的手机号
        :return:
        """
        sql = do_yaml.read("mysql", "user_select_sql")
        if self.run(sql, param=[mobile]):
            return True
        else:
            return False

    def create_not_existed_mobile(self):
        """
        随机生成一个在数据库中不存在的手机号
        :return:
        """
        while True:
            one_mobile = self.create_mobile()
            if not self.is_existed_mobile(one_mobile):
                break

        return one_mobile


if __name__ == '__main__':
    # sql_2 = "SELECT * FROM member WHERE mobile_phone = '13888888889';"
    # sql_3 = "SELECT * FROM member LIMIT 0,10;"

    do_mysql = HandleMysql()
    # print(do_mysql.run(sql_2))
    # print(do_mysql.run(sql_3, is_more=True))
    # print(do_mysql.is_existed_mobile('18664925000'))
    print(do_mysql.create_not_existed_mobile())
    do_mysql.close()
