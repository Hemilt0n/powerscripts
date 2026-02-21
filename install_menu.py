#!/usr/bin/env python3
"""
安装/卸载右键菜单项
需要以管理员权限运行
"""

import os
import sys
import winreg
from pathlib import Path


SCRIPT_PATH = Path(__file__).parent / "folders_to_cbz.py"
MENU_NAME = "转换为CBZ"
REG_KEY_PATH = r"Directory\shell\FoldersToCBZ"


def get_python_path() -> str:
    """获取Python解释器路径"""
    return sys.executable


def install_context_menu():
    """安装右键菜单"""
    python_path = get_python_path()
    script_path = str(SCRIPT_PATH.resolve())

    try:
        # 创建主菜单项
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, REG_KEY_PATH)
        winreg.SetValue(key, "", winreg.REG_SZ, MENU_NAME)
        winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, "shell32.dll,45")
        winreg.CloseKey(key)

        # 创建命令
        command_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, REG_KEY_PATH + r"\command")
        command = f'"{python_path}" "{script_path}" "%V"'
        winreg.SetValue(command_key, "", winreg.REG_SZ, command)
        winreg.CloseKey(command_key)

        print("✓ 右键菜单已安装")
        print(f"  Python路径: {python_path}")
        print(f"  脚本路径: {script_path}")
        print("\n现在右键点击任意文件夹，即可看到「转换为CBZ」选项")

    except PermissionError:
        print("✗ 错误: 需要管理员权限")
        print("  请右键点击此脚本，选择「以管理员身份运行」")
        return False
    except Exception as e:
        print(f"✗ 安装失败: {e}")
        return False

    return True


def uninstall_context_menu():
    """卸载右键菜单"""
    try:
        # 删除命令子键
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, REG_KEY_PATH + r"\command")
        except FileNotFoundError:
            pass

        # 删除主键
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, REG_KEY_PATH)
        except FileNotFoundError:
            pass

        print("✓ 右键菜单已卸载")

    except PermissionError:
        print("✗ 错误: 需要管理员权限")
        return False
    except Exception as e:
        print(f"✗ 卸载失败: {e}")
        return False

    return True


def main():
    print("=" * 50)
    print("  文件夹转CBZ - 右键菜单安装程序")
    print("=" * 50)
    print()

    if not SCRIPT_PATH.exists():
        print(f"✗ 错误: 找不到主脚本 {SCRIPT_PATH}")
        input("按回车键退出...")
        sys.exit(1)

    print("请选择操作:")
    print("  1. 安装右键菜单")
    print("  2. 卸载右键菜单")
    print("  0. 退出")
    print()

    choice = input("请输入选项 [1/2/0]: ").strip()

    if choice == "1":
        install_context_menu()
    elif choice == "2":
        uninstall_context_menu()
    elif choice == "0":
        print("已退出")
    else:
        print("无效选项")

    print()
    input("按回车键退出...")


if __name__ == '__main__':
    main()
