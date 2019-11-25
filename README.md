[toc]

python + selenium + unittest

# 框架注意点！
- ui-test/case 中存放测试用例，测试用例的`.py`文件需要以`test`打头
- ui-test/page 中存放 PO 对象，PO 对象中的测试点方法名需要以`test`开头，并且通过下划线加数字形式进行执行排序
- ui-test/resource/driver 中的谷歌驱动对应浏览器 77 版本的，对于 78 及以上版本的浏览器还需要小伙伴们自行更新驱动文件
- 学习过 testng 的人知道可以利用 testng 的注解来调整驱动的执行时期，unittest 一般把驱动初始化放在 setUp 方法中（类似 @BeforeTest），放在 test 打头的方法貌似是不行的，因为 unittest.main() 每执行一个 test 方法实际上是新创一个实例对象
- 此项目中已将 api-test 和 ui-test 设置成包文件夹，虽然 api-test 包中为空
- case 包中有时候 before_setUp() 和 after_tearDown() 方法存在是有必要的，因为并不是每一个测试方法需要 setUp() 执行在前，有的可能只需要 before_setUp() 执行在前，after_SetUp() 也是一样的道理

# 所需依赖
```
selenium 3.141.0
urllib3 1.25.7
```

# 项目结构
```
python-ui-auto-test
    - data（项目中的数据）
    - resource（项目下的资源文件夹）
        - driver（存放各个浏览器驱动）
    - ui-test（ui 测试包）
        - base（与驱动启动相关的类）
        - case（测试用例脚本）
        - common（共用方法）
        - data（数据驱动）
        - listener（监听器）
        - locator（页面对应的元素定位）
        - page（页面类）
        - resource（资源文件夹）
        - util（工具类）
    - util（项目使用的工具类）
    - venv（虚拟环境的文件夹）
    - execute.py（类似于 testng 文件执行测试套）
    - README.md（项目介绍 md）
External Libraries
Scratches and Consoles
```
# 该项目缺少
1. 报告或者 beautifulReport 报告
2. log 日志信息
3. 截图
4. 多线程考虑
5. 连接服务器配置相关
6. 多语言考虑
7. 一些信息对配置文件的读取
8. 考虑数据驱动有没有必要做到 excel 读取
9. 对于 @BeforeClass 该怎么办，该放哪？
10. 进行各种浏览器的识别
11. 使用 redis 存取值
12. 连接 mysql 操作