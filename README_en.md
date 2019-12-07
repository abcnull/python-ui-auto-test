**[中文](https://github.com/abcnull/python-ui-auto-test/blob/master/README.md) | [Blog](https://blog.csdn.net/abcnull/article/details/103379143)**

[TOC]
# python-ui-auto-test

python + selenium + unittest + PageObject + BeautifulReport + redis + mysql + ParamUnittest + tomorrow + ThreadLocal + screenshot + log + multiple browser drivers + RemoteWebDriver + .ini file reader + configurable projects

Thanks to Pengfei Li for his technical support during the construction process! If you have any further questions, please contact us through the following channels

Welcome to **Watch**, **Star** and **Fork**！

- Author: **abcnull**
- Csdn Blog: **https://blog.csdn.net/abcnull**
- GitHub: **https://github.com/abcnull**
- E-Mail: **abcnull@qq.com**

## Hierarchy

```
python-ui-auto-test
    - api-test（api test package, to be continue...）
    - ui-test（ui test package）
        - base（related to the project initialization configuration）
        - case（test case）
        - common（common package）
        - data（data driving）
        - locator（element locator）
        - page（page object）
        - report（report package）
            - html（html report）
            - log（log report）
            - img（test screenshot）
        - resource（resouece package）
            - config（configuration of peoject）
            - driver（drivers）
        - util（utility package）
        - README.md（project brief）
        - requirements.txt（dependencies list）
        - run_all.py（runnable test suite, single thread）
        - run_all_mutithread.py（runnable test suite, muti thread）
    - venv（virtual environment）
    - .gitignore（git ignore list）
External Libraries
Scratches and Consoles
```

![framework](https://github.com/abcnull/Image-Resources/blob/master/python-ui-auto-test/1575304456217.png)


## Framework Overview

- Using PO structure, and making it more detailed, i put element locator in locator package and put data-driven data in data package, case holding test case

- Common contains PageCommon class and BrowserCommon class, and they are code that encapsulates page operations and browser operations, respectively

- Base contains Assembler initial tool which is to initial database and driver, and others before the test suite runs. `__init__(self)`function source is as follows:

  ```python
  # init
      def __init__(self):
          # assemble driver
          self.assemble_driver()
          # assemble redis 
          if ConfigReader().read("project")["redis_enable"].upper() == "Y":
              self.assemble_redis()
          elif ConfigReader().read("project")["redis_enable"].upper() == "N":
              self.redis_pool_tool = None
          else:
              self.redis_pool_tool = None
              raise RuntimeError("配置文件中配置 redis 是否启用字段有误！请修改！")
          # assemble mysql
          if ConfigReader().read("project")["mysql_enable"].upper() == "Y":
              self.assemble_mysql()
          elif ConfigReader().read("project")["mysql_enable"].upper() == "N":
              self.mysql_tool = None
          else:
              self.mysql_tool = None
              raise RuntimeError("配置文件中配置 mysql 是否启用字段有误！请修改！")
          # store thread and data in ThreadLocalStorage
          ThreadLocalStorage.set(threading.current_thread(), self)
  ```
  
- Report package contains html report, log report and test screenshot, respectively. Test report use BeautifulReport dependency. The generation of log report can be controlled by util/config/config.ini. Because of the flaw of the BeautifulReport, screenshot is supposed to be in project/img package, i want the screenshot in resource/img for i was used to java project structure. Up to now, i still use `../` to stitch path as `@BeautifulReport`. For the peculiarity of Firefox, which can generate a log report by himself in case package, i aslo use `../` to make the log move to resource/log. Html report and screenshot can be configured to enable or disable. Log have been configured that maximum rotation is 5 and repetition switch control file name repetition. Taking html for example, we can decide the report use a new name or the repective name just according to a Configuration. The function use a recursive method as follows:

  ```python
  # recursion
  # get a new name controlled by configuration
  def get_html_name(self, filename: str = None, report_dir="."):
      """
          get new report name
          :param filename: old report name
          :param report_dir: report path
          :return: a new name controlled by name repetition enable switch in configuration file
          """
      # if allow name repetition
      if ConfigReader().read("html")["cover_allowed"].upper() == "Y":
          # get new report name
          return filename
      # else if not allow name repetition
      elif ConfigReader().read("html")["cover_allowed"].upper() == "N":
          # if path right
          if os.path.exists(report_dir + filename + ".html"):
              # if the report name not end with ")"
              if not filename.endswith(")"):
                  filename = filename + "(2)"
                  # else the reprot name end with ")"
                  else:
                      file_num = filename[filename.index("(") + 1: -1]
                      num = int(file_num)
                      # num ++
                      num += 1
                      filename = filename[:filename.index("(")] + "(" + str(num) + ")"
                      # else name not exist
                      else:
                          # recursive export
                          return filename
                      # recursive: change filename constantly
                      return self.get_html_name(filename, report_dir)
                  # else it neither Y/y nor N/n, throw error
                  else:
                      raise RuntimeError("config.ini中[html]的cover_allowed字段配置错误，请检查！")
  ```

- In resource package, config realized that driver package contains all mainstream drivers, and all version info are in config.ini file

  ![框架概述](https://github.com/abcnull/Image-Resources/blob/master/python-ui-auto-test/1575305550583.png)

- Utiltiy package ccontains .ini file reader, log tool, mysql tool, redis tool, report generator, screenshot tool, text tool,  local storage tool

- `run_all.py`can run suite through a single thread, `run_all_mutithread` can run suite through muti thread. What should be paid attention to is when we run suite through muti thread, we can not get one report per thread. What can we do to solve this problem? Redevelop BeautifulReport can solve this

## Running Process

Project use mainstream idea - PageObject. Logical code can be amended in page package. Business flow can be amended in case package. The changes of data or element locator can be quickly tracked and modified. Base Package contains initial tool. Common package contains common funtions. How do the test case run? Let's see following explanations:

- Case package contains test class is made up of functions which starts with a word - test. These functions create an object of Assembler through `setUp()` function which contains a driver instance. When a test function run, it can create a new object of Assembler containing driver instance. A test function is a whole test process
- If you don't want to write `setUp()`, you can write another function, and then you can call the function you just write in the first line of some functions that you need test, so that this test functions can run after what you write before
- This fromework has a very nice feature. For example, like Taobao, Tianmao and other ebusiness system, they can be devided into good detail page, cart page, settlment page and others, so when we have created these page object, and we have written them in corresponding case, and we want to String a series cases as a whole process, we can take out the driver and other data in current thread.In Assembler's initialize funtion, we put the data in a static dictionary which storages the thread and data in the form of key-value pairs.
- These test case alse have other organization form because of ParamUnittest dependency. If we move Assembler object in the outside params of ParamUnittest, the test functions below all can use the data in Assembler object. This way is also OK and there are a lot of ways. ParamUnittest, local storage, config.ini make case orgnization very flexible. How you organize test cases can accord to the requirment of your project and you can also add some idea in this framework depend on your need

## Assembler 

The features: 

- Initialization of mainstream drivers
- Assembling redis 
- Assembling mysql
- Storing all data and thread in a static dictionary

## ParamUnittest

Environment could be SIT,  UAT or PROD, so we can modify parameters in config.ini to control the running way of the suites and cases. You guys can also consider to write the parameters in`run_all.py` for the same purpose. There is another parameter besides enviroment parameter - language. It means that you can select specified language and to control data package using which data, if you amend code in data package a little bit. Except these parameters, you can also add other parameters unused

![ParamUnittest](https://github.com/abcnull/Image-Resources/blob/master/python-ui-auto-test/1575369275406.png)

## config.ini

Contains:

- [project] project configuration, like customized parameters, some kinds of mainstream drivers, remote server ip, redis/mysql enable switch etc.
- [driver] almost all of mainstream browsers’ drivers
- [redis] redis configuration
- [mysql] mysql configuration
- [screenshot] screenshot path and screenshot format and name repetition enable switch
- [html] html report name configuration, report path and name repetition enable switch
- [log] there are lots of configurations here

Follew-up user can add oracle, sqlserver, mongoDB and other configuration in .ini file to make theproject perfect.Don't forget to add code in Assembler!

![config.ini](https://github.com/abcnull/Image-Resources/blob/master/python-ui-auto-test/1575369314016.png)

## Utility

- ConfigReader: .ini file reader

- LogTool: log generator

- MysqlTool: mysql generator

- RedisPool: redis pool generator

- ReportTool: html report generator, just add a shell to BeautifulReport in order to control the generative process by configuration file

- ScreenshotTool: screenshot generator

- TextTool: just for a startup text

- ThreadLocalStorage: store thread and Assembler object in a static dictionary through key-value pairs in order to take out the data in any test case

  ![工具类](https://github.com/abcnull/Image-Resources/blob/master/python-ui-auto-test/1575369333647.png)

## Bottom Line

There is much about this project to optimized. I sincerely holp for your **Watch**, **Start**, **Fork**! Your commit will help us better improve the project!
Thanks again!

: )

- Author: **abcnull**
- Csdn Blog: **https://blog.csdn.net/abcnull**
- GitHub: **https://github.com/abcnull**
- E-Mail: **abcnull@qq.com**
