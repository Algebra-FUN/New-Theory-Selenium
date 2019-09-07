# 新理论答题测试辅助
## 开发背景

由于该项目的特殊性，开发测试任务量与一般的项目相比较大；为了节省测试时间，故而开发此程序

## 使用说明

### 运行环境

python3 version>=3.5 

### 安装依赖

> 请同时安装python2&python3的用户，使用pip3,python3代替下面命令

##### STEP 0: clone本项目源码

##### STEP 1: 安装模组

```shell
pip install selenium
pip install xlrd
```

##### STEP 2: 安装webdriver

下载chromedriver.exe,存放在Python目录下
> 也可以按照的主流网络教程进行安装在Chrome目录下

##### STEP 3: 启动

```shell
python main.py
```

### 配置
#### 使用非Chrome,配置webdriver
在 main.py 文件中可根据需求 自行修改代码
```python
# 可根据需求更换webdriver,如IE,Edge,Firefox等
browser = webdriver.Chrome()
```
#### 资源初始配置
##### 通过 config.ini
在 config.ini 文件中 直接配置
```ini
[website]
# 测试目标网站URL
url = localhost:8000
[excel]
# 测试用例Excel文件PATH
path = ./lib_sheet.xls
```
##### 通过 内置command
```shell
reset --website_url <url>
reset --sheet_path <path>
```

### 开始使用

##### 填充

```shell
fill --questions
```

### 常见问题

##### Excel文件路径

excel_path是相对于main.py的启动路径
可以通过reset命令更换excel源文件

```shell
reset --sheet_path <path_to_excel>
```

## 免责声明

本程序仅用于开发测试；若使用在其他领域，责任由使用者承担，作者概不负责

## LICENSE

[![LICENSE](https://img.shields.io/badge/license-Anti%20996-blue.svg)](https://github.com/996icu/996.ICU/blob/master/LICENSE)

