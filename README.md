多媒体编辑器用户文档
==================

# 简介

多媒体编辑器是一个基于FFmpeg的图形用户界面应用程序，用于对视频和音频进行编辑、截取、压制以及格式转换。
该编辑器提供了直观的界面，使用户能够方便地执行多种多媒体处理操作。

## 视频编辑

### 视频裁剪

* 用户可以选择需要编辑的视频文件。
* 提供预览视频功能，支持使用ffplay进行视频预览。
* 用户可以设置起始时刻和结束时刻，对视频进行裁剪。
* 提供选择输出路径的功能，方便保存编辑后的视频文件。

### 合并字幕

* 用户可以选择需要合并的字幕文件（.ass 格式）。
* 提供选择压制加速方法和质量的选项。
* 支持“无加速”、“AMD AMF”、“NVIDIA NVENC”和“Intel QSV”四种压制方法。
* 用户可选择压制后的视频质量为高、中、低三档。

### 视频抽取

* 用户可以抽取原视频中的音频或视频。
* 输出路径为原音视频路径，程序将自动添加输出格式的文件后缀。

## 格式转换

### 视频转换

* 用户可以选择需要转换格式的视频文件。
* 提供选择输出格式的选项，支持常见的视频格式（mp4、avi、mkv、mov、mpeg、mpg、webm）。
* 输出路径为原视频路径，程序将自动添加输出格式的文件后缀。

### 音频转换

* 用户可以选择需要转换格式的音频文件。
* 提供选择输出格式的选项，支持常见的音频格式（mp3、wav、aac、flac、m4a、ogg）。
* 输出路径为原音频路径，程序将自动添加输出格式的文件后缀。

# 使用方法

* 安装依赖：确保已安装FFmpeg环境。
* 运行程序：双击打开程序
* 选择功能：在主界面中点击菜单栏中的“视频编辑”或“格式转换”切换到对应功能界面。
* 操作步骤：根据界面提示，选择或输入相应的文件路径和参数，执行相应的操作。
* 查看结果：在界面中会显示操作结果，如视频是否成功裁剪、压制，以及转换后的文件路径。

# 注意事项

请确保输入文件的格式与所选择的操作兼容，否则可能导致操作失败。
对于视频压制操作，建议选择适当的加速方法和质量，以免影响输出效果。

# 反馈与贡献

如果您在使用过程中遇到问题或有改进建议，请随时提出。
我们欢迎开发者共同参与贡献，共同改进这个多媒体编辑器。

# 版本历史

v1.0.0（2023/12/29）：初版发布，包含视频编辑和格式转换两大功能。