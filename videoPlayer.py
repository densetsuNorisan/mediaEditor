from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QTimer

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

if __name__ == '__main__':
    app = QApplication([])
    video_path = 'test.mp4'
    player = VideoPlayer(video_path)
    player.show()
    app.exec_()
