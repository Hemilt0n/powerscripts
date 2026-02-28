#!/usr/bin/env python3
"""
将选中的文件夹压缩为CBZ格式（漫画书归档格式）
CBZ本质上是ZIP格式，仅修改扩展名

用法：
    python folders_to_cbz.py <folder_or_zip1> [folder_or_zip2] ...

支持：
    - 文件夹：压缩为CBZ并删除原文件夹
    - ZIP文件：直接重命名为CBZ
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path


def rename_zip_to_cbz(zip_path: Path) -> bool:
    """
    将ZIP文件重命名为CBZ文件

    Args:
        zip_path: 要重命名的ZIP文件路径

    Returns:
        bool: 成功返回True，失败返回False
    """
    if not zip_path.is_file():
        print(f"跳过: {zip_path} 不是文件")
        return False

    if zip_path.suffix.lower() != '.zip':
        print(f"跳过: {zip_path} 不是ZIP文件")
        return False

    cbz_path = zip_path.with_suffix('.cbz')

    # 检查目标文件是否已存在
    if cbz_path.exists():
        print(f"跳过: {cbz_path} 已存在")
        return False

    try:
        zip_path.rename(cbz_path)
        print(f"重命名: {zip_path.name} -> {cbz_path.name}")
        return True
    except Exception as e:
        print(f"错误: 重命名 {zip_path.name} 时失败 - {e}")
        return False


def create_cbz_from_folder(folder_path: Path) -> bool:
    """
    将文件夹压缩为CBZ文件并删除原文件夹

    Args:
        folder_path: 要压缩的文件夹路径

    Returns:
        bool: 成功返回True，失败返回False
    """
    if not folder_path.is_dir():
        print(f"跳过: {folder_path} 不是文件夹")
        return False

    cbz_path = folder_path.parent / (folder_path.name + '.cbz')

    # 检查目标文件是否已存在
    if cbz_path.exists():
        print(f"跳过: {cbz_path} 已存在")
        return False

    try:
        # 创建ZIP文件（使用临时扩展名）
        zip_path = folder_path.parent / (folder_path.name + '.zip')

        print(f"正在压缩: {folder_path.name}")

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = Path(root) / file
                    # 计算相对路径，保持目录结构
                    arcname = file_path.relative_to(folder_path)
                    zf.write(file_path, arcname)

        # 重命名为CBZ
        zip_path.rename(cbz_path)

        # 删除原文件夹
        shutil.rmtree(folder_path)

        print(f"完成: {cbz_path.name}")
        return True

    except Exception as e:
        print(f"错误: 处理 {folder_path.name} 时失败 - {e}")
        # 清理可能创建的临时文件
        if zip_path.exists():
            zip_path.unlink()
        return False


def main():
    if len(sys.argv) < 2:
        print("用法: python folders_to_cbz.py <folder_or_zip1> [folder_or_zip2] ...")
        print("支持: 文件夹（压缩为CBZ）或 ZIP文件（重命名为CBZ）")
        print("请拖放文件夹或ZIP文件到此脚本上，或通过右键菜单调用")
        input("按回车键退出...")
        sys.exit(1)

    paths = [Path(arg) for arg in sys.argv[1:]]

    success_count = 0
    fail_count = 0

    for path in paths:
        if path.is_dir():
            if create_cbz_from_folder(path):
                success_count += 1
            else:
                fail_count += 1
        elif path.is_file() and path.suffix.lower() == '.zip':
            if rename_zip_to_cbz(path):
                success_count += 1
            else:
                fail_count += 1
        else:
            print(f"跳过: {path} 不是文件夹或ZIP文件")
            fail_count += 1

    print(f"\n处理完成: 成功 {success_count}, 失败 {fail_count}")

    # 如果是双击运行，暂停让用户看到结果
    if os.environ.get('PROMPT'):
        input("按回车键退出...")


if __name__ == '__main__':
    main()
