#!/usr/bin/env python3
"""
安装/卸载「使用MPV批量播放」右键菜单项
需要以管理员权限运行

安装两种右键菜单：
1. 文件夹右键菜单（在文件夹上右键）
2. 文件夹内空白处右键菜单（在文件夹内空白处右键）
"""

import sys
import ctypes
import winreg
from pathlib import Path


SCRIPT_PATH = Path(__file__).parent / "mpv_batch_play.py"
MENU_NAME = "使用MPV批量播放"
REG_KEY_DIRECTORY = r"Directory\shell\MPVBatchPlay"
REG_KEY_BACKGROUND = r"Directory\Background\shell\MPVBatchPlay"


def is_admin() -> bool:
    """检查是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    """请求管理员权限重新运行"""
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join([f'"{arg}"' for arg in sys.argv]), None, 1
    )


def get_python_path() -> str:
    """获取Python解释器路径"""
    return sys.executable


def install_context_menu(key_path: str, description: str) -> bool:
    """安装指定位置的右键菜单"""
    python_path = get_python_path()
    script_path = str(SCRIPT_PATH.resolve())

    try:
        # 创建主菜单项
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path)
        winreg.SetValue(key, "", winreg.REG_SZ, MENU_NAME)
        winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, "shell32.dll,23")  # 播放图标
        winreg.CloseKey(key)

        # 创建命令
        command_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path + r"\command")
        command = f'"{python_path}" "{script_path}" "%V"'
        winreg.SetValue(command_key, "", winreg.REG_SZ, command)
        winreg.CloseKey(command_key)

        print(f"✓ {description} 已安装")
        return True

    except Exception as e:
        print(f"✗ {description} 安装失败: {e}")
        return False


def uninstall_context_menu(key_path: str, description: str) -> bool:
    """卸载指定位置的右键菜单"""
    try:
        # 删除命令子键
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path + r"\command")
        except FileNotFoundError:
            pass

        # 删除主键
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path)
        except FileNotFoundError:
            pass

        print(f"✓ {description} 已卸载")
        return True

    except Exception as e:
        print(f"✗ {description} 卸载失败: {e}")
        return False


def install_all_menus() -> bool:
    """安装所有右键菜单"""
    print("正在安装右键菜单...")
    print()

    if not SCRIPT_PATH.exists():
        print(f"✗ 错误: 找不到主脚本 {SCRIPT_PATH}")
        return False

    success = True

    # 安装文件夹右键菜单
    if not install_context_menu(REG_KEY_DIRECTORY, "文件夹右键菜单"):
        success = False

    # 安装文件夹背景右键菜单
    if not install_context_menu(REG_KEY_BACKGROUND, "文件夹内空白处右键菜单"):
        success = False

    if success:
        print("\n✓ 所有右键菜单已安装")
        print("\n现在你可以：")
        print("  1. 右键点击任意文件夹，选择「使用MPV批量播放」")
        print("  2. 在文件夹内空白处右键，选择「使用MPV批量播放」")
        print("\nMPV 将自动播放该文件夹内的所有文件")

    return success


def uninstall_all_menus() -> bool:
    """卸载所有右键菜单"""
    print("正在卸载右键菜单...")
    print()

    success = True

    # 卸载文件夹右键菜单
    if not uninstall_context_menu(REG_KEY_DIRECTORY, "文件夹右键菜单"):
        success = False

    # 卸载文件夹背景右键菜单
    if not uninstall_context_menu(REG_KEY_BACKGROUND, "文件夹内空白处右键菜单"):
        success = False

    if success:
        print("\n✓ 所有右键菜单已卸载")

    return success


def main():
    print("=" * 50)
    print("  MPV批量播放 - 右键菜单安装程序")
    print("=" * 50)
    print()

    # 检查管理员权限
    if not is_admin():
        print("需要管理员权限，正在请求...")
        run_as_admin()
        sys.exit(0)

    print("请选择操作:")
    print("  1. 安装右键菜单")
    print("  2. 卸载右键菜单")
    print("  0. 退出")
    print()

    choice = input("请输入选项 [1/2/0]: ").strip()

    if choice == "1":
        install_all_menus()
    elif choice == "2":
        uninstall_all_menus()
    elif choice == "0":
        print("已退出")
    else:
        print("无效选项")

    print()
    input("按回车键退出...")


if __name__ == '__main__':
    main()
