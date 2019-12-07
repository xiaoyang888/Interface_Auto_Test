import yaml

from scripts.handle_path import CONFIGS_FILE_PATH


class HandleYaml:
    def __init__(self, filename):
        with open(filename, encoding="utf-8") as one_file:
            self.datas = yaml.full_load(one_file)

    def read(self, section, option):
        """
        读数据
        :param section: 区域名
        :param option: 选项名
        :return:
        """
        return self.datas[section][option]

    @staticmethod
    def write(datas, filename):
        """
        写数据
        :param datas: 嵌套字典的字典
        :param filename: yaml文件路径
        :return:
        """
        with open(filename, mode="w", encoding="utf-8") as one_file:
            yaml.dump(datas, one_file, allow_unicode=True)


do_yaml = HandleYaml(CONFIGS_FILE_PATH)

if __name__ == '__main__':
    # do_yaml = HandleYaml(CONFIGS_FILE_PATH)
    # print(do_yaml.read("report","name"))
    pass
