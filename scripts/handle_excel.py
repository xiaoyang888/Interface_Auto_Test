import os
import openpyxl

from scripts.handle_path import DATAS_DIR
from scripts.handle_yaml import do_yaml


class CaseData:
    """测试用例数据类，专门用来创建对象，存放用例数据"""
    pass


class HandleExcel(object):

    def __init__(self, sheetname, filename=None):
        if filename is None:
            self.filename = os.path.join(DATAS_DIR, do_yaml.read("excel", "cases_path"))
        else:
            self.filename = filename
        self.sheetname = sheetname

    def open(self):
        """打开工作表和表单"""
        self.wb = openpyxl.load_workbook(self.filename)
        self.sh = self.wb[self.sheetname]

    def read_data(self):
        """读取数据的方法"""
        # 打开工作簿和表单
        self.open()
        # 将表单中的内容，按行获取所有的格子
        rows = list(self.sh.rows)
        # 创建一个空列表，用例存放所有的用例数据
        cases = []
        # 获取表头，放到一个列表中
        title = [c.value for c in rows[0]]
        # 获取除表头以外的其他行中的数据
        for r in rows[1:]:
            # 每遍历一行，创建一个列表，用例存放该行的数据
            data = [c.value for c in r]
            # 将表头和该行的数据进行聚合打包，转换字典
            case_data = dict(zip(title, data))
            # 将该行的用例数据加入到cases这个列表中
            cases.append(case_data)
        # 关闭工作簿对象
        self.wb.close()
        # 将读取好的数据返回出去
        return cases

    def read_data_obj(self):
        """读取数据的方法,数据返回的是列表嵌套对象的形式"""
        # 打开工作簿和表单
        self.open()
        # 将表单中的内容，按行获取所有的格子
        rows = list(self.sh.rows)
        # 创建一个空列表，用例存放所有的用例数据
        cases = []
        # 通过列表推导式获取表头，放到一个列表中
        title = [c.value for c in rows[0]]
        # 获取除表头以外的其他行中的数据
        for r in rows[1:]:
            # 通过列表推导式，获取改行的数据，放到一个列表中
            data = [c.value for c in r]
            # 创建一个用例数据对象
            case = CaseData()
            # 将表头和该行的数据进行聚合打包，然后进行遍历
            for i in zip(title, data):
                # 通过反射机制，将表头设为对象属性，对应值设为对象的属性值
                setattr(case, i[0], i[1])
            # 将该行的用例数据加入到cases这个列表中
            cases.append(case)
        # 关闭工作薄
        self.wb.close()
        # 将读取好的数据返回出去
        return cases

    def write_data(self, row, column, value):
        """写入数据"""
        # 打开工作簿和表单
        self.open()
        # 写入内容
        self.sh.cell(row=row, column=column, value=value)
        # 保存文件
        self.wb.save(self.filename)
        # 关闭工作簿
        self.wb.close()


if __name__ == '__main__':
    read = HandleExcel('register')
    print(read)
