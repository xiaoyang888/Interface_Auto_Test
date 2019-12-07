from scripts.handle_mysql import HandleMysql
from scripts.handle_request import HandleRequest
from scripts.handle_yaml import do_yaml
from scripts.handle_path import USER_ACCOUNTS_FILE_PATH


def create_new_user(reg_name, pwd="12345678", user_type=1):
    """
    创建一个用户
    :param reg_name: 用户名
    :param pwd: 密码
    :param user_type: 用户类型
    :return: 存储一个用户信息, 嵌套字典的字典(以用户名为key, 以用户信息所在字典为value)
    """
    # 建立连接
    do_mysql = HandleMysql()
    do_request = HandleRequest()
    # 添加公共请求头
    do_request.add_headers(do_yaml.read('api', 'header'))

    url = do_yaml.read('api', 'url_prefix') + '/member/register'
    sql = do_yaml.read('mysql', 'select_userid_sql')
    while True:
        mobile_phone = do_mysql.create_not_existed_mobile()
        data = {
            "mobile_phone": mobile_phone,
            "pwd": pwd,
            "reg_name": reg_name,
            "type": user_type
        }
        # 注册接口发起请求
        do_request.send(url, data=data)

        # 查询数据库, 获取用户id
        result = do_mysql.run(sql=sql, param=[mobile_phone])
        if result:
            user_id = result["id"]
            break

    # 构造用户信息字典
    user_dict = {
        reg_name: {
            "id": user_id,
            "reg_name": reg_name,
            "mobile_phone": mobile_phone,
            "pwd": pwd
        }
    }

    # 关闭连接
    do_mysql.close()
    do_request.close()

    return user_dict


def generate_users_config():
    """
    生成三个用户信息
    :return:
    """
    users_datas_dict = {}
    users_datas_dict.update(create_new_user("admin", user_type=0))
    users_datas_dict.update(create_new_user("invest"))
    users_datas_dict.update(create_new_user("borrow"))
    do_yaml.write(users_datas_dict, USER_ACCOUNTS_FILE_PATH)


if __name__ == '__main__':
    generate_users_config()
