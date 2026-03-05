# PowerScripts

Windows 实用脚本工具集。

## 文件夹/ZIP 转 CBZ

将文件夹或 ZIP 文件批量转换为 CBZ 格式（漫画书归档格式）。

### 功能

- 文件夹：压缩为 CBZ 文件并删除源文件夹
- ZIP 文件：直接重命名为 CBZ（CBZ 本质就是 ZIP）
- 保持原有目录结构
- 支持 Windows 右键菜单集成（文件夹 + ZIP 文件）

### 安装右键菜单

双击运行 `install_cbz_menu.py`（自动请求管理员权限），选择「安装」即可。

安装后，右键点击文件夹或 ZIP 文件，即可看到「转换为CBZ」选项。

### 手动使用

```bash
python folders_to_cbz.py <folder_or_zip1> [folder_or_zip2] ...
```

或将文件夹/ZIP 文件拖放到 `folders_to_cbz.py` 上。

### 卸载

再次运行 `install_cbz_menu.py`，选择「卸载」。

## 减少目录层级

将文件夹内的全部内容提取到上级目录，然后删除该文件夹。适用于解压后多了一层无用目录的情况。

### 功能

- 将文件夹内容移动到上级目录
- 自动处理同名文件冲突（添加原文件夹名前缀）
- 自动删除已清空的文件夹
- 支持 Windows 右键菜单集成

### 安装右键菜单

双击运行 `install_flatten_menu.py`（自动请求管理员权限），选择「安装」即可。

安装后，右键点击任意文件夹即可看到「减少目录层级」选项。

### 手动使用

```bash
python flatten_folder.py <folder1> [folder2] [folder3] ...
```

或将文件夹拖放到 `flatten_folder.py` 上。

### 卸载

再次运行 `install_flatten_menu.py`，选择「卸载」。

## MPV 批量播放

使用 MPV 播放器批量播放文件夹内的所有文件。支持视频、音频等多种格式。

### 功能

- 批量播放文件夹内所有支持的文件格式
- 支持两种右键菜单：文件夹右键 + 文件夹内空白处右键
- 显示 MPV 原生输出信息和控制界面
- 自动检测 MPV 是否已安装

### 安装右键菜单

双击运行 `install_mpv_menu.py`（自动请求管理员权限），选择「安装」即可。

安装后，右键点击任意文件夹或文件夹内空白处，即可看到「使用MPV批量播放」选项。

### 手动使用

```bash
python mpv_batch_play.py [folder_path]
```

如果不提供 `folder_path` 参数，则播放当前目录下的所有文件。

或将文件夹拖放到 `mpv_batch_play.py` 上。

### 卸载

再次运行 `install_mpv_menu.py`，选择「卸载」。

## 视频截取

使用 FFmpeg 截取视频片段，支持指定起始和结束时间。

### 功能

- 支持秒数或时间戳格式输入（如 `90` 或 `00:01:30`）
- 交互模式引导输入时间参数
- 自动获取视频时长
- 输出文件自动命名（源文件名+截取区间）
- 优先使用流复制，失败时自动重新编码
- 截取后询问是否转换为 MP4 格式（方便分享至社交平台）
- 实时显示 FFmpeg 命令和输出
- 支持常见视频格式右键菜单

### 安装右键菜单

双击运行 `install_video_cut_menu.py`（自动请求管理员权限），选择「安装」即可。

安装后，右键点击视频文件即可看到「截取视频片段」选项。

支持格式：mp4, mkv, avi, mov, wmv, flv, webm, m4v, mpg, mpeg

### 手动使用

```bash
# 交互模式（引导输入时间）
python video_cut.py video.mp4

# 命令行模式
python video_cut.py video.mp4 30 90           # 秒数
python video_cut.py video.mp4 00:00:30 00:01:30  # 时间戳
```

或将视频文件拖放到 `video_cut.py` 上，进入交互模式。

### 卸载

再次运行 `install_video_cut_menu.py`，选择「卸载」。

## 依赖

- Python 3.6+
- Windows 操作系统

## 许可证

MIT
