[toc]

python + selenium + unittest

# 1.框架注意点-使用前必看！
- `ui-test/case`中存放测试用例，测试用例的`.py`文件需要以 test 打头
- `ui-test/page`中存放 PO 对象，PO 对象中的测试点方法名需要以 test 开头，并且通过下划线加数字形式进行执行排序
- `ui-test/resource/driver`中的谷歌驱动对应浏览器 77 版本的，对于 78 及以上版本的浏览器还需要小伙伴们自行更新驱动文件
- 学习过 testng 的人知道可以利用 testng 的注解来调整驱动的执行时期，unittest 一般把驱动初始化放在 setUp 方法中（类似`@BeforeTest`），放在 test 打头的方法貌似是不行的，因为`unittest.main()`每执行一个 test 方法实际上是新创一个实例对象
- 此项目中已将`api-test`和`ui-test`设置成包文件夹，虽然`api-test`包中为空
- `case`包中有时候`before_setUp()`和`after_tearDown()`方法存在是有必要的，因为并不是每一个测试方法需要`setUp()`执行在前，有的可能只需要`before_setUp()`执行在前，`after_SetUp()`也是一样的道理
- 此项目在我电脑中才用虚拟环境，所以在`.gitignore`中把`venv`文件取消了跟踪
- `ui-test`包中`/resource/config/config.ini`中的键名参数不能大写，以为读取`.ini`的键名必以小写读出！
- `ui-test`包中`/util/log_tool.py`中最下方请不要取消注释，除非`log_tool.py`去单独调试
- 除了项目名是`python-ui-auto-test`，其下目录名或文件名不要使用同名，当 ci/cd 集成时其上目录名要不要使用此名，因为代码中根据此名寻找路径，同名文件寻找路径会出现异常
- `config.ini`文件中一些路径的参数后面是必加`/`，否则会有异常请注意，如`htmlfile_path`参数
- 各测试点方法上的装饰器的参数需要固定这么写，因为它默认保存到 img 下，我也很无奈啊╮(╯▽╰)╭

# 2.所需依赖
```
BeautifulReport 0.1.2	
pip             10.0.1	
selenium        3.141.0	
setuptools      39.1.0	
urllib3	        1.25.7	
```

# 3.项目结构
```
python-ui-auto-test
    - ui-test（ui 测试包）
        - base（与项目初始化配置相关）
        - case（测试用例脚本）
        - common（共用方法）
        - data（数据驱动）
        - listener（监听器）
        - locator（页面对应的元素定位）
        - page（页面类）
        - report（输出报告）
            - html（html 类型报告）
            - log（log 日志报告）
            - screenshot（测试截图）
        - resource（资源文件夹）
            - config（配置文件）
            - driver（驱动）
        - util（工具类）
    - venv（虚拟环境的文件夹）
    - .gitignore（git 忽略文件）
    - execute.py（类似于 testng 文件执行测试套）
    - README.md（项目介绍 md）
    - requirements.txt（项目依赖清单）
```
# 4.该项目缺少
1. 多线程考虑报告被覆盖
2. 多语言考虑
3. 使用 redis 存取值
4. 进行各种浏览器的识别
5. 连接服务器配置相关
6. 连接 mysql 操作

# 5.可以拓展补充的地方
1. 运行多线程时，虽然确实实现了多线程，但是报告中没有将几个多线程的用例联合起来，而是一个线程一个报告，然后报告被覆盖，这一块还不知道如何解决
1. 可添加读取 csv，xls，yml，txt 等文件的工具类方便读取数据
2. 可将浏览器驱动添加齐全，之后在 assembler.py 装配器中把驱动初始化代码补充完全
3. 连接 oracle,sqlserver,mongoDB 等多种类型数据库的拓展实现
4. log_tool.py 和 config_reader.py 和 screenshot_tool 三个工具类和 assembler.py 装配器中使用 os 获取项目路径的方式不是很友好（因为如果改动项目文件结构有可能导致文件找不到的错误），虽然目前结构是正常实现
5. 对于邮件的发送工具类我建议小伙伴无需添加，可以自行将项目集成到 jenkins 等其他 ci/cd 平台自动构建，自动发送邮件
6. 可以考虑修改 config.ini 中的路径参数，不用每个路径后必添 "/"，可以做成更智能化，同时注意使用到这几个路径参数的工具类代码也需要修改
7. 框架中所有模块包括工具类中基本全是采用纯粹面向对象的思路，只要是参数都放在了类里头，面向对象的情结太严重了`(*/ω＼*)`，正因为没有对象所以才情结那么深...

# 6.其他
- 框架作者：**abcnull**
- csdn 博客：**https://blog.csdn.net/abcnull**
- github：**https://github.com/abcnull**