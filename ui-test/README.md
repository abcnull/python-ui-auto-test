[toc]

python + selenium + unittest + BeautifulReport + redis + mysql + ParamUnittest(外部传参) + tomorrow(多线程) + 本地线程存储 + img 截图 + log 日志 + 多浏览器支持 + ini 文件读取 + 全参数化构建  

# 1.框架注意点-使用前必看！
- 项目完全依靠参数化构建，见文件`ui-test/resource/config/config.ini`
- `ui-test/case`中存放测试用例，测试用例的`.py`文件需要以 test 打头
- `ui-test/page`中存放 PO 对象，PO 对象中的测试点方法名需要以 test 开头，并且通过下划线加数字形式进行执行排序
- `ui-test/resource/driver`中的谷歌驱动对应浏览器 77 版本的，对于 78 及以上版本的浏览器还需要小伙伴们自行更新驱动文件
- 此项目中已将`api-test`和`ui-test`设置成包文件夹，虽然`api-test`包中为空
- 此项目在我电脑中才用虚拟环境，所以在`.gitignore`中把`venv`文件取消了跟踪
- `ui-test`包中`/resource/config/config.ini`中的键名参数不能大写，以为读取`.ini`的键名必以小写读出！
- `ui-test`包中`/util/log_tool.py`中最下方请不要取消注释，除非`log_tool.py`模块去单独调试
- 项目名一定要是`python-ui-auto-test`，其下目录名或文件名不要使用同名，当 ci/cd 集成时其上目录名要不要使用此名，因为代码中根据此名寻找路径，同名文件寻找路径会出现异常
- 各测试点方法上的报告截图装饰器的参数需要固定这么写，因为路径原因，我也很无奈啊╮(╯▽╰)╭
- 建议用谷歌和火狐驱动，ie 似乎元素定位不到

# 2.所需依赖
本人使用的是 python 3.6
```
BeautifulReport 0.1.2
ParamUnittest   0.2
PyMySQL         0.9.3
futures         3.1.1
pip             10.0.1	
redis           3.3.11
selenium        3.141.0	
setuptools      39.1.0	
tomorrow        0.2.4	
urllib3         1.25.7	
```

# 3.项目结构
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

# 4.可以拓展补充的地方
1. 运行多线程`run_all_mutithread.py`，虽然确实实现了多线程，但报告中没有将多线程的用例联合起来，而是一个线程一个报告，应该可以通过对 BeautifulReport 进行二次开发或者对 unittest 二次开发，采用协程的方式可以解决
2. 可添加读取 csv，xls，yml，txt 等多种文件的工具类方便读取数据
3. 连接 oracle,sqlserver,mongoDB 等多种类型数据库的拓展实现
4. `log_tool.py`，`config_reader.py`，`screenshot_tool`，`assembler.py`中获取项目路径的方式不是很友好（因为如果改动项目文件结构有可能导致文件找不到的错误）。采用目前结构是正常实现，可以优化下路径获取方式
5. 对于邮件的发送工具类我建议小伙伴无需添加，可以自行将项目集成到 jenkins 等其他 ci/cd 平台自动构建，自动发送邮件
6. 可以考虑修改 config.ini 中的路径参数，不用每个路径后必添 "/"，也可智能识别路径，同时注意使用到这几个路径参数的工具类代码也需要修改
7. 可以通过配置让火狐浏览器不自动产生 log 日志，目前只把火狐自动产生的日志放在项目 ui-log 日志生成的地方
8. 配置文件中可添加浏览器版本信息，目前是没有这项参数的。之后再在 assembler 装载器中补全代码即可
9. 其他......

# 5.其他
搭建过程中非常感谢李鹏飞大侠的技术支持！后续有问题请在如下途径私聊联系！
- 框架作者：**abcnull**
- csdn 博客：**https://blog.csdn.net/abcnull**
- github：**https://github.com/abcnull**
- e-mail：**abcnull@qq.com**