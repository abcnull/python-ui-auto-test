**[English]() | [博客](https://blog.csdn.net/abcnull/article/details/103379143)**

[TOC]
# python-ui-auto-test

python + selenium + unittest + PO + BeautifulReport + redis + mysql + ParamUnittest + 多线程 + 截图/日志 + 多浏览器支持 + RemoteWebDriver +文件读取 + 全参数化构建

搭建过程中非常感谢李鹏飞大侠的技术支持！后续有问题请在如下途径私聊联系！

欢迎大家 **Watch**，**Star** 和 **Fork**！

- 框架作者：**abcnull**
- csdn 博客：**https://blog.csdn.net/abcnull**
- github：**https://github.com/abcnull**
- e-mail：**abcnull@qq.com**

## 框架结构

```
python-ui-auto-test
    - api-test（api 测试包，未添加内容）
    - ui-test（ui 测试包）
        - base（与项目初始化配置相关）
        - case（测试用例脚本）
        - common（共用方法）
        - data（数据驱动）
        - locator（页面对应的元素定位）
        - page（页面类）
        - report（输出报告）
            - html（html 类型报告）
            - log（log 日志报告）
            - img（测试截图）
        - resource（资源文件夹）
            - config（配置文件）
            - driver（驱动）
        - util（工具类）
        - README.md（项目介绍 md）
        - requirements.txt（项目依赖清单）
        - run_all.py（类似于 testng 文件执行测试套，单线程）
        - run_all_mutithread.py（类似于 testng 文件执行测试套，多线程）
    - venv（虚拟环境的文件夹，github 拉下来后需要自己创虚拟环境）
    - .gitignore（git 忽略文件）
External Libraries
Scratches and Consoles
```

![框架结构](https://github.com/abcnull/Image-Resources/blob/master/python-ui-auto-test/1575304456217.png)


## 框架概述

- 采用 PO 思想，将 PageObject 更细致化，使得页面的元素定位和页面对应的数据分别放在 locator 和 data 中，case 中存放测试用例

- common 中存放了 PageCommon 和 BrowserCommon，分别是封装了页面操作和浏览器操作的代码

- base 中存放的是初始化数据库和驱动的 Assembler 装配器，用来在测试用例之初创建初始化配置。其`__init__(self)`方法源码如下所示：

  ```python
  # 初始化所有工具
      def __init__(self):
          # 驱动装配
          self.assemble_driver()
          # redis 工具装配
          if ConfigReader().read("project")["redis_enable"].upper() == "Y":
              # 装配 redis 连接池工具
              self.assemble_redis()
          elif ConfigReader().read("project")["redis_enable"].upper() == "N":
              self.redis_pool_tool = None
          else:
              self.redis_pool_tool = None
              raise RuntimeError("配置文件中配置 redis 是否启用字段有误！请修改！")
          # mysql 工具装配
          if ConfigReader().read("project")["mysql_enable"].upper() == "Y":
              # 装配 mysql 工具
              self.assemble_mysql()
          elif ConfigReader().read("project")["mysql_enable"].upper() == "N":
              self.mysql_tool = None
          else:
              self.mysql_tool = None
              raise RuntimeError("配置文件中配置 mysql 是否启用字段有误！请修改！")
          # 将装配器保存到线程存储器中，键名为线程，键值为装配器对象
          ThreadLocalStorage.set(threading.current_thread(), self)
  ```

- report 中分别存放了 html 测试报告，log 日志信息和 img 截图。测试报告采用 BeautifulReport 模板，log 日志的输出可以通过 util/config/config.ini 进行全套参数化配置，截图这块受于 BeautifulReport 的限制本来是存放于项目下 img 中，但目前通过`../`的方式还是将截图放在这里。对于火狐驱动会产生 log 日志在 case 用例中，目前我也通过`../`将火狐的日志移动此 log 文件夹中。html 和 截图可以配置选择重名是否被覆盖，log 直接配置成最大轮转数为 5，重名是否被覆盖，拿 html 举例，可以判断重名获取新的报告名，采用递归思想，源码如下所示：

  ```python
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
  ```

- 资源文件夹中 config 实现了项目完全依靠参数来配置运行，driver 文件夹中目前存放了所有主流驱动，版本信息请见 config.ini 中有介绍

  ![框架概述](https://github.com/abcnull/Image-Resources/blob/master/python-ui-auto-test/1575305550583.png)

- 工具类中包括配置文件读取器，log 日志工具，mysql 连接工具，redis 连接池工具，报告生成工具，截图工具，文本工具，线程本地存储工具
- `run_all.py`可以单线程运行所有测试用例，`run_all_mutithread`则可以多线程运行测试用例，但是要注意的是多线程运行后测试报告还是无法汇总成一个报告，这个得对 BeautifulReport 进行二次开发才可以解决

## 层次结构思想

框架采用火热的 PageObject（PO）思想使得结构更加清晰，对于逻辑性代码可以在 page 文件夹中维护，业务流程组织可以在 case 中维护，data 数据改变或者 locator 元素定位改变也可以快速跟踪修改，base 中存放初始化的工具，common 存放共用方法。至于用例如何组织来运行，可见下面几种方式

- case 文件中的一个测试类中分有多个 test 打头的方法，这些方法通过`setUp()`方法来初始化装配器（装配器中含有一个驱动），也就是一个 test 打头的方法为一个测试点，每开一个测试点相当于使用了一个新的装配器，其中含有驱动。测试类中一个 test 打头的方法可以是一个完整流程
- 如若不希望写`setUp()`，自己可以专门写个方法放在某一个 test 打头的方法里头也行，这样不会每个 test 都跑这个方法了
- 框架中有个非常好用的功能，比如测试电商系统类似淘宝，天猫的购物网站系统，分为商品页面，购物车页，结算页等，当我们分别按页面写好 page 之后，并且 case 中分别测试的是各个页面的功能点，如果我们需要把几个 case 串联起来，该如何去做呢，由于装配器中创建驱动之后会把驱动和对应的线程号保存到静态字典中，我们直接在另一个 case 中依据当前线程去取驱动即可接着上一个 case 跑了
- 用例的其他组织方式，由于存在 ParamUnittest 工具，把 Assembler 装配器（内含驱动）专门放在测试类上的字典参数中，这样该类下每个测试方法都可以直接取用，这种方式也是可以的，也能组织跑一个类中完整的流程，还有多种方式，由于含有 ParamUnittest 外不传参，线程本地存储，config.ini 全参数化构建，用例的组织非常灵活，可以根据项目具体需求稍微加以修改增加功能

## Assembler 装配器

有几大点功能：

- 各种类型驱动初始化
- redis 装配
- mysql 装配
- 将该装配器对象和本地线程保存到一个静态字典中，方便在其他 case 中对驱动的取用

## ParamUnittest 外部传参

由于待测的环境可能是 SIT 或是 UAT 或是 PROD，所以可以通过 config.ini 修改参数的方式来往 case 中的类上参数中传值，进而传进类中的测试方法中。小伙伴们也可以考虑下二次开发直接在`run_all.py`中把参数传进具体的 case 里。还有一个参数是语言参数，对于多语言环境，可以修改此参数进而可以选择 data 中的指定数据。小伙伴们当然也可以根据项目需求自己增加自己需要的参数

![ParamUnittest 外部传参](https://github.com/abcnull/Image-Resources/blob/master/python-ui-auto-test/1575369275406.png)

## config.ini 项目配置

其中包含

- [project] 项目配置，如自定义的参数，哪种驱动，远程服务器 ip，redis/mysql 是否启用等参数
- [driver] 几乎所有主流浏览器驱动路径
- [redis] redis 各项配置
- [mysql] mysql 各项配置
- [screenshot] 截图路径以及截图格式和截图是否支持覆盖
- [html] 包含报告名，报告存放路径以及报告是否支持覆盖
- [log] 这个 log 日志的配置比较多，可以详细查看该文件

后续小伙伴可以添加 oracle，sqlserver，mongoDB 等的配置参数进去，记得同时要给 Assembler 装配器增添代码

![config.ini 项目配置](https://github.com/abcnull/Image-Resources/blob/master/python-ui-auto-test/1575369314016.png)

## 工具类

- ConfigReader 项目参数化构建的配置文件读取器

- LogTool log 日志工具类

- MysqlTool mysql 连接工具可以返回一个连接成功的 mysql 连接

- RedisPool redis 连接池工具，其中包含连接池对象和连接池中的一个连接

- ReportTool 报告生成工具，对 BeautifulReport 封装了一层外壳，可以依据配置文件进行同名文件覆盖或不覆盖

- ScreenshotTool 截图工具

- TextTool 文字工具，简单的生成一段文字信息

- ThreadLocalStorage 用于将线程号和 Assembler 装配器通过键值对形式存进一个静态字典中，方便在不同 case 中取用装配器中的驱动

  ![工具类](https://github.com/abcnull/Image-Resources/blob/master/python-ui-auto-test/1575369333647.png)

## 写在后头

项目仍有许多值得修改优化的地方，望 commit 宝贵意见，更好完善框架内容！
再次感谢！

- 框架作者：**abcnull**
- csdn 博客：**https://blog.csdn.net/abcnull**
- github：**https://github.com/abcnull**
- e-mail：**abcnull@qq.com**
