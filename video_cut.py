#!/usr/bin/env python3
"""
使用 FFmpeg 截取视频片段

用法：
    python video_cut.py <video_file> [start_time] [end_time]

时间格式支持：
    - 秒数：90
    - 时间戳：00:01:30 或 1:30

示例：
    python video_cut.py video.mp4 30 90         # 截取 30秒 到 90秒
    python video_cut.py video.mp4 00:00:30 00:01:30  # 同上
    python video_cut.py video.mp4               # 交互模式
"""

import os
import sys
import subprocess
from pathlib import Path


def parse_time(time_str: str) -> float:
    """
    将时间字符串转换为秒数

    支持格式：
    - 秒数：90
    - 时间戳：1:30, 00:01:30
    """
    time_str = time_str.strip()

    # 纯数字，直接返回
    if time_str.isdigit():
        return float(time_str)

    # 时间戳格式 HH:MM:SS 或 MM:SS
    parts = time_str.split(':')
    if len(parts) == 2:
        minutes, seconds = parts
        return float(minutes) * 60 + float(seconds)
    elif len(parts) == 3:
        hours, minutes, seconds = parts
        return float(hours) * 3600 + float(minutes) * 60 + float(seconds)

    raise ValueError(f"无法解析时间格式: {time_str}")


def format_time(seconds: float) -> str:
    """将秒数格式化为时间戳"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def get_video_duration(video_path: Path) -> float:
    """获取视频时长（秒）"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', str(video_path)],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return float(result.stdout.strip())
    except:
        pass
    return 0


def run_ffmpeg(cmd: list, description: str) -> bool:
    """
    运行 FFmpeg 命令，实时显示输出

    Args:
        cmd: FFmpeg 命令列表
        description: 操作描述

    Returns:
        bool: 成功返回True，失败返回False
    """
    print(f"\n执行: {' '.join(cmd)}")
    print("-" * 50)

    try:
        result = subprocess.run(cmd)
        print("-" * 50)

        if result.returncode == 0:
            print(f"✓ {description}成功")
            return True
        else:
            print(f"✗ {description}失败 (退出码: {result.returncode})")
            return False
    except Exception as e:
        print(f"✗ 执行出错: {e}")
        return False


def convert_to_mp4(source_path: Path) -> Path:
    """
    将视频转换/封装为 MP4 格式

    Args:
        source_path: 源视频文件路径

    Returns:
        Path: 转换后的 MP4 文件路径，失败返回原路径
    """
    mp4_path = source_path.with_suffix('.mp4')

    if mp4_path.exists():
        print(f"跳过: {mp4_path} 已存在")
        return source_path

    print(f"\n正在转换为 MP4: {source_path.name}")

    # 先尝试直接封装（不重新编码）
    cmd = [
        'ffmpeg', '-y',
        '-i', str(source_path),
        '-c', 'copy',
        str(mp4_path)
    ]

    if run_ffmpeg(cmd, "封装"):
        try:
            source_path.unlink()  # 删除原文件
            print(f"已删除原文件: {source_path.name}")
            return mp4_path
        except:
            pass

    # 直接封装失败，尝试重新编码
    print("直接封装失败，尝试重新编码...")
    cmd = [
        'ffmpeg', '-y',
        '-i', str(source_path),
        str(mp4_path)
    ]

    if run_ffmpeg(cmd, "重新编码"):
        try:
            source_path.unlink()
            print(f"已删除原文件: {source_path.name}")
            return mp4_path
        except:
            pass

    print("转换失败，保留原格式文件")
    return source_path


def cut_video(video_path: Path, start_time: float, end_time: float) -> Path:
    """
    使用 FFmpeg 截取视频片段

    Args:
        video_path: 视频文件路径
        start_time: 开始时间（秒）
        end_time: 结束时间（秒）

    Returns:
        Path: 输出文件路径
    """
    if not video_path.is_file():
        print(f"错误: {video_path} 不是文件")
        return None

    # 生成输出文件名
    stem = video_path.stem
    suffix = video_path.suffix
    start_str = format_time(start_time).replace(':', '-')
    end_str = format_time(end_time).replace(':', '-')
    output_path = video_path.parent / f"{stem}_{start_str}_{end_str}{suffix}"

    if output_path.exists():
        print(f"跳过: {output_path} 已存在")
        return None

    print(f"\n正在截取: {video_path.name}")
    print(f"  时间段: {format_time(start_time)} - {format_time(end_time)}")
    print(f"  时长: {format_time(end_time - start_time)}")
    print(f"  输出: {output_path.name}")

    # 使用 -ss 和 -to 参数截取视频
    # -ss 放在 -i 前面可以加速seek
    cmd = [
        'ffmpeg', '-y',
        '-ss', str(start_time),
        '-i', str(video_path),
        '-to', str(end_time - start_time),
        '-c', 'copy',  # 直接复制，不重新编码，速度快
        str(output_path)
    ]

    if run_ffmpeg(cmd, "截取"):
        return output_path

    # 如果 copy 失败，尝试重新编码
    print("直接复制失败，尝试重新编码...")
    cmd = [
        'ffmpeg', '-y',
        '-ss', str(start_time),
        '-i', str(video_path),
        '-to', str(end_time - start_time),
        str(output_path)
    ]

    if run_ffmpeg(cmd, "截取"):
        return output_path

    return None


def interactive_mode(video_path: Path):
    """交互模式：引导用户输入时间"""
    duration = get_video_duration(video_path)
    print(f"视频: {video_path.name}")
    if duration > 0:
        print(f"时长: {format_time(duration)}")
    print()

    while True:
        start_input = input("请输入开始时间（秒或时间戳，如 30 或 00:00:30）: ").strip()
        try:
            start_time = parse_time(start_input)
            break
        except ValueError as e:
            print(f"格式错误: {e}")

    while True:
        end_input = input("请输入结束时间: ").strip()
        try:
            end_time = parse_time(end_input)
            if end_time <= start_time:
                print("结束时间必须大于开始时间")
                continue
            if duration > 0 and end_time > duration:
                print(f"警告: 结束时间超过视频时长 ({format_time(duration)})")
                confirm = input("是否继续？[y/N]: ").strip().lower()
                if confirm != 'y':
                    continue
            break
        except ValueError as e:
            print(f"格式错误: {e}")

    output_path = cut_video(video_path, start_time, end_time)

    if output_path:
        # 询问是否转换为 MP4
        if output_path.suffix.lower() != '.mp4':
            print()
            convert = input("是否转换为 MP4 格式方便分享？[Y/n]: ").strip().lower()
            if convert != 'n':
                output_path = convert_to_mp4(output_path)

        print(f"\n输出文件: {output_path}")


def main():
    if len(sys.argv) < 2:
        print("用法: python video_cut.py <video_file> [start_time] [end_time]")
        print("时间格式: 秒数(如 90) 或 时间戳(如 00:01:30)")
        print("如果不提供时间参数，将进入交互模式")
        input("按回车键退出...")
        sys.exit(1)

    video_path = Path(sys.argv[1])

    if not video_path.exists():
        print(f"错误: {video_path} 不存在")
        input("按回车键退出...")
        sys.exit(1)

    if len(sys.argv) == 2:
        # 交互模式
        interactive_mode(video_path)
    elif len(sys.argv) == 4:
        # 命令行模式
        try:
            start_time = parse_time(sys.argv[2])
            end_time = parse_time(sys.argv[3])
        except ValueError as e:
            print(f"时间格式错误: {e}")
            sys.exit(1)

        if end_time <= start_time:
            print("错误: 结束时间必须大于开始时间")
            sys.exit(1)

        output_path = cut_video(video_path, start_time, end_time)

        if output_path:
            # 询问是否转换为 MP4
            if output_path.suffix.lower() != '.mp4':
                print()
                convert = input("是否转换为 MP4 格式方便分享？[Y/n]: ").strip().lower()
                if convert != 'n':
                    output_path = convert_to_mp4(output_path)

            print(f"\n输出文件: {output_path}")
    else:
        print("用法: python video_cut.py <video_file> [start_time] [end_time]")
        sys.exit(1)

    # 如果是双击运行，暂停让用户看到结果
    if os.environ.get('PROMPT'):
        input("\n按回车键退出...")


if __name__ == '__main__':
    main()