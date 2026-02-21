#!/usr/bin/env python3
"""
将文件夹内的全部内容提取到上级目录，然后删除该文件夹
用于减少不必要的目录层级

用法：
    python flatten_folder.py <folder1> [folder2] [folder3] ...
"""

import os
import sys
import shutil
from pathlib import Path


def flatten_folder(folder_path: Path) -> bool:
    """
    将文件夹内容移动到上级目录，然后删除该文件夹

    Args:
        folder_path: 要处理的文件夹路径

    Returns:
        bool: 成功返回True，失败返回False
    """
    if not folder_path.is_dir():
        print(f"跳过: {folder_path} 不是文件夹")
        return False

    parent_dir = folder_path.parent

    try:
        print(f"正在处理: {folder_path.name}")

        # 获取文件夹内所有内容
        items = list(folder_path.iterdir())

        if not items:
            print(f"  文件夹为空，直接删除")
            folder_path.rmdir()
            print(f"完成: {folder_path.name}")
            return True

        # 移动所有内容到上级目录
        for item in items:
            dest = parent_dir / item.name

            # 处理同名冲突
            if dest.exists():
                # 添加原文件夹名作为前缀
                new_name = f"{folder_path.name}_{item.name}"
                dest = parent_dir / new_name
                print(f"  冲突: {item.name} -> {new_name}")

            shutil.move(str(item), str(dest))
            print(f"  移动: {item.name}")

        # 删除空文件夹
        folder_path.rmdir()

        print(f"完成: {folder_path.name}")
        return True

    except Exception as e:
        print(f"错误: 处理 {folder_path.name} 时失败 - {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("用法: python flatten_folder.py <folder1> [folder2] ...")
        print("请拖放文件夹到此脚本上，或通过右键菜单调用")
        input("按回车键退出...")
        sys.exit(1)

    folders = [Path(arg) for arg in sys.argv[1:]]

    success_count = 0
    fail_count = 0

    for folder in folders:
        if flatten_folder(folder):
            success_count += 1
        else:
            fail_count += 1

    print(f"\n处理完成: 成功 {success_count}, 失败 {fail_count}")

    # 如果是双击运行，暂停让用户看到结果
    if os.environ.get('PROMPT'):
        input("按回车键退出...")


if __name__ == '__main__':
    main()
