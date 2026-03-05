#!/usr/bin/env python3
"""
安装/卸载「截取视频片段」右键菜单项
需要以管理员权限运行

支持常见视频格式：mp4, mkv, avi, mov, wmv, flv, webm
"""

import sys
import ctypes
import winreg
from pathlib import Path


SCRIPT_PATH = Path(__file__).parent / "video_cut.py"
MENU_NAME = "截取视频片段"

# 支持的视频格式
VIDEO_EXTENSIONS = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg']


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


def install_context_menu() -> bool:
    """安装视频文件右键菜单"""
    python_path = get_python_path()
    script_path = str(SCRIPT_PATH.resolve())

    if not SCRIPT_PATH.exists():
        print(f"✗ 错误: 找不到主脚本 {SCRIPT_PATH}")
        return False

    success_count = 0
    fail_count = 0

    print("正在安装右键菜单...")
    print()

    for ext in VIDEO_EXTENSIONS:
        reg_key = f"SystemFileAssociations\\{ext}\\shell\\VideoCut"

        try:
            # 创建主菜单项
            key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, reg_key)
            winreg.SetValue(key, "", winreg.REG_SZ, MENU_NAME)
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, "shell32.dll,100")  # 视频图标
            winreg.CloseKey(key)

            # 创建命令
            command_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, reg_key + r"\command")
            command = f'"{python_path}" "{script_path}" "%1"'
            winreg.SetValue(command_key, "", winreg.REG_SZ, command)
            winreg.CloseKey(command_key)

            print(f"✓ {ext} 右键菜单已安装")
            success_count += 1

        except Exception as e:
            print(f"✗ {ext} 安装失败: {e}")
            fail_count += 1

    print()
    print(f"安装完成: 成功 {success_count}, 失败 {fail_count}")
    print(f"\n现在右键点击视频文件，即可看到「{MENU_NAME}」选项")
    print("支持格式:", ", ".join(VIDEO_EXTENSIONS))

    return fail_count == 0


def uninstall_context_menu() -> bool:
    """卸载视频文件右键菜单"""
    success_count = 0
    fail_count = 0

    print("正在卸载右键菜单...")
    print()

    for ext in VIDEO_EXTENSIONS:
        reg_key = f"SystemFileAssociations\\{ext}\\shell\\VideoCut"

        try:
            # 删除命令子键
            try:
                winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, reg_key + r"\command")
            except FileNotFoundError:
                pass

            # 删除主键
            try:
                winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, reg_key)
            except FileNotFoundError:
                pass

            print(f"✓ {ext} 右键菜单已卸载")
            success_count += 1

        except Exception as e:
            print(f"✗ {ext} 卸载失败: {e}")
            fail_count += 1

    print()
    print(f"卸载完成: 成功 {success_count}, 失败 {fail_count}")

    return fail_count == 0


def main():
    print("=" * 50)
    print("  视频截取 - 右键菜单安装程序")
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