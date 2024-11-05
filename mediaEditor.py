import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QAction, QFileDialog,QWidget, QHBoxLayout,QComboBox
from PyQt5.QtCore import QSettings
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QTimer
import subprocess
import os

from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout

class VideoEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.video_player = VideoPlayer()# 创建视频播放器

        self.settings = QSettings("MyApp", "VideoEditor")  # 创建QSettings实例，指定应用程序名和组织名

        self.cut_text = QLabel('视频裁剪', self)

        self.video_path_textbox = QLineEdit(self)
        self.video_path_textbox.setPlaceholderText('请选择需要编辑的视频路径')

        self.browse_video_button = QPushButton('选择视频', self)
        self.browse_video_button.clicked.connect(self.open_file_manager)

        self.preview_button = QPushButton('预览视频', self)
        self.preview_button.clicked.connect(self.preview_video)

        self.output_path_textbox = QLineEdit(self)
        self.output_path_textbox.setPlaceholderText('请选择视频的输出路径')

        self.output_button = QPushButton('选择路径', self)
        self.output_button.clicked.connect(self.output_video)

        self.start_time_label = QLabel('起始时刻', self)
        self.start_time_textbox = QLineEdit('00:00:00', self)

        self.end_time_label = QLabel('结束时刻', self)
        self.end_time_textbox = QLineEdit('00:00:20', self)

        self.cut_button = QPushButton('截取', self)
        self.cut_button.clicked.connect(self.cut_video)

        self.ass_text = QLabel('合并字幕', self)
        self.ass_path_textbox = QLineEdit(self)
        self.ass_path_textbox.setPlaceholderText('请选择需要合并的字幕路径')

        self.ass_button = QPushButton('选择字幕', self)
        self.ass_button.clicked.connect(self.add_ass)

        self.method_label = QLabel('请选择压制加速方法', self)
        self.method_combobox = QComboBox(self)
        self.method_combobox.addItems(['无加速', 'AMD AMF', 'NVIDIA NVENC', 'Intel QSV'])
        default_method = self.settings.value("method_combobox", "无加速", type=str)  # 读取上次保存的选择，默认为"无加速"
        self.method_combobox.setCurrentText(default_method)

        self.quality_label = QLabel('请选择质量', self)
        self.quality_combobox = QComboBox(self)
        self.quality_combobox.addItems(['高', '中', '低'])
        default_quality = self.settings.value("quality_combobox", "高", type=str)  # 读取上次保存的选择，默认为"高"
        self.quality_combobox.setCurrentText(default_quality)

        self.press_button = QPushButton('压制', self)
        self.press_button.clicked.connect(self.press_video)

        self.get_text = QLabel('抽取', self)
        self.get_textbox = QLineEdit(self)
        self.get_textbox.setPlaceholderText('抽取的视频或音频在原视频路径下')
        self.getA_button = QPushButton('抽取音频',self)
        self.getA_button.clicked.connect(self.get_audio)
        self.getV_button = QPushButton('抽取视频', self)
        self.getV_button.clicked.connect(self.get_video)

        # 创建水平布局

        hbox_video_input = QHBoxLayout()
        hbox_video_input.addWidget(self.video_path_textbox)
        hbox_video_input.addWidget(self.browse_video_button)

        hbox_output = QHBoxLayout()
        hbox_output.addWidget(self.output_path_textbox)
        hbox_output.addWidget(self.output_button)

        hbox_preview_button = QHBoxLayout()
        hbox_preview_button.addStretch(1)
        hbox_preview_button.addWidget(self.preview_button)

        hbox_cut = QHBoxLayout()
        hbox_cut.addWidget(self.start_time_label)
        hbox_cut.addWidget(self.start_time_textbox)
        hbox_cut.addStretch(1)
        hbox_cut.addWidget(self.end_time_label)
        hbox_cut.addWidget(self.end_time_textbox)
        hbox_cut.addStretch(1)
        hbox_cut.addWidget(self.cut_button)

        hbox_ass = QHBoxLayout()
        hbox_ass.addWidget(self.ass_path_textbox)
        hbox_ass.addWidget(self.ass_button)

        hbox_press_button = QHBoxLayout()
        hbox_press_button.addWidget(self.method_label)
        hbox_press_button.addWidget(self.method_combobox)
        hbox_press_button.addStretch(1)
        hbox_press_button.addWidget(self.quality_label)
        hbox_press_button.addWidget(self.quality_combobox)
        hbox_press_button.addStretch(1)
        hbox_press_button.addWidget(self.press_button)

        hbox_get = QHBoxLayout()
        hbox_get.addWidget(self.get_textbox)
        hbox_get.addWidget(self.getV_button)
        hbox_get.addWidget(self.getA_button)

        # 创建垂直布局
        layout = QVBoxLayout()

        layout.addWidget(self.cut_text)
        layout.addLayout(hbox_video_input)
        layout.addLayout(hbox_preview_button)
        layout.addLayout(hbox_output)
        layout.addLayout(hbox_cut)
        layout.addStretch(1)

        layout.addWidget(self.ass_text)
        layout.addLayout(hbox_ass)
        layout.addLayout(hbox_press_button)
        layout.addStretch(1)

        layout.addWidget(self.get_text)
        layout.addLayout(hbox_get)
        layout.addStretch(1)

        self.setLayout(layout)

    def open_file_manager(self):
        video_path, _ = QFileDialog.getOpenFileName(self, "打开视频", "", "视频文件 (*.mp4 *.avi *.mkv *.mov *.mpeg *.mpg *.webm')")
        if video_path:
            self.video_path_textbox.setText(video_path)

    def preview_video(self):
        video_path = self.video_path_textbox.text()  # 获取视频路径
        '''
        if video_path:
            cmd = ['ffplay', '-i', video_path, '-vf', 'scale=1280:720', '-window_title', 'Video Player']
            subprocess.Popen(cmd, stderr=subprocess.PIPE)
        else:
            print("错误：请先选择视频文件")
        '''

        if video_path:
            self.video_player.load_video(video_path)
            self.video_player.show()
        else:
            print("错误：请先选择视频文件")


    def output_video(self):
        # 打开文件夹对话框，选择输出路径
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder_dialog = QFileDialog()
        selected_path = folder_dialog.getExistingDirectory(self, "选择输出文件夹", options=options)

        # 如果用户选择了路径
        if selected_path:
            # 提取原视频文件名
            original_video_path = self.video_path_textbox.text()
            original_video_name = os.path.basename(original_video_path)
            base_name, extension = os.path.splitext(original_video_name)

            # 构建默认输出视频名（原视频名 + "_output" + 原视频格式后缀）
            default_output_name = base_name + "_output" + extension

            # 在文本框中显示选择的路径和默认输出视频名
            self.output_path_textbox.setText(os.path.join(selected_path, default_output_name))

    def cut_video(self):
        # 读取起始时刻和结束时刻文本框的时间
        start_time = self.start_time_textbox.text()
        end_time = self.end_time_textbox.text()

        # 获取输入视频路径和输出路径
        input_video_path = self.video_path_textbox.text()
        output_video_path = self.output_path_textbox.text()

        # 将输出路径中的斜杠改为双反斜杠，并使用原始字符串处理路径
        output_video_path = output_video_path.replace('/', '\\')

        # 将输出路径中的斜杠改为双反斜杠，并使用原始字符串处理路径
        input_video_path = input_video_path.replace('/', '\\')

        # 如果用户未选择输出路径，则使用原视频路径作为输出路径
        if not output_video_path:
            input_folder, input_filename = os.path.split(input_video_path)
            input_filename_no_ext, input_file_ext = os.path.splitext(input_filename)

            output_video_filename = f"{input_filename_no_ext}_output{input_file_ext}"
            output_video_path = os.path.join(input_folder, output_video_filename)

            # 检查是否已经存在相同文件名的文件
        counter = 0
        while os.path.exists(output_video_path):
            counter += 1
            output_video_filename = f"{input_filename_no_ext}_output_{counter}{input_file_ext}"
            output_video_path = os.path.join(input_folder, output_video_filename)

            # 构建ffmpeg命令
        ffmpeg_command = [
            'ffmpeg',
            '-ss', start_time,
            '-t', end_time,
            '-i', input_video_path,
            '-vcodec', 'copy', '-acodec', 'copy',
            output_video_path
        ]

        try:
            # 调用ffmpeg命令
            subprocess.run(ffmpeg_command, check=True)
            print("视频截取成功！")
        except subprocess.CalledProcessError as e:
            # 输出异常信息
            print("视频截取失败。异常信息:", e)
            # 在GUI中显示错误信息，可以使用 QMessageBox 进行弹窗提示
            # QMessageBox.critical(self, "错误", f"视频截取失败。异常信息: {str(e)}")
        except Exception as e:
            # 捕获其他可能的异常
            print("发生未知错误:", e)
            # 在GUI中显示错误信息
            # QMessageBox.critical(self, "错误", f"发生未知错误: {str(e)}")

    def add_ass(self):
        ass_path, _ = QFileDialog.getOpenFileName(self, "选择字幕文件", "", "字幕文件 (*.ass);;All Files (*)")
        if ass_path:
            self.ass_path_textbox.setText(ass_path)

    def press_video(self):
        # 获取输入视频路径和输出路径
        input_video_path = self.video_path_textbox.text()
        output_video_path = self.output_path_textbox.text()

        input_video_path = input_video_path.replace('/', '\\')
        output_video_path = output_video_path.replace('/', '\\')

        # 如果用户未选择输出路径，则使用原视频路径作为输出路径
        if not output_video_path:
            input_folder, input_filename = os.path.split(input_video_path)
            input_filename_no_ext, input_file_ext = os.path.splitext(input_filename)

            output_video_filename = f"{input_filename_no_ext}_output{input_file_ext}"
            output_video_path = os.path.join(input_folder, output_video_filename)

        # 检查是否已经存在相同文件名的文件
        counter = 0
        while os.path.exists(output_video_path):
            counter += 1
            output_video_filename = f"{input_filename_no_ext}_output_{counter}{input_file_ext}"
            output_video_path = os.path.join(input_folder, output_video_filename)

        #获取输入字幕ass路径
        ass_path = self.ass_path_textbox.text()

        ass_path = ass_path.replace('/', '\\\\\\')
        ass_path = ass_path.replace(':', "\:")

        #如果用户未选择字幕
        if not ass_path:
            print("请先选择字幕文件")
            return

        selected_method = self.method_combobox.currentText()  # 获取用户选择的转换方法
        self.settings.setValue("method_combobox", selected_method)

        selected_quality = self.quality_combobox.currentText()  # 获取用户选择的质量
        self.settings.setValue("quality_combobox", selected_quality)

        if selected_quality == '高':
            code_rate='12000K'
        elif selected_quality == '中':
            code_rate='6000K'
        elif selected_quality == '低':
            code_rate='3000K'

        if selected_method == '无加速':
            ffmpeg_command_pass1 = (
                'ffmpeg -y -i "{input}" -c:v libx264 -preset medium -b:v "{rate}" -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2, subtitles=\'{ass}\'" -pass 1 -an -sn -f mp4 -threads 0 NUL'
            ).format(input=input_video_path, ass=ass_path, rate=code_rate)

            ffmpeg_command_pass2 = (
                'ffmpeg -y -i "{input}" -c:v libx264 -preset medium -b:v "{rate}" -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2, subtitles=\'{ass}\'" -map 0:v:0? -pass 2 -c:a aac -q:a 2 -map 0:a? -map_chapters 0 -f mp4 -threads 0 "{output}"'
            ).format(input=input_video_path, ass=ass_path, rate=code_rate, output=output_video_path)
        elif selected_method == 'AMD AMF':
            ffmpeg_command_pass1 = (
                'ffmpeg -y -i "{input}" -c:v h264_amf -quality balanced -b:v "{rate}" -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2, subtitles=\'{ass}\'" -pass 1 -an -sn -f mp4 -threads 0 NUL'
            ).format(input=input_video_path, ass=ass_path, rate=code_rate)

            ffmpeg_command_pass2 = (
                'ffmpeg -y -i "{input}" -c:v h264_amf -quality balanced -b:v "{rate}" -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2, subtitles=\'{ass}\'" -map 0:v:0? -pass 2 -c:a aac -q:a 2 -map 0:a? -map_chapters 0 -f mp4 -threads 0 "{output}"'
            ).format(input=input_video_path, ass=ass_path, rate=code_rate, output=output_video_path)
        elif selected_method == 'NVIDIA NVENC':
            ffmpeg_command_pass1 = (
                'ffmpeg -y -hwaccel cuda -i "{input}" -c:v h264_nvenc -preset medium -b:v "{rate}" -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2, subtitles=\'{ass}\'" -pass 1 -an -sn -f mp4 -threads 0 NUL'
            ).format(input=input_video_path, ass=ass_path, rate=code_rate)

            ffmpeg_command_pass2 = (
                'ffmpeg -y -hwaccel cuda -i "{input}" -c:v h264_nvenc -preset medium -b:v "{rate}" -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2, subtitles=\'{ass}\'" -map 0:v:0? -pass 2 -c:a aac -q:a 2 -map 0:a? -map_chapters 0 -f mp4 -threads 0 "{output}"'
            ).format(input=input_video_path, ass=ass_path, rate=code_rate, output=output_video_path)
        elif selected_method == 'Intel QSV':
            ffmpeg_command_pass1 = (
                'ffmpeg -y -hwaccel qsv -c:v h264_qsv -b:v "{rate}" -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2, subtitles=\'{ass}\'" -pass 1 -an -sn -f mp4 -threads 0 NUL'
            ).format(input=input_video_path, ass=ass_path, rate=code_rate)

            ffmpeg_command_pass2 = (
                'ffmpeg -y -hwaccel qsv -c:v h264_qsv -b:v "{rate}" -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2, subtitles=\'{ass}\'" -map 0:v:0? -pass 2 -c:a aac -q:a 2 -map 0:a? -map_chapters 0 -f mp4 -threads 0 "{output}"'
            ).format(input=input_video_path, ass=ass_path, rate=code_rate, output=output_video_path)

        try:
            # 调用ffmpeg命令
            subprocess.run(ffmpeg_command_pass1, check=True)
            subprocess.run(ffmpeg_command_pass2, check=True)
            print(f"视频已成功压制，输出路径为：{output_video_path}")
        except subprocess.CalledProcessError as e:
            # 输出异常信息
            print("视频压制失败。异常信息:", e)
            # 在GUI中显示错误信息，可以使用 QMessageBox 进行弹窗提示
            # QMessageBox.critical(self, "错误", f"视频截取失败。异常信息: {str(e)}")
        except Exception as e:
            # 捕获其他可能的异常
            print("发生未知错误:", e)
            # 在GUI中显示错误信息
            # QMessageBox.critical(self, "错误", f"发生未知错误: {str(e)}"

    def get_audio(self):
        input_video_path = self.video_path_textbox.text()

        if not input_video_path:
            print("请先选择输入视频")
            return

        input_folder, input_filename = os.path.split(input_video_path)
        input_filename_no_ext, input_file_ext = os.path.splitext(input_filename)

        output_audio_filename = f"{input_filename_no_ext}_output_audio.mp3"
        output_audio_path = os.path.join(input_folder, output_audio_filename)

        # 检查是否已经存在相同文件名的文件
        counter = 0
        while os.path.exists(output_audio_path):
            counter += 1
            output_audio_filename = f"{input_filename_no_ext}_output_{counter}{input_file_ext}"
            output_audio_path = os.path.join(input_folder, output_audio_filename)

        # 构建 FFmpeg 命令
        ffmpeg_command = [
            'ffmpeg',
            '-i', input_video_path,
            '-vn',  # 仅抽取音频
            '-y',  # 覆盖输出文件
            '-acodec', 'libmp3lame',  # 设置音频编解码器为 libmp3lame
            output_audio_path
        ]

        try:
            # 调用 FFmpeg 命令
            subprocess.run(ffmpeg_command, check=True)
            print(f"音频已成功抽取，输出路径为：{output_audio_path}")
        except subprocess.CalledProcessError as e:
            # 输出异常信息
            print("音频抽取失败。异常信息:", e)

    def get_video(self):
        input_video_path = self.video_path_textbox.text()

        if not input_video_path:
            print("请先选择输入视频")
            return

        input_folder, input_filename = os.path.split(input_video_path)
        input_filename_no_ext, input_file_ext = os.path.splitext(input_filename)

        output_video_filename = f"{input_filename_no_ext}_output_video{input_file_ext}"
        output_video_path = os.path.join(input_folder, output_video_filename)

        # 检查是否已经存在相同文件名的文件
        counter = 0
        while os.path.exists(output_video_path):
            counter += 1
            output_video_filename = f"{input_filename_no_ext}_output_{counter}{input_file_ext}"
            output_video_path = os.path.join(input_folder, output_video_filename)

        # 构建 FFmpeg 命令
        ffmpeg_command = [
            'ffmpeg',
            '-i', input_video_path,
            '-an',  # 不包含音频
            '-c:v', 'copy',  # 使用原始视频编解码器进行拷贝
            '-y',  # 覆盖输出文件
            output_video_path
        ]

        try:
            # 调用 FFmpeg 命令
            subprocess.run(ffmpeg_command, check=True)
            print(f"视频已成功抽取，输出路径为：{output_video_path}")
        except subprocess.CalledProcessError as e:
            # 输出异常信息
            print("视频抽取失败。异常信息:", e)

class Format(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_text = QLabel('视频转换', self)

        self.video_path_textbox = QLineEdit(self)
        self.video_path_textbox.setPlaceholderText('输入视频路径')

        self.browse_video_button = QPushButton('输入视频', self)
        self.browse_video_button.clicked.connect(self.open_file_manager)

        self.format_text = QLabel('选择转换格式', self)
        self.format_combobox = QComboBox(self)
        self.format_combobox.addItems(['mp4','avi','mkv','mov','mpeg','mpg','webm'])  # 添加常用视频格式
        self.format_combobox.setCurrentText('mp4')  # 初始选择为 mp4

        self.convert_button = QPushButton('点击转换', self)
        self.convert_button.clicked.connect(self.convert_video)

        self.audio_text = QLabel('音频转换', self)

        self.audio_path_textbox = QLineEdit(self)
        self.audio_path_textbox.setPlaceholderText('输入音频路径')

        self.browse_audio_button = QPushButton('输入音频', self)
        self.browse_audio_button.clicked.connect(self.open_file_managerA)

        self.formatA_text = QLabel('选择转换格式', self)
        self.formatA_combobox = QComboBox(self)
        self.formatA_combobox.addItems(['mp3','wav','aac','flac','m4a','ogg'])  # 添加常用音频格式
        self.formatA_combobox.setCurrentText('mp3')  # 初始选择为 mp3

        self.convertA_button = QPushButton('点击转换', self)
        self.convertA_button.clicked.connect(self.convert_audio)

        # 创建水平布局
        hbox_video_input = QHBoxLayout()
        hbox_video_input.addWidget(self.video_path_textbox)
        hbox_video_input.addWidget(self.browse_video_button)

        hbox_video_format = QHBoxLayout()
        hbox_video_format.addWidget(self.format_text)
        hbox_video_format.addWidget(self.format_combobox)
        hbox_video_format.addStretch(1)
        hbox_video_format.addWidget(self.convert_button)

        hbox_audio_input = QHBoxLayout()
        hbox_audio_input.addWidget(self.audio_path_textbox)
        hbox_audio_input.addWidget(self.browse_audio_button)

        hbox_audio_format = QHBoxLayout()
        hbox_audio_format.addWidget(self.formatA_text)
        hbox_audio_format.addWidget(self.formatA_combobox)
        hbox_audio_format.addStretch(1)
        hbox_audio_format.addWidget(self.convertA_button)

        # 创建垂直布局
        layout = QVBoxLayout()

        layout.addWidget(self.video_text)
        layout.addLayout(hbox_video_input)
        layout.addLayout(hbox_video_format)
        layout.addStretch(1)

        layout.addWidget(self.audio_text)
        layout.addLayout(hbox_audio_input)
        layout.addLayout(hbox_audio_format)
        layout.addStretch(1)

        self.setLayout(layout)

    def open_file_manager(self):
        video_path, _ = QFileDialog.getOpenFileName(self, "打开视频", "", "视频文件 (*.mp4 *.avi *.mkv *.mov *.mpeg *.mpg *.webm')")
        if video_path:
            self.video_path_textbox.setText(video_path)

    def convert_video(self):
        input_video_path = self.video_path_textbox.text()
        output_format = self.format_combobox.currentText()

        if not input_video_path:
            print("请先选择输入视频")
            return

        input_folder, input_filename = os.path.split(input_video_path)
        input_filename_no_ext, input_file_ext = os.path.splitext(input_filename)

        output_video_filename = f"{input_filename_no_ext}_output.{output_format}"
        output_video_path = os.path.join(input_folder, output_video_filename)

        # 检查是否已经存在相同文件名的文件
        counter = 0
        while os.path.exists(output_video_path):
            counter += 1
            output_video_filename = f"{input_filename_no_ext}_output_{counter}{input_file_ext}"
            output_video_path = os.path.join(input_folder, output_video_filename)

        # 根据输出视频格式选择编码器
        if output_format == 'mp4':
            video_encoder = 'libx264'
        elif output_format == 'avi':
            video_encoder = 'mpeg4'
        elif output_format == 'mkv':
            video_encoder = 'libx264'
        elif output_format == 'mov':
            video_encoder = 'libx264'
        elif output_format == 'mpeg':
            video_encoder = 'mpeg2video'
        elif output_format == 'mpg':
            video_encoder = 'mpeg2video'
        elif output_format == 'webm':
            video_encoder = 'libvpx'
        else:
            print("不支持的视频格式")
            return

        # 构建 FFmpeg 命令
        ffmpeg_command = [
            'ffmpeg',
            '-i', input_video_path,
            '-c:v', video_encoder,  # 根据选择的格式设置相应的编码器
            '-c:a', 'copy',  # 使用原始音频编解码器进行拷贝
            '-y',  # 覆盖输出文件
            output_video_path
        ]

        try:
            # 调用 FFmpeg 命令
            subprocess.run(ffmpeg_command, check=True)
            print(f"视频已成功转换，输出路径为：{output_video_path}")
        except subprocess.CalledProcessError as e:
            # 输出异常信息
            print("视频转换失败。异常信息:", e)

    def open_file_managerA(self):
        audio_path, _ = QFileDialog.getOpenFileName(self, "打开音频", "", "音频文件 (*.mp3 *.wav *.aac *.mov *.flac *.m4a *.ogg')")
        if audio_path:
            self.audio_path_textbox.setText(audio_path)

    def convert_audio(self):
        input_audio_path = self.audio_path_textbox.text()
        output_audio_format = self.formatA_combobox.currentText()

        if not input_audio_path:
            print("请先选择输入音频")
            return

        input_folder, input_filename = os.path.split(input_audio_path)
        input_filename_no_ext, input_file_ext = os.path.splitext(input_filename)

        output_audio_filename = f"{input_filename_no_ext}_output_audio.{output_audio_format}"
        output_audio_path = os.path.join(input_folder, output_audio_filename)

        # 检查是否已经存在相同文件名的文件
        counter = 0
        while os.path.exists(output_audio_path):
            counter += 1
            output_audio_filename = f"{input_filename_no_ext}_output_{counter}{input_file_ext}"
            output_audio_path = os.path.join(input_folder, output_audio_filename)

        # 根据输出音频格式选择编码器
        if output_audio_format == 'mp3':
            audio_encoder = 'libmp3lame'
        elif output_audio_format == 'wav':
            audio_encoder = 'pcm_s16le'
        elif output_audio_format == 'aac':
            audio_encoder = 'aac'
        elif output_audio_format == 'mov':
            audio_encoder = 'aac'
        elif output_audio_format == 'flac':
            audio_encoder = 'flac'
        elif output_audio_format == 'm4a':
            audio_encoder = 'aac'
        elif output_audio_format == 'ogg':
            audio_encoder = 'libvorbis'
        else:
            print("不支持的音频格式")
            return

        # 构建 FFmpeg 命令
        ffmpeg_command = [
            'ffmpeg',
            '-i', input_audio_path,
            '-c:a', audio_encoder,  # 根据选择的格式设置相应的编码器
            '-y',  # 覆盖输出文件
            output_audio_path
        ]

        try:
            # 调用 FFmpeg 命令
            subprocess.run(ffmpeg_command, check=True)
            print(f"音频已成功转换，输出路径为：{output_audio_path}")
        except subprocess.CalledProcessError as e:
            # 输出异常信息
            print("音频转换失败。异常信息:", e)

class VideoPlayer(QWidget):
    def __init__(self, video_path=None):
        super().__init__()

        # 创建播放器和视频窗口
        self.player = QMediaPlayer(self)
        self.video_widget = QVideoWidget(self)
        self.player.setVideoOutput(self.video_widget)

        # 创建UI元素
        self.play_button = QPushButton('▶', self)
        self.volume_label = QLabel('音量：', self)
        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.seek_label = QLabel('播放进度：', self)
        self.seek_slider = QSlider(Qt.Horizontal, self)
        self.label_time = QLabel('00:00:00', self)

        # 设置布局
        controls_layout0 = QHBoxLayout()
        controls_layout0.addWidget(self.video_widget)

        # 第一行布局
        controls_layout1 = QHBoxLayout()
        controls_layout1.addStretch(6)
        controls_layout1.addWidget(self.play_button)
        controls_layout1.addStretch(5)  # 添加占位符
        controls_layout1.addWidget(self.volume_label)
        controls_layout1.addWidget(self.volume_slider)

        # 第二行布局
        controls_layout2 = QHBoxLayout()
        controls_layout2.addWidget(self.seek_label)
        controls_layout2.addWidget(self.label_time)
        controls_layout2.addStretch(1)

        # 第三行布局
        controls_layout3 = QHBoxLayout()
        controls_layout3.addWidget(self.seek_slider)

        layout = QVBoxLayout(self)
        layout.addLayout(controls_layout0)
        layout.addLayout(controls_layout1)
        layout.addLayout(controls_layout2)
        layout.addLayout(controls_layout3)

        # 设置布局中视频播放器的拉伸因子
        layout.setStretchFactor(controls_layout0, 2)

        # 初始化界面
        self.init_ui()

        # 如果提供了视频路径，则加载视频
        if video_path:
            self.load_video(video_path)

    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle('视频播放器')
        self.setGeometry(100, 100, 1300, 900)

        # 绑定按钮点击事件
        self.play_button.clicked.connect(self.toggle_play)

        # 绑定播放器信号
        self.player.positionChanged.connect(self.update_slider)
        self.player.durationChanged.connect(self.update_duration)
        self.player.volumeChanged.connect(self.update_volume)
        self.player.mediaStatusChanged.connect(self.handle_media_status)

        # 设置定时器，实时更新播放时间
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_play_time)
        self.timer.start(1000)

        # 设置音量滑块初始值
        self.volume_slider.setValue(self.player.volume())
        # 设置音量滑块信号
        self.volume_slider.valueChanged.connect(self.set_volume)

        # 设置滑动条信号
        self.seek_slider.sliderReleased.connect(self.seek_to_position)

    def load_video(self, video_path):
        video_url = QUrl.fromLocalFile(video_path)
        self.player.setMedia(QMediaContent(video_url))

    def toggle_play(self):
        # 切换播放/暂停状态
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_button.setText('▶')
        else:
            self.player.play()
            self.play_button.setText('||')

    def update_slider(self, position):
        # 更新滑动条位置和播放时间显示
        if not self.seek_slider.isSliderDown():
            self.seek_slider.setValue(position)
            self.update_play_time()

    def update_duration(self, duration):
        # 设置滑动条的最大值为视频时长
        self.seek_slider.setMaximum(duration)

    def update_play_time(self):
        # 更新播放时间显示
        m, s = divmod(self.player.position() / 1000, 60)
        h, m = divmod(m, 60)
        self.label_time.setText("%02d:%02d:%02d" % (h, m, s))

    def update_volume(self):
        # 更新音量滑块位置
        self.volume_slider.setValue(self.player.volume())

    def set_volume(self, value):
        # 设置播放器音量
        self.player.setVolume(value)

    def seek_to_position(self):
        # 处理点击滑动条时的快进和倒退功能
        target_position = self.seek_slider.value()
        self.player.setPosition(target_position)

    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.stop_video()

    def stop_video(self):
        self.player.stop()
        self.play_button.setText('▶')
        self.seek_slider.setValue(0)

    def closeEvent(self, event):
        # 重写关闭事件，确保在窗口关闭时停止播放
        self.player.stop()
        event.accept()

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("多媒体编辑器")
        self.setGeometry(100, 100, 560, 330)

        self.central_widget = VideoEditor()
        self.setCentralWidget(self.central_widget)

        self.create_menu()

    def create_menu(self):
        main_menu = self.menuBar()

        video_option = QAction('视频编辑', self)
        video_option.triggered.connect(self.switch_to_video_editor)

        format_option = QAction('格式转换', self)
        format_option.triggered.connect(self.switch_to_format_conversion)

        main_menu.addAction(video_option)
        main_menu.addAction(format_option)

        exit_action = QAction('退出', self)
        exit_action.triggered.connect(self.close)
        main_menu.addAction(exit_action)

    def switch_to_video_editor(self):
        self.central_widget = VideoEditor(self)
        self.setCentralWidget(self.central_widget)

    def switch_to_format_conversion(self):
        self.central_widget = Format(self)
        self.setCentralWidget(self.central_widget)

def run_app():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app()
