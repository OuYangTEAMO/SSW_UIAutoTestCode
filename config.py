# 这是配置文件，放4个平台的登录信息

import datetime
import random
from pathlib import Path

PLATFORMS = {
    "provider": { # 提供方连接器
        "url": "https://providernet.mayishangshu.cn:82/",
        "username": "18277778800",
        "password": "654321"
    },
    "user": { # 使用方连接器
            "url": "https://usernet.mayishangshu.cn:82/",
            "username": "18277778811",
            "password": "654321"
        },
    "operator": { # 运营方服务平台
        "url": "https://tds.mayishangshu.cn:82/",
        "username": "Presenter",
        "password": "0000"
    },
    "delivery": { # 交付平台
        "url": "https://dos.mayishangshu.cn:82/",
        "username": "18277778811",
        "password": "654321"
    }
}

# 生成基础字符串：MySQL_MMDD_随机4位数
today = datetime.datetime.now().strftime("%m%d")
rand_num = random.randint(1000, 9999)
base = f"MySQL_{today}_{rand_num}"

TEST_DATA = {
    "datasource_name": f"Auto_{base}", # 数据源名称
    "resource_name": f"Auto_Resource_{base}", # 数据资源名称
    "price": f"{random.randint(1, 10000)}" # 产品价格
}

# 上传文件路径
# 项目根目录
PROJECT_ROOT = Path(__file__).parent
# 资源文件目录
RESOURCES_DIR = PROJECT_ROOT / "resources"
# 具体文件路径
SAMPLE_FILE = RESOURCES_DIR / "样例表.xlsx"
COVER_IMAGE = RESOURCES_DIR / "cover.jpg"


# 这个箱子用来在多个脚本之间传递数据（比如存数据源名称）
global_data = {}