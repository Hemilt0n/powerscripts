#!/usr/bin/env python3
"""
使用 MPV 批量播放文件夹内所有文件

用法：
    python mpv_batch_play.py [folder_path]

如果不提供参数，则播放当前目录下的所有文件
"""

import os
import sys
import subprocess
from pathlib import Path


def batch_play_with_mpv(folder_path: Path = None) -> bool:
    """
    使用 MPV 播放文件夹内的所有文件

    Args:
        folder_path: 要播放的文件夹路径，如果为 None 则使用当前目录

    Returns:
        bool: 成功返回True，失败返回False
    """
    if folder_path is None:
        folder_path = Path.cwd()

    if not folder_path.is_dir():
        print(f"错误: {folder_path} 不是文件夹")
        return False

    try:
        print(f"正在播放: {folder_path}")
        print(f"包含文件: {len(list(folder_path.iterdir()))} 个")
        print("按 'q' 停止播放，'<' 和 '>' 导航，空格暂停/继续")
        print("-" * 50)

        # 切换到目标目录并运行 mpv *
        os.chdir(folder_path)

        # 执行 mpv 命令，使用通配符播放所有文件
        # 不捕获输出，让 MPV 原生信息直接显示在终端
        result = subprocess.run(['mpv', '*'],
                              shell=True)  # 需要 shell 来展开通配符

        if result.returncode != 0:
            print(f"MPV 退出代码: {result.returncode}")
            return False

        return True

    except FileNotFoundError:
        print("错误: 未找到 mpv 播放器")
        print("请确保 MPV 已安装并添加到 PATH 环境变量")
        print("下载地址: https://mpv.io/installation/")
        return False
    except Exception as e:
        print(f"播放失败: {e}")
        return False


def main():
    if len(sys.argv) > 2:
        print("用法: python mpv_batch_play.py [folder_path]")
        print("请拖放文件夹到此脚本上，或通过右键菜单调用")
        input("按回车键退出...")
        sys.exit(1)

    folder_path = None
    if len(sys.argv) == 2:
        folder_path = Path(sys.argv[1])
        if not folder_path.is_dir():
            print(f"错误: {folder_path} 不是文件夹")
            input("按回车键退出...")
            sys.exit(1)

    print("=" * 50)
    print("  MPV 批量播放器")
    print("=" * 50)
    print()

    if batch_play_with_mpv(folder_path):
        print("\n播放完成")
    else:
        print("\n播放失败")

    # 如果是双击运行，暂停让用户看到结果
    if os.environ.get('PROMPT'):
        input("按回车键退出...")


if __name__ == '__main__':
    main()
