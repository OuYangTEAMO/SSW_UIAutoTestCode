import pytest
import sys

if __name__ == "__main__":
# 按顺序执行所有测试文件
    test_files = [
        "test_01_provider.py",
        "test_02_operator.py",
        "test_03_user.py",
        "test_04_operator_pay.py",
        "test_05_user_sign.py",
        "test_06_provider_sign.py"
    ]

    print("🚀 开始执行全流程自动化测试...")

    # 使用 pytest.main 在同一个进程中运行所有文件
    # 这样 config.py 只会被导入一次，TEST_DATA 中的随机数保持一致
    agrs = ["-v", "--tb=short"] + test_files
    exit_code = pytest.main(agrs)

    if exit_code == 0:
        print("🎉 全流程自动化测试完成，所有测试通过！")
    else:
        print("❌ 测试执行失败！")

    sys.exit(exit_code)