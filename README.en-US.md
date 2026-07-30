

**[English](https://github.com/abcnull/python-ui-auto-test/blob/master/README_en.md) | [Blog](https://blog.csdn.net/abcnull/article/details/103379143)**

[TOC]
# python-ui-auto-test

python + selenium + unittest + PO + BeautifulReport + redis + mysql + ParamUnittest + Multi-threading + Screenshots/Logs + Multi-browser Support + RemoteWebDriver + File Reading + Fully Parameterized Configuration

Welcome to **Watch**, **Star**, and **Fork** this repository!

- Framework Author: **abcnull**
- CSDN Blog: **https://blog.csdn.net/abcnull**
- GitHub: **https://github.com/abcnull**
- Email: **abcnull@qq.com**

## Framework Structure

```
python-ui-auto-test
    - api-test (API test package, no content added yet)
    - ui-test (UI test package)
        - base (Related to project initialization configuration)
        - case (Test case scripts)
        - common (Shared methods)
        - data (Data-driven)
        - locator (Element locators for pages)
        - page (Page classes)
        - report (Output reports)
            - html (HTML type reports)
            - log (Log reports)
            - img (Test screenshots)
        - resource (Resource folder)
            - config (Configuration files)
            - driver (Drivers)
        - util (Utility classes)
        - README.md (Project introduction markdown)
        - requirements.txt (Project dependency list)
        - run_all.py (Similar to TestNG suite runner, single-threaded)
        - run_all_mutithread.py (Similar to TestNG suite runner, multi-threaded)
    - venv (Virtual environment folder, needs to be created manually after cloning from GitHub)
    - .gitignore (Git ignore file)
External Libraries
Scratches and Consoles
```

![Framework Structure](https://github.com/abcnull/Image-Resources/blob/master/python-ui-auto-test/1575304456217.png)


## Framework Overview

- Adopts the Page Object (PO) design pattern, further refining `PageObject`. Element locators and page-specific data are placed separately in `locator` and `data` directories, while `case` stores the test scripts.

- `common` contains `PageCommon` and `BrowserCommon`, which encapsulate page operations and browser operations respectively.

- `base` contains the `Assembler` configurator for initializing the database and drivers, used to create initial configurations at the beginning of test cases. The source code for its `__init__(self)` method is shown below:

  ```python
  # Initialize all tools
      def __init__(self):
          # Assemble driver
          self.assemble_driver()
          # Assemble Redis tool
          if ConfigReader().read("project")["redis_enable"].upper() == "Y":
              # Assemble Redis connection pool tool
              self.assemble_redis()
          elif ConfigReader().read("project")["redis_enable"].upper() == "N":
              self.redis_pool_tool = None
          else:
              self.redis_pool_tool = None
              raise RuntimeError("Incorrect configuration for Redis enable field in config file! Please fix!")
          # Assemble MySQL tool
          if ConfigReader().read("project")["mysql_enable"].upper() == "Y":
              # Assemble MySQL tool
              self.assemble_mysql()
          elif ConfigReader().read("project")["mysql_enable"].upper() == "N":
              self.mysql_tool = None
          else:
              self.mysql_tool = None
              raise RuntimeError("Incorrect configuration for MySQL enable field in config file! Please fix!")
          # Save the assembler to thread local storage, with thread as key and assembler object as value
          ThreadLocalStorage.set(threading.current_thread(), self)
  ```

- `report` stores HTML test reports, log files, and screenshots. The test report uses the BeautifulReport template. Log output can be fully parameterized via `util/config/config.ini`. Screenshots were originally stored in `img` under the project due to BeautifulReport limitations, but are now placed here using `../`. Firefox driver logs generated in test cases are also moved to this `log` folder using `../`. HTML reports and screenshots can be configured to allow or disallow overwriting existing files. Logs are configured with a maximum rotation of 5. Taking HTML as an example, duplicate names can be handled by generating a new report name using recursion. The source code is as follows:

  ```python
  # Recursive method
      # Check if the report name duplicates in the configured path, and return a new name based on the overwrite configuration
      def get_html_name(self, filename: str = None, report_dir="."):
          """
          Get a new report name
          :param filename: Report name
          :param report_dir: Report path
          :return: Determines if the report can be overwritten based on configuration, returns a new report name
          """
          # If overwriting duplicate report names is allowed
          if ConfigReader().read("html")["cover_allowed"].upper() == "Y":
              # Return report name
              return filename
          # If overwriting duplicate report names is not allowed
          elif ConfigReader().read("html")["cover_allowed"].upper() == "N":
              # Check if the report path exists
              if os.path.exists(report_dir + filename + ".html"):
                  # If the name does not end with ")"
                  if not filename.endswith(")"):
                      filename = filename + "(2)"
                  # If the name ends with ")"
                  else:
                      file_num = filename[filename.index("(") + 1: -1]
                      num = int(file_num)
                      # Increment report name field
                      num += 1
                      filename = filename[:filename.index("(")] + "(" + str(num) + ")"
              # If report does not exist
              else:
                  # Recursive exit, run test and generate report for storage
                  return filename
              # Recursion: keep changing filename until no duplicate is found
              return self.get_html_name(filename, report_dir)
          # Raise exception if configuration is neither Y/y nor N/n
          else:
              raise RuntimeError("Incorrect configuration for cover_allowed field in [html] section of config.ini. Please check!")
  ```

- The `config` in the resource folder enables the project to be fully configured and run via parameters. The `driver` folder currently contains all mainstream drivers. Version information is documented in `config.ini`.

  ![Framework Overview](https://github.com/abcnull/Image-Resources/blob/master/python-ui-auto-test/1575305550583.png)

- Utility classes include: configuration file reader, log tool, MySQL connection tool, Redis connection pool tool, report generation tool, screenshot tool, text tool, and thread-local storage tool.
- `run_all.py` can run all test cases in a single thread, while `run_all_mutithread` runs them in multiple threads. Note that multi-threaded execution does not consolidate reports into a single report; this requires secondary development on BeautifulReport.

## Hierarchical Structure Design

The framework adopts the popular Page Object (PO) design pattern for a clearer structure. Logical code can be maintained in the `page` folder, business workflow organization in `case`, and changes in `data` or `locator` can be quickly tracked and modified. `base` stores initialization tools, and `common` stores shared methods. As for how test cases are organized and executed, see the following approaches:

- A test class in a `case` file contains multiple methods prefixed with `test`. These methods initialize the Assembler (which contains a driver) via the `setUp()` method. Each `test`-prefixed method represents a test point, and opening a test point is equivalent to using a new Assembler with its driver. A `test`-prefixed method can represent a complete workflow.
- If you prefer not to use `setUp()`, you can manually write a dedicated method inside a specific `test`-prefixed method. This prevents every test from running that method.
- The framework includes a highly useful feature. For example, when testing e-commerce systems like Taobao or Tmall, which consist of product pages, shopping cart pages, checkout pages, etc., after writing page objects for each, and testing specific functional points in `case`, how can multiple cases be chained together? Since the driver is saved in a static dictionary linked to the thread ID after creation in the Assembler, you can directly retrieve the driver from another case based on the current thread and continue from where the previous case left off.
- Other case organization methods: Thanks to the `ParamUnittest` tool, the Assembler (containing the driver) can be placed specifically in the class-level dictionary parameters of the test class, allowing each test method in that class to directly access it. This approach also works well for organizing complete workflows within a class. There are many other ways to organize cases. Thanks to `ParamUnittest` external parameter passing, thread-local storage, and fully parameterized configuration via `config.ini`, case organization is highly flexible and can be slightly modified or extended based on specific project requirements.

## Assembler Configurator

Key features include:

- Initialization of various driver types
- Redis configuration/assembly
- MySQL configuration/assembly
- Saves this Assembler object and the local thread to a static dictionary for easy driver access in other cases

## ParamUnittest External Parameter Passing

Since the testing environment could be SIT, UAT, or PROD, parameters can be passed to test methods within case classes by modifying values in `config.ini`. Developers can also consider secondary development to pass parameters directly into specific cases within `run_all.py`. Another parameter is the language parameter; in multi-language environments, modifying this parameter allows selecting specific data from `data`. Of course, developers can add their own required parameters based on project needs.

![ParamUnittest External Parameter Passing](https://github.com/abcnull/Image-Resources/blob/master/python-ui-auto-test/1575369275406.png)

## config.ini Project Configuration

Contains the following sections:

- `[project]` Project configuration, such as custom parameters, driver type, remote server IP, whether Redis/MySQL is enabled, etc.
- `[driver]` Paths for almost all mainstream browser drivers
- `[redis]` Various Redis configurations
- `[mysql]` Various MySQL configurations
- `[screenshot]` Screenshot path, format, and whether overwriting is supported
- `[html]` Includes report name, storage path, and whether overwriting is supported
- `[log]` Contains extensive log configurations; please refer to the file for details

Developers can later add configuration parameters for Oracle, SQL Server, MongoDB, etc. Remember to also add corresponding code to the Assembler.

![config.ini Project Configuration](https://github.com/abcnull/Image-Resources/blob/master/python-ui-auto-test/1575369314016.png)

## Utility Classes

- `ConfigReader`: Configuration file reader for project parameterized configuration
- `LogTool`: Log utility class
- `MysqlTool`: MySQL connection tool that returns a successful MySQL connection
- `RedisPool`: Redis connection pool tool, containing the connection pool object and a connection from the pool
- `ReportTool`: Report generation tool that wraps BeautifulReport, allowing configuration-based handling of duplicate file overwriting
- `ScreenshotTool`: Screenshot utility
- `TextTool`: Text utility for simple text generation
- `ThreadLocalStorage`: Used to store the thread ID and Assembler object as key-value pairs in a static dictionary, facilitating driver access across different cases

  ![Utility Classes](https://github.com/abcnull/Image-Resources/blob/master/python-ui-auto-test/1575369333647.png)

## Conclusion

The project still has many areas for improvement and optimization. Valuable feedback via commits is welcome to further enhance the framework!
Thank you again!

- Framework Author: **abcnull**
- CSDN Blog: **https://blog.csdn.net/abcnull**
- GitHub: **https://github.com/abcnull**
- Email: **abcnull@qq.com**
