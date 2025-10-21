#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
UV 迁移验证脚本 / UV Migration Verification Script

此脚本验证 uv 迁移是否成功完成
This script verifies if the uv migration is successfully completed
"""

import sys
import importlib.util
from pathlib import Path


def check_python_version():
    """检查 Python 版本"""
    print("🔍 检查 Python 版本 / Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 11:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor}.{version.micro} (需要 >= 3.11)")
        return False


def check_file_exists(filepath, description):
    """检查文件是否存在"""
    path = Path(filepath)
    if path.exists():
        print(f"  ✅ {description}: {filepath}")
        return True
    else:
        print(f"  ❌ {description}: {filepath} (未找到)")
        return False


def check_module_import(module_name):
    """检查模块是否可以导入"""
    try:
        if importlib.util.find_spec(module_name) is not None:
            print(f"  ✅ 模块 {module_name} 可导入")
            return True
        else:
            print(f"  ❌ 模块 {module_name} 未安装")
            return False
    except Exception as e:
        print(f"  ❌ 模块 {module_name} 检查失败: {e}")
        return False


def main():
    """主验证函数"""
    print("=" * 60)
    print("🚀 UV 迁移验证开始 / UV Migration Verification Started")
    print("=" * 60)
    print()
    
    results = []
    
    # 1. 检查 Python 版本
    results.append(check_python_version())
    print()
    
    # 2. 检查配置文件
    print("📁 检查配置文件 / Checking configuration files...")
    results.append(check_file_exists("pyproject.toml", "项目配置"))
    results.append(check_file_exists(".python-version", "Python 版本文件"))
    results.append(check_file_exists(".gitignore", "Git 忽略文件"))
    print()
    
    # 3. 检查文档文件
    print("📚 检查文档文件 / Checking documentation files...")
    results.append(check_file_exists("UV_MIGRATION_GUIDE.md", "UV 迁移指南"))
    results.append(check_file_exists("QUICKSTART.md", "快速入门指南"))
    results.append(check_file_exists("MIGRATION_SUMMARY.md", "迁移总结"))
    results.append(check_file_exists("CHANGELOG_UV_MIGRATION.md", "变更日志"))
    results.append(check_file_exists("Makefile", "Makefile"))
    print()
    
    # 4. 检查核心模块
    print("📦 检查核心模块 / Checking core modules...")
    results.append(check_module_import("flask"))
    results.append(check_module_import("requests"))
    results.append(check_module_import("pydantic"))
    results.append(check_module_import("fastapi"))
    results.append(check_module_import("PIL"))
    results.append(check_module_import("numpy"))
    print()
    
    # 5. 检查项目模块
    print("🔧 检查项目模块 / Checking project modules...")
    sys.path.insert(0, str(Path.cwd()))
    results.append(check_module_import("pyJianYingDraft"))
    results.append(check_module_import("settings"))
    print()
    
    # 6. 检查向后兼容性文件
    print("🔄 检查向后兼容性 / Checking backward compatibility...")
    results.append(check_file_exists("requirements.txt", "传统依赖文件"))
    results.append(check_file_exists("requirements-mcp.txt", "MCP 依赖文件"))
    print()
    
    # 总结
    print("=" * 60)
    total = len(results)
    passed = sum(results)
    failed = total - passed
    
    print(f"📊 验证结果 / Verification Results:")
    print(f"  总计 / Total: {total}")
    print(f"  通过 / Passed: {passed} ✅")
    print(f"  失败 / Failed: {failed} ❌")
    print()
    
    if failed == 0:
        print("🎉 恭喜！UV 迁移验证全部通过！")
        print("🎉 Congratulations! All UV migration verifications passed!")
        print()
        print("✨ 下一步 / Next Steps:")
        print("  1. 运行 'uv sync' 安装依赖")
        print("  2. 运行 'uv run capcut_server.py' 启动服务")
        print("  3. 查看 QUICKSTART.md 了解更多")
        return 0
    else:
        print("⚠️  部分验证未通过，请检查上述失败项")
        print("⚠️  Some verifications failed, please check the items above")
        return 1


if __name__ == "__main__":
    exit_code = main()
    print("=" * 60)
    sys.exit(exit_code)
