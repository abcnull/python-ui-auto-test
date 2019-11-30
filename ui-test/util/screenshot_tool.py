import os
from util.config_reader import ConfigReader


# 截图工具，可控制图片是否被覆盖
class ScreenshotTool:
    # 错误截图方法
    def save_img(self, driver, img_name):
        """
        截图并保存进指定路径
        :param driver: 驱动
        :param img_name: 截图名
        :return: 新的截图名
        """
        # 图片绝对路径
        img_path = r"" + os.path.abspath(os.path.dirname(__file__))[
                         :os.path.abspath(os.path.dirname(__file__)).find("python-ui-auto-test\\") + len(
                             "python-ui-auto-test\\")] + "ui-test" + ConfigReader().read("screenshot")["shotfile_path"]
        # 获取新的图片名
        new_img_name = self.get_img_name(img_name)
        # 根据配置文件的配置，截图智能存放
        driver.get_screenshot_as_file(("{}/{}" + ConfigReader().read("screenshot")["shot_format"]).format(img_path, new_img_name))
        # 由于可配置是否允许图片被覆盖，这里返回的是图片新名字
        return new_img_name

    # 递归方法
    # 判断图片的名字在配置文件指定路径下是否有重复，并根据配置是否允许重复返回图片新的名字
    def get_img_name(self, img_name):
        """
        获取新的截图名
        :param img_name: 截图名
        :return: 新的截图名
        """
        # 图片绝对路径
        img_path = r"" + os.path.abspath(os.path.dirname(__file__))[
                         :os.path.abspath(os.path.dirname(__file__)).find("python-ui-auto-test\\") + len(
                             "python-ui-auto-test\\")] + "ui-test" + ConfigReader().read("screenshot")["shotfile_path"]
        # 判断同名截图是否支持覆盖，若支持覆盖同名图片
        if ConfigReader().read("screenshot")["cover_allowed"].upper() == "Y":
            # 返回截图名字
            return img_name
        # 若不支持覆盖同名图片
        elif ConfigReader().read("screenshot")["cover_allowed"].upper() == "N":
            # 判断图片路径是否存在，若存在
            if os.path.exists(img_path + img_name + ConfigReader().read("screenshot")["shot_format"]):
                # 如果名字不以 ")" 结尾
                if not img_name.endswith(")"):
                    img_name = img_name + "(2)"
                # 如果名字以 ")" 结尾
                else:
                    img_num = img_name[img_name.index("(") + 1: -1]
                    num = int(img_num)
                    # 图片名称字段自增
                    num += 1
                    img_name = img_name[:img_name.index("(")] + "(" + str(num) + ")"
            # 若图片不存在
            else:
                # 递归出口
                return img_name
            # 递归：不断改变 img_name 后图片是否还能找到
            return self.get_img_name(img_name)
        # 若配置中既不是 Y/y 也不是 N/n 就抛出异常
        else:
            raise RuntimeError("config.ini中[img]的cover_allowed 字段配置错误，请检查！")
