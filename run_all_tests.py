import pytest
import sys

if __name__ == "__main__":
    test_files = [
        "tests/test_01_provider.py",
        "tests/test_02_operator.py",
        "tests/test_03_user.py",
        "tests/test_04_operator_pay.py",
        "tests/test_05_user_sign.py",
        "tests/test_06_provider_sign.py"
    ]

    print("🚀 开始执行全流程自动化测试...")

    agrs = ["-v", "--tb=short"] + test_files
    exit_code = pytest.main(agrs)

    if exit_code == 0:
        print("🎉 全流程自动化测试完成，所有测试通过！")
    else:
        print("❌ 测试执行失败！")

    sys.exit(exit_code)
