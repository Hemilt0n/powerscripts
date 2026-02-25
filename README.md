# PowerScripts

Windows 实用脚本工具集。

## 文件夹转 CBZ

将文件夹批量转换为 CBZ 格式（漫画书归档格式）。

### 功能

- 批量将文件夹压缩为 CBZ 文件
- 保持原有目录结构
- 自动删除已转换的源文件夹
- 支持 Windows 右键菜单集成

### 安装右键菜单

双击运行 `install_cbz_menu.py`（自动请求管理员权限），选择「安装」即可。

安装后，右键点击任意文件夹即可看到「转换为CBZ」选项。

### 手动使用

```bash
python folders_to_cbz.py <folder1> [folder2] [folder3] ...
```

或将文件夹拖放到 `folders_to_cbz.py` 上。

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

## 依赖

- Python 3.6+
- Windows 操作系统

## 许可证

MIT
