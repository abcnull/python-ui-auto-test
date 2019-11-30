import os
from BeautifulReport import BeautifulReport
from util.config_reader import ConfigReader
from util.text_tool import TextTool


# BeautifulReport 报告产生器，可控制文件是否支持覆盖
class ReportTool:
    # 构造器
    def __init__(self, suites):
        """
        构造器
        :param suites: 测试套件
        """
        self.suites = suites

    # 运行并产出报告方法
    def run(self, description, filename: str = None, report_dir=".", log_path=None, theme="theme_default"):
        """
        运行测试套并产生报告进行存放
        :param description: 见 BeautifulReport 的 report 方法参数
        :param filename: 见 BeautifulReport 的 report 方法参数
        :param report_dir: 见 BeautifulReport 的 report 方法参数
        :param log_path: 见 BeautifulReport 的 report 方法参数
        :param theme: 见 BeautifulReport 的 report 方法参数
        :return: 返回新的报告名称
        """
        # 项目开始装配时输出文本到控制台
        TextTool().project_start()
        # 获取新的报告名
        new_filename = self.get_html_name(filename, report_dir)
        # 运行测试并产出报告存放 self.get_html_name(filename, report_dir)
        BeautifulReport(self.suites).report(filename=new_filename, description=description, report_dir=report_dir,
                                            theme=theme)
        # 由于可配置是否允许报告被覆盖，这里返回的是报告新名字
        return new_filename

    # 递归方法
    # 判断报告的名字在配置文件指定路径下是否有重复，并根据配置是否允许重复返回报告新的名字
    def get_html_name(self, filename: str = None, report_dir="."):
        """
        获取新的报告名
        :param filename: 报告名称
        :param report_dir: 报告路径
        :return: 通过配置文件判断报告是否可以被覆盖，返回新的报告名
        """
        # 若允许被覆盖同名报告
        if ConfigReader().read("html")["cover_allowed"].upper() == "Y":
            # 返回报告名
            return filename
        # 若不支持覆盖同名报告
        elif ConfigReader().read("html")["cover_allowed"].upper() == "N":
            # 判断报告路径是否存在，若存在
            if os.path.exists(report_dir + filename + ".html"):
                # 如果名字不以 ")" 结尾
                if not filename.endswith(")"):
                    filename = filename + "(2)"
                # 如果名字以 ")" 结尾
                else:
                    file_num = filename[filename.index("(") + 1: -1]
                    num = int(file_num)
                    # 报告名称字段自增
                    num += 1
                    filename = filename[:filename.index("(")] + "(" + str(num) + ")"
            # 若报告不存在
            else:
                # 递归出口，运行测试并产出报告存放
                return filename
            # 递归：不断改变 filename 后报告是否还能找到
            return self.get_html_name(filename, report_dir)
        # 若配置中既不是 Y/y 也不是 N/n 就抛出异常
        else:
            raise RuntimeError("config.ini中[html]的cover_allowed字段配置错误，请检查！")
