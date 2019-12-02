import os
import unittest
from case import test_baidu_case, test_csdn_case, test_other_case
from util.config_reader import ConfigReader
from util.report_tool import ReportTool
from tomorrow import threads

# 报告存放路径
report_path = os.path.abspath(os.path.dirname(__file__))[
              :os.path.abspath(os.path.dirname(__file__)).find("python-ui-auto-test") + len(
                  "python-ui-auto-test")] + "/ui-test" + ConfigReader().read("html")["htmlfile_path"]


# 报告名字
# report_name = ConfigReader().read("html")["htmlfile_name"]


# 设置三线程
@threads(3)
def run_mutithread(test_suite):
    # 报告生成器，运行用例并生成报告，对 BeautifulReport 套了一层外壳
    ReportTool(test_suite).run(filename=new_report_name, description='demo', report_dir=report_path, theme="theme_cyan")


# 运行所有用例（多线程，运行无问题，但是产出报告会被覆盖，未解决）
if __name__ == "__main__":
    # 创建测试套
    suites = unittest.TestSuite()
    loader = unittest.TestLoader()

    # 百度测试流程添加到测试套
    suites.addTests(loader.loadTestsFromModule(test_baidu_case))
    # csdn 测试流程添加到测试套
    suites.addTests(loader.loadTestsFromModule(test_csdn_case))
    # 其他测试流程（这一行可以取消注释，可以查看断言错误的截图在报告中的效果）
    # suites.addTests(loader.loadTestsFromModule(test_other_case))

    # 循环遍历
    n = 0
    for i in suites:
        # 循环次数
        n += 1
        # 获取多线程报告名字
        report_name = ConfigReader().read("html")["htmlfile_name"] + "-第" + str(n) + "个线程"
        new_report_name = ReportTool(suites).get_html_name(filename=report_name, report_dir=report_path)
        # 多线程运行
        run_mutithread(i)
