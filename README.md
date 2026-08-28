# SSW_UIAutoTestCode

基于 Playwright + pytest 的 UI 自动化测试框架，应用于**蚂蚁树数据交易平台**的全流程端到端测试。

## 项目概述

本项目覆盖数据交易平台的四大角色：**提供方**、**使用方**、**运营方**、**交付方**，通过 Playwright 模拟浏览器操作，自动化执行从资源发布到签约交付的完整业务流程。

## 测试流程

```
┌─────────────────────────────────────────────────────────────────┐
│                      数据交易全流程测试                            │
├───────────────┬───────────────┬───────────────┬─────────────────┤
│   提供方       │   运营方       │   使用方       │   提供方/使用方   │
│ (Provider)    │ (Operator)    │   (User)      │   (签约)         │
├───────────────┼───────────────┼───────────────┼─────────────────┤
│ 1. 创建数据源  │ 2. 审批上架    │ 3. 购买资源    │ 5-6. 双方签约    │
│ 1. 创建数据资源 │               │               │                 │
│ 1. 发布资源    │               │ 4. 运营方审批  │                 │
│               │               │   支付订单     │                 │
└───────────────┴───────────────┴───────────────┴─────────────────┘
```

## 目录结构

```
SSW_UIAutoTestCode/
├── config.py              # 配置文件（平台账号、测试数据）
├── run_all_tests.py       # 一键运行所有测试的入口
│
├── pages/                 # 页面对象模型（Page Object）
│   ├── __init__.py
│   ├── base_page.py       # 基类：封装 Playwright 公共操作
│   ├── provider_page.py   # 提供方平台页面操作
│   ├── user_page.py       # 使用方平台页面操作
│   └── operator_page.py   # 运营方平台页面操作
│
├── tests/                 # 测试用例（使用 Page Object 模式）
│   ├── __init__.py
│   ├── test_01_provider.py     # 提供方：数据源/资源创建与发布
│   ├── test_02_operator.py     # 运营方：资源上架审批
│   ├── test_03_user.py         # 使用方：购买数据资源
│   ├── test_04_operator_pay.py # 运营方：交易订单审批
│   ├── test_05_user_sign.py    # 使用方：签约确认
│   └── test_06_provider_sign.py # 提供方：签约确认
│
├── legacy/                # 旧测试文件（原封不动，仅作备份）
│   └── test_*.py
│
├── resources/             # 测试资源文件（封面图、样例表）
└── videos/                # Playwright 录屏输出目录
```

## 架构说明

本项目采用 **Page Object（页面对象）模式**，将页面定位器和页面操作与测试逻辑分离：

- **pages/** — 封装页面元素定位和操作方法，供 tests/ 调用
- **tests/** — 测试逻辑，简洁地调用 pages 中的方法
- **legacy/** — 旧版测试文件，未经重构，保持原样

这样做的好处是：当页面 UI 变更时，只需修改 pages/ 中的代码，无需改动 tests/ 中的测试逻辑。

## 依赖

| 依赖 | 版本 | 说明 |
|------|------|------|
| Python | ≥ 3.9 | 推荐 3.11 |
| pytest | 8.4.2 | 测试框架 |
| playwright | 1.58.0 | 浏览器自动化 |

## 安装

```bash
# 1. 安装 Python 依赖
pip install pytest==8.4.2 playwright==1.58.0

# 2. 安装浏览器（仅需 Chromium）
playwright install chromium
```

## 运行

### 运行全部测试
```bash
python run_all_tests.py
```

### 运行单个测试文件
```bash
pytest -v tests/test_01_provider.py
```

### 按顺序运行所有测试
```bash
pytest -v --tb=short tests/test_01_provider.py tests/test_02_operator.py tests/test_03_user.py tests/test_04_operator_pay.py tests/test_05_user_sign.py tests/test_06_provider_sign.py
```

## 配置说明

`config.py` 中包含四类平台的登录信息：

| 平台 | 角色 | 用途 |
|------|------|------|
| provider | 提供方 | 创建、发布数据资源 |
| user | 使用方 | 购买资源、签约 |
| operator | 运营方 | 审批资源上架、审批支付 |
| delivery | 交付方 | 交付相关操作 |

**测试数据**通过随机生成实现隔离：
- 数据源名称：`Auto_{MySQL_MMDD_XXXX}`
- 数据资源名称：`Auto_Resource_{MySQL_MMDD_XXXX}`
- 价格：随机 1-10000

## 平台账号

> ⚠️ **注意**：生产环境请使用环境变量替代明文密码。

| 平台 | 用户名 | 密码 |
|------|--------|------|
| 提供方 | 18277778800 | 654321 |
| 使用方 | 18277778811 | 654321 |
| 运营方 | Presenter | 0000 |
| 交付方 | 18277778811 | 654321 |

## 测试类说明

### TestProvider (`tests/test_01_provider.py`)
- 登录提供方平台
- 创建 MySQL 数据源（IP: 192.168.1.15, Port: 1966）
- 创建数据资源，配置脱敏规则（tel 字段掩码）
- 上传样例表文件
- 发布数据资源（一口价定价，数据服务交付方式）
- 启用资源发布

### TestOperator (`tests/test_02_operator.py`)
- 登录运营方平台
- 进入待办事项
- 审批数据资源上架

### TestUser (`tests/test_03_user.py`)
- 登录使用方平台
- 进入数据资源目录
- 购买目标资源
- 获取订单编号并保存（供后续测试使用）

### TestOperatorPay (`tests/test_04_operator_pay.py`)
- 登录运营方平台
- 审批交易订单

### TestUserSign (`tests/test_05_user_sign.py`)
- 登录使用方平台
- 对订单进行签约确认

### TestProviderSign (`tests/test_06_provider_sign.py`)
- 登录提供方平台
- 对订单进行签约确认

## Jenkins 集成

创建 `Jenkinsfile`：

```groovy
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/OuYangTEAMO/SSW_UIAutoTestCode.git'
            }
        }

        stage('Install') {
            steps {
                bat 'pip install -r requirements.txt'
                bat 'playwright install chromium'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python run_all_tests.py'
            }
        }
    }

    post {
        always {
            junit '**/test-results/*.xml'
            archiveArtifacts 'videos/**'
        }
    }
}
```

建议添加 `requirements.txt`：
```
pytest==8.4.2
playwright==1.58.0
```

## 注意事项

1. **执行顺序**：测试依赖执行顺序，请确保按 01 → 02 → 03 → 04 → 05 → 06 的顺序运行
2. **视频录制**：Playwright 默认录制测试视频，存于 `videos/` 目录
3. **数据隔离**：每次运行的资源名称不同（带随机后缀），避免数据污染
4. **截图配置**：如需失败截图，可在 Playwright context 中配置
