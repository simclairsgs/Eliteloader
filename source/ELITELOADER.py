from sys import exit, argv, stdout
from os import path as os_path
import requests
from re import search, match, sub
import wget
from PyQt5.QtCore import QRect, QMetaObject, Qt, QCoreApplication, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QWidget, QComboBox, QCheckBox, QLabel, QGroupBox, \
    QRadioButton, QPushButton, QProgressBar, QMenuBar, QStatusBar, QLineEdit, QMenu, QAction, QApplication, \
    QStackedWidget
from PyQt5.QtGui import QFont, QIcon
from pytube import YouTube
from threading import Thread
from multiprocessing import process

"""
             Elites's ELITELOADER [ Downloads Youtube,Facebook,Instagram and any other Mp4 Videos ]
                                     Version-[0.1.1]  -->   Release-[R5-22-20]
                                     
                                                                                Developed By
                                                                            GEORGE SIMCLAIR SAM,
                                                                                Elite Coders.
                                                                                    Contact:
                                                                              simclair.sgs@gmail.com
"""

BLOCK_SIZE: int = 1024


class DataBus(dict):
    """Acts as a data transfer channel (Bus)"""
    def __init__(self):
        super().__init__()
        self = dict()

    def add(self, key, value):
        self[key] = value


class PageWindow(QMainWindow):  # for window or page transition
    gotoSignal = pyqtSignal(str)

    def goto(self, name):
        self.gotoSignal.emit(name)


class UiYoutube(PageWindow):  # Youtube UI and Youtube Download Manager

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("Youtube Downloader")

    def initUI(self):
        self.setupUi(self)

    def UiTest(self):                                   # Used for testing UI
        self.progressBar.setVisible(True)
        self.pushButton.setVisible(False)
        self.groupBox_for_videoFormats.setVisible(False)
        self.groupBox_for_typeSelection.setVisible(False)
        self.label_for_SizeDisplay.setVisible(True)
        self.label_for_FilenameDisplay.setVisible(True)

    def type_vid(self):                                     # Executed, if the type video is selected
        """ Changes the UI for video downloading """
        self.groupBox_for_typeSelection.setVisible(False)
        self.groupBox_for_videoFormats.setVisible(True)
        self.resolution_comboBox.setVisible(True)
        self.pushButton.setVisible(True)
        self.progressive_checkbox.setVisible(True)
        QMessageBox.question(self, 'NOTE', "HD Videos are stored separately as Audio and Only Video "
                                                     "formats in youtube.\nUse High"
                                                     " resolution option to download HD video and combine it with"
                                                     " audio with FFMPEG for best result.\n**-->>SD(480p-) videos "
                                                     "are available in combined form.", QMessageBox.Ok)
        TYPE = "video"
        data.add('type', TYPE)
        print('Type -> video proceeding to qual,format setup')

    def type_aud(self):                             # Executed, if the type Audio is selected
        """ Establishes connection and downloads audio """
        print('Type audio -> ask loc and start download')
        TYPE = "audio"
        data.add('type', TYPE)
        self.groupBox_for_typeSelection.setVisible(False)
        self.Title_label.setText('PLEASE WAIT...\nStarting Download..')
        path_to_save = QFileDialog.getExistingDirectory()
        print(path_to_save)
        data.add('loc', path_to_save)
        print(data, '@ type aud')
        try:
            yt = YouTube(data.get('url'))
            aud_stream = yt.streams.filter(type='audio').first()    # Establish connection and gets audio stream
        except:
            print('OOPs!')
            QMessageBox.question(self, 'ELITE', 'Server Connection Failed!!',
                                           QMessageBox.Ok)
            exit(0)
        if aud_stream is None:                                          # Check if audio stream is available
            print('SGS_ERROR-404_NO_STREAM')
            QMessageBox.question(self, 'ELITE', 'Selected Stream not available\nPing Streams'
                                                          ' from other menu or retry a different stream',
                                           QMessageBox.Ok)
            exit(0)
        else:
            try:
                aud_stream.download(str(data.get('loc')))               # Download in given location
                print('SGS_CODE_SUCCESS')
                QMessageBox.question(self, 'ELITE', 'Download succesful !!!',
                                               QMessageBox.Ok)
            except:
                print('ERROR_IN_DOWNLOAD')
                QMessageBox.question(self, 'ELITE', 'Download Failed !!!',
                                               QMessageBox.Ok)
                exit(0)
        exit(0)

    def progress_check(self, stream=None, chunk=None, remaining=None):
        """ Computes percentage for displaying in progressbar """
        percentage = (100 * (data.get('size') - remaining)) / data.get('size')
        self.progressBar.setValue(int(percentage))

    def download_manager_vid(self):  # Downloads Youtube videos
        """ Establishes connection and selects reqd. stream and downloads it """
        try:
            yt = YouTube(data.get('url'), on_progress_callback=self.progress_check)
        except:
            print('internet??')
            return 'Server Connection failed! \nCheck Internet and URL'
        resolution = data.get('qual')
        format = data.get('format')
        path = data.get('loc')
        Progressive_or_not = data.get('ext')
        if Progressive_or_not:
            if resolution == 'any' and format == 'mp4':
                self.selected_stream = yt.streams.filter(progressive=Progressive_or_not, file_extension=format).order_by('resolution').last()
            elif format == 'any' and resolution == 'any':
                self.selected_stream = yt.streams.filter(progressive=Progressive_or_not).order_by('resolution').last()
            else:
                self.selected_stream = yt.streams.filter(progressive=Progressive_or_not, file_extension=format).get_by_resolution(resolution)
        if not Progressive_or_not:
            if resolution == 'any' and format == 'mp4':
                self.selected_stream = yt.streams.filter(type='video', file_extension=format).order_by('resolution').last()
            elif format == 'any' and resolution == 'any':
                self.selected_stream = yt.streams.filter(type='video').order_by('resolution').last()
            else:
                self.selected_stream = yt.streams.filter(file_extension=format).get_by_resolution(resolution)
        if self.selected_stream is None:
            print('SGS_ERROR-404_NO_STREAM')
            return 'Selected Stream not available\nPing Streams' + 'from other menu or retry a different stream'
        data.add('size', self.selected_stream.filesize)
        self.selected_stream.download(path)
        print('SGS_CODE_SUCCESS')
        return 'Download Successful !!'

    def get_VideoSpecs(self):
        """Gets Video specifications and location and adjusts UI accordingly"""
        if self.mp4_radioButton.isChecked():
            print('Mp4 is selected -- proceed 147')
            data.add('format', 'mp4')
        elif self.webm_radioButton.isChecked():
            print('WEBM is selected -- proceed 149')
            data.add('format', 'webm')
        else:
            data.add('format', 'any')
        QUALITY = str(self.resolution_comboBox.currentText())
        data.add('qual', QUALITY)
        if self.progressive_checkbox.isChecked():
            data.add('ext', False)
            print('Progressive - False')
        else:
            data.add('ext', True)
            print('Progressive - True')
        print(data.get('format'), data.get('qual'), data.get('ext'), "End of info collection")
        self.groupBox_for_videoFormats.setVisible(False)
        self.pushButton.setVisible(False)
        self.progressive_checkbox.setVisible(False)
        self.resolution_comboBox.setVisible(False)
        self.Title_label.setText('PLEASE WAIT...\nStarting Download...')
        self.Title_label.setVisible(True)
        try:
            yt = YouTube(data.get('url'))
        except:
            QMessageBox.question(self, 'ELITE', 'Server Connection Failed!!\nCheck url or Internet',
                                           QMessageBox.Ok)
            print('internet??')
            exit(0)
        resolution = data.get('qual')
        format = data.get('format')
        Progressive_or_not = data.get('ext')
        if Progressive_or_not:
            if resolution == 'any' and format == 'mp4':
                selected_stream = yt.streams.filter(progressive=Progressive_or_not, file_extension=format).order_by('resolution').last()
            elif format == 'any' and resolution == 'any':
                selected_stream = yt.streams.filter(progressive=Progressive_or_not).order_by('resolution').last()
            else:
                selected_stream = yt.streams.filter(progressive=Progressive_or_not, file_extension=format).get_by_resolution(resolution)
        if not Progressive_or_not:
            if resolution == 'any' and format == 'mp4':
                selected_stream = yt.streams.filter(type='video', file_extension=format).order_by('resolution').last()
            elif format == 'any' and resolution == 'any':
                selected_stream = yt.streams.filter(type='video').order_by('resolution').last()
            else:
                selected_stream = yt.streams.filter(file_extension=format).get_by_resolution(resolution)
        if selected_stream is None:
            QMessageBox.question(self, 'ELITE', 'Selected Stream not available\nPing Streams'
                                                          ' from other menu or retry a different stream',
                                           QMessageBox.Ok)
            print('SGS_ERROR-404_NO_STREAM @ 484')
            exit(0)
        filesize = (selected_stream.filesize) * (10 ** -6)
        filename = selected_stream.default_filename
        self.label_for_SizeDisplay.setText("FILE SIZE: " + str(round(filesize, 2)) + ' MB')
        self.label_for_SizeDisplay.setVisible(True)
        self.label_for_FilenameDisplay.setText('VIDEO NAME: ' + str(filename))
        self.label_for_FilenameDisplay.setVisible(True)
        self.progressBar.setVisible(True)
        self.pushButton_.setVisible(False)
        path_to_save = QFileDialog.getExistingDirectory(self)
        print(path_to_save)
        data.add('loc', path_to_save)
        print(data)
        message_from_func = self.download_manager_vid()
        QMessageBox.question(self, 'ELITE', message_from_func,
                                       QMessageBox.Ok)
        exit(0)

    def setupUi(self, youtube_setup):
        """Sets up the page UI"""
        youtube_setup.setObjectName("youtube_setup")
        self.centralwidget = QWidget(youtube_setup)
        self.centralwidget.setObjectName("centralwidget")
        self.resolution_comboBox = QComboBox(self.centralwidget)
        self.resolution_comboBox.setGeometry(QRect(410, 110, 100, 33))
        self.resolution_comboBox.setObjectName("resolution_comboBox")
        list_quality = ['any', '240p', '360p', '720p', '1080p']
        self.resolution_comboBox.addItems(list_quality)
        self.resolution_comboBox.setVisible(False)
        self.progressive_checkbox = QCheckBox(self.centralwidget)
        self.progressive_checkbox.setGeometry(QRect(20, 230, 350, 50))
        self.progressive_checkbox.setObjectName("check_box")
        self.progressive_checkbox.setVisible(False)
        self.Title_label = QLabel(self.centralwidget)
        self.Title_label.setGeometry(QRect(170, 10, 261, 51))
        self.label_for_SizeDisplay = QLabel(self.centralwidget)
        self.label_for_SizeDisplay.setGeometry(QRect(160, 160, 180, 41))
        self.label_for_SizeDisplay.setObjectName("label_for_SizeDisplay")
        self.label_for_SizeDisplay.setVisible(False)
        self.label_info = QLabel(self.centralwidget)
        self.label_info.setGeometry(QRect(20, 310, 260, 20))
        self.label_info.setObjectName("label_info")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.Title_label.setFont(font)
        self.Title_label.setObjectName("Title_label")
        self.groupBox_for_typeSelection = QGroupBox(self.centralwidget)
        self.groupBox_for_typeSelection.setGeometry(QRect(200, 90, 191, 121))
        self.groupBox_for_typeSelection.setObjectName("groupBox_for_typeSelection")
        self.type_audio_radioButton = QRadioButton(self.groupBox_for_typeSelection)
        self.type_audio_radioButton.setGeometry(QRect(40, 40, 104, 23))
        self.type_audio_radioButton.setObjectName("type_audio_radioButton")
        self.type_audio_radioButton.clicked.connect(lambda: self.type_aud())
        self.type_video_radioButton = QRadioButton(self.groupBox_for_typeSelection)
        self.type_video_radioButton.setGeometry(QRect(40, 70, 104, 23))
        self.type_video_radioButton.setObjectName("type_video_radioButton")
        self.type_video_radioButton.clicked.connect(lambda: self.type_vid())
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QRect(460, 290, 88, 33))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setVisible(False)
        self.pushButton.clicked.connect(lambda: self.get_VideoSpecs())
        self.pushButton_ = QPushButton(self.centralwidget)
        self.pushButton_.setGeometry(QRect(460, 290, 88, 33))
        self.pushButton_.setObjectName("pushButton")
        self.pushButton_.setVisible(False)
        self.pushButton_.clicked.connect(lambda: self.YoutubeManager.download_manager_vid(self))
        self.groupBox_for_videoFormats = QGroupBox(self.centralwidget)
        self.groupBox_for_videoFormats.setGeometry(QRect(200, 90, 141, 111))
        self.groupBox_for_videoFormats.setObjectName("groupBox_for_videoFormats")
        self.groupBox_for_videoFormats.setVisible(False)
        self.mp4_radioButton = QRadioButton(self.groupBox_for_videoFormats)
        self.mp4_radioButton.setGeometry(QRect(20, 30, 104, 23))
        self.mp4_radioButton.setObjectName("mp4_radioButton")
        self.webm_radioButton = QRadioButton(self.groupBox_for_videoFormats)
        self.webm_radioButton.setGeometry(QRect(20, 60, 104, 23))
        self.webm_radioButton.setObjectName("webm_radioButton")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QRect(90, 230, 391, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setVisible(False)
        self.label_for_FilenameDisplay = QLabel(self.centralwidget)
        self.label_for_FilenameDisplay.setGeometry(QRect(75, 110, 500, 50))
        self.label_for_FilenameDisplay.setObjectName("label_for_FilenameDisplay")
        self.label_for_FilenameDisplay.setVisible(False)
        youtube_setup.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(youtube_setup)
        self.menubar.setGeometry(QRect(0, 0, 586, 25))
        self.menubar.setObjectName("menubar")
        youtube_setup.setMenuBar(self.menubar)
        self.progressBar.setValue(0)
        self.statusbar = QStatusBar(youtube_setup)
        self.statusbar.setObjectName("statusbar")
        youtube_setup.setStatusBar(self.statusbar)

        self.retranslateUi(youtube_setup)
        QMetaObject.connectSlotsByName(youtube_setup)

    def retranslateUi(self, youtube_setup):
        _translate = QCoreApplication.translate
        youtube_setup.setWindowTitle(_translate("youtube_setup", "Youtube Video Download-ELITELOADER"))
        self.Title_label.setText(_translate("youtube_setup", "Select Format and Quality"))
        self.label_for_SizeDisplay.setText(_translate("ELITE", "SIZE:"))
        self.label_for_FilenameDisplay.setText(_translate("ELITE", "FILENAME:"))
        self.groupBox_for_typeSelection.setTitle(_translate("youtube_setup", "Type"))
        self.progressive_checkbox.setText(_translate('youtube_setup', "High Resolution/Non-Progressive"))
        self.type_audio_radioButton.setText(_translate("youtube_setup", "Audio"))
        self.label_info.setText(_translate("StartPage_Url", "*This checking process may take longer"))
        self.type_video_radioButton.setText(_translate("youtube_setup", "Video"))
        self.pushButton.setText(_translate("youtube_setup", "Proceed"))
        self.pushButton_.setText(_translate("youtube_setup", "Download"))
        self.groupBox_for_videoFormats.setTitle(_translate("youtube_setup", "Format"))
        self.mp4_radioButton.setText(_translate("youtube_setup", "MP4"))
        self.webm_radioButton.setText(_translate("youtube_setup", "WEBM"))

    class YoutubeManager:  # Manage Youtube Downloads
        def __init__(self):
            pass

        def ping(self):  # Check Available Streams and returns a list of streams
            try:
                yt = YouTube(data.get('url'))
                pingster = yt.streams.all()
                return pingster
            except:
                print('Error in connection')
                return 'Error in connection\nCheck URL and Internet'


class UiInstagram(PageWindow):  # UI for Instagram ,Downloads Instagram Video
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle(" INSTAGRAM - ELITELOADER")

    def initUI(self):
        self.setupUi(self)

    def is_connected(self, test_url: str = "https://instagram.com", timeout: int = 2) -> bool:
        """ Checks Internet Connection
            returns-Bool value
        """
        try:
            test_connection = requests.get(test_url, timeout=timeout)
            test_connection.raise_for_status()
            return True
        except requests.HTTPError as error:
            print("http error")
            QMessageBox.question(self, "Error", 'http error', QMessageBox.Ok)
        except requests.exceptions.ConnectionError:
            print("An error happened when trying to establish a connection to Instagram.")
            QMessageBox.question(self, "Error", 'http error', QMessageBox.Ok)
        return False

    def is_instagram_domain(self, post_url: str = None) -> bool:
        """ Check if its a insta domain
            returns-Bool value
        """
        is_match = match(r"^(https:)[/][/]www.([^/]+[.])*instagram.com", post_url)
        if is_match:
            return True
        else:
            return False

    def determine_media_type(self, media_content: str = None) -> str:
        """ Determines the media type
            returns-media type (image or video)
        """
        content_type_header: str = search(
            r'<meta name="medium" content=[\'"]?([^\'" >]+)', media_content
        ).group()
        content_type = sub(r'<meta name="medium" content="', "", content_type_header)
        return content_type

    def extract_video_direct_link(self, media_content: str = None) -> str:
        """ Gets direct url of the video """
        image_link_header: str = search(
            r'meta property="og:video" content=[\'"]?([^\'" >]+)', media_content
        ).group()
        video_link: str = sub(r'meta property="og:video" content="', "", image_link_header)
        return video_link

    def download_video(self, post_content: str = None) -> None:
        """ Downloads the video and displays progressbar"""
        try:
            video_direct_url: str = self.extract_video_direct_link(post_content)
            video_content = requests.get(video_direct_url, stream=True)
            video_size = int(video_content.headers["Content-Length"])
            video_file_path = data.get('loc')
            self.label_for_Size.setText("SIZE: " + str(round(video_size * (0.000001), 3)) + ' MB')
            downloaded = 0
            with open(video_file_path, "wb") as video_file:
                for data_block in video_content.iter_content(BLOCK_SIZE):
                    downloaded += len(data_block)
                    video_file.write(data_block)
                    pct = (downloaded/video_size)*100
                    self.progressBar.setValue(int(pct))
        except:
            QMessageBox.question(self, "Error", "Download Failed!!", QMessageBox.Ok)
            exit(0)

    def main(self, url):
        """ Checks URL and connetion """
        if not self.is_connected():
            QMessageBox.question(self, "Error", "Download Failed!!", QMessageBox.Ok)
            exit()
        if not self.is_instagram_domain(url):
            QMessageBox.question(self, "Error", "Download Failed!!", QMessageBox.Ok)
            exit()
        media_content = requests.get(url).content.decode("utf-8")
        media_type = self.determine_media_type(media_content)
        if media_type == "image":
           print("image link found")
           exit(0)
        elif media_type == "video":
            self.download_video(media_content)
        else:
            QMessageBox.question(self, "Error", "Download Failed!!", QMessageBox.Ok)
            exit()

    def Initiate_Download(self, url):
        self.main(url)
        exit(0)

    def download(self):
        """ Changes UI"""
        self.progressBar.setVisible(True)
        self.pushButton.setVisible(False)
        self.label_for_Size.setVisible(True)
        self.label_info.setVisible(False)
        self.Title_label.setText("Starting Download..\nPlease wait...")
        url = data.get('url')
        self.t = Thread(target=self.Initiate_Download(url))
        self.t.start()
        process.join()

    def setupUi(self, general_vidloader):
        """ Sets up UI"""
        general_vidloader.setObjectName("general_vidloader")
        self.centralwidget = QWidget(general_vidloader)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QRect(110, 150, 381, 25))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setVisible(False)
        self.progressBar.setValue(0)
        self.Title_label = QLabel(self.centralwidget)
        self.Title_label.setGeometry(QRect(170, 10, 261, 51))
        self.label_for_Size = QLabel(self.centralwidget)
        self.label_for_Size.setGeometry(QRect(220, 200, 180, 41))
        self.label_for_Size.setObjectName("label_for_SizeDisplay")
        self.label_for_Size.setVisible(False)
        self.Title_label = QLabel(self.centralwidget)
        self.Title_label.setGeometry(QRect(230, 20, 230, 41))
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.Title_label.setFont(font)
        self.Title_label.setObjectName("Title_label")
        self.label_info = QLabel(self.centralwidget)
        self.label_info.setGeometry(QRect(30, 300, 271, 17))
        self.label_info.setObjectName("label_info")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QRect(430, 220, 88, 33))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.download())
        general_vidloader.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(general_vidloader)
        self.menubar.setGeometry(QRect(0, 0, 586, 25))
        self.menubar.setObjectName("menubar")
        general_vidloader.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(general_vidloader)
        self.statusbar.setObjectName("statusbar")
        general_vidloader.setStatusBar(self.statusbar)

        self.retranslateUi(general_vidloader)
        QMetaObject.connectSlotsByName(general_vidloader)

    def retranslateUi(self, general_vidloader):
        _translate = QCoreApplication.translate
        general_vidloader.setWindowTitle(_translate("general_vidloader", "Insta video downloader - ELITELOADER"))
        self.Title_label.setText(_translate("general_vidloader", "Continue.. ?"))
        self.label_info.setText(_translate("general_vidloader", "*save file with reqd. name and extension"))
        self.pushButton.setText(_translate("general_vidloader", "Download"))
        self.label_for_Size.setText(_translate("ELITE", "SIZE:"))


class GeneralManager(PageWindow):  # Download Normal Video
    def __init__(self):
        super().__init__()
        self.initUI()
        self.BLOCK_SIZE: int = 1024
        self.setWindowTitle("ELITELOADER")

    def initUI(self):
        self.setupUi(self)

    def download(self):
        """ Downloads file and writes with Progressbar"""
        url = data.get('url')
        self.progressBar.setVisible(True)
        self.pushButton.setVisible(False)
        self.label_forSize.setVisible(True)
        self.label_info.setVisible(False)
        self.Title_label.setText("Starting Download..\nPlease wait...")
        try:
            response = requests.get(url, stream=True)
            total = response.headers.get('content-length')
            print('Total_size = ', total)
            with open(data.get('loc'), 'wb') as f:
                self.label_forSize.setText("FILE SIZE: " + str(round(float(total) * (0.000001), 3)) + ' MB')
                if total is None:
                    f.write(response.content)
                else:
                    downloaded = 0
                    total = int(total)
                    for datas in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                        downloaded += len(datas)
                        f.write(datas)
                        pct = downloaded/total*100
                        if downloaded <= total:
                            self.progressBar.setValue(int(pct))
                print('Download Successful !!!')
        except:
            QMessageBox.question(self, "Error", "Download Failed!!", QMessageBox.Ok)
        exit(0)

    def setupUi(self, general_vidloader):
        """ Sets up UI"""
        general_vidloader.setObjectName("general_vidloader")
        self.centralwidget = QWidget(general_vidloader)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QRect(110, 150, 381, 25))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setVisible(False)
        self.progressBar.setValue(0)
        self.Title_label = QLabel(self.centralwidget)
        self.Title_label.setGeometry(QRect(170, 10, 261, 51))
        self.label_forSize = QLabel(self.centralwidget)
        self.label_forSize.setGeometry(QRect(220, 200, 180, 41))
        self.label_forSize.setObjectName("label_for_SizeDisplay")
        self.label_forSize.setVisible(False)
        self.Title_label = QLabel(self.centralwidget)
        self.Title_label.setGeometry(QRect(230, 20, 230, 41))
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.Title_label.setFont(font)
        self.Title_label.setObjectName("Title_label")
        self.label_info = QLabel(self.centralwidget)
        self.label_info.setGeometry(QRect(30, 300, 271, 17))
        self.label_info.setObjectName("label_info")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QRect(430, 220, 88, 33))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.download())
        general_vidloader.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(general_vidloader)
        self.menubar.setGeometry(QRect(0, 0, 586, 25))
        self.menubar.setObjectName("menubar")
        general_vidloader.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(general_vidloader)
        self.statusbar.setObjectName("statusbar")
        general_vidloader.setStatusBar(self.statusbar)

        self.retranslateUi(general_vidloader)
        QMetaObject.connectSlotsByName(general_vidloader)

    def retranslateUi(self, general_vidloader):
        _translate = QCoreApplication.translate
        general_vidloader.setWindowTitle(_translate("general_vidloader", "Video downloader - ELITELOADER"))
        self.Title_label.setText(_translate("general_vidloader", "Continue.. ?"))
        self.label_info.setText(_translate("general_vidloader", "*save file with reqd. name and extension"))
        self.pushButton.setText(_translate("general_vidloader", "Download"))
        self.label_forSize.setText(_translate("ELITE", "SIZE:"))


class UiFacebook(PageWindow):  # Facebook UI
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("FaceBook - ELITELOADER")

    def initUI(self):
        self.setupUi(self)

    def Progressbar_Manager(self, current, total, width):
        pct = (current/total)*100
        self.progressBar.setValue(int(pct))

    def Download_H(self):  # For High Quality
        ERASE_LINE = '\x1b[2K'
        Location = os_path.join(data.get('loc'))
        try:
            html = requests.get(data.get('url'))
            hdvideo_url = search('hd_src:"(.+?)"', html.text)[1]
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error.")
            return 'Connection Error\n' + 'Check your Internet'
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            return 'Network Timeout'
        except requests.RequestException as e:
            print("OOPS!! General Error or Invalid URL")
            return 'General Error or Invalid URL'
        except (KeyboardInterrupt, SystemExit):
            print("Ok ok, quitting")
            exit(1)
        except TypeError:
            print("Video May be Private or Hd version not available")
            return 'Video May Private or Hd version not available'
        else:
            hd_url = hdvideo_url.replace('hd_src:"', '')
            print("\n")
            print("High Quality: " + hd_url)
            print("[+] Video Started Downloading")
            wget.download(hd_url, Location, bar=self.Progressbar_Manager)
            stdout.write(ERASE_LINE)
            print("\n")
            print("Video downloaded")
            return 'Video Downloaded Successfully !!'

    def Download_L(self):  # For Low Quality
        ERASE_LINE = '\x1b[2K'
        Location = os_path.join(data.get('loc'))
        try:
            html = requests.get(data.get('url'))
            sdvideo_url = search('sd_src:"(.+?)"', html.text)[1]
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error.")
            return 'Connection Error\n' + 'Check your Internet'
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            return 'Network Timeout'
        except requests.RequestException as e:
            print("OOPS!! General Error or Invalid URL")
            return 'General Error or Invalid URL'
        except (KeyboardInterrupt, SystemExit):
            print("Ok ok, quitting")
            exit(1)
        except TypeError:
            print("Video May Private or Invalid URL")
            return 'Video May be Private or Invalid URL'
        else:
            sd_url = sdvideo_url.replace('sd_src:"', '')
            print("\n")
            print("Normal Quality: " + sd_url)
            print("[+] Video Started Downloading")
            wget.download(sd_url, Location, bar=self.Progressbar_Manager)
            stdout.write(ERASE_LINE)
            print("\n")
            print("Video downloaded")
            return 'Video Downloaded Successfully !!'

    def Selector(self):
        """ Identifies which Quality is reqd."""
        if self.HighQual_radioButton.isChecked():
            print('HQ selected--fwding to manager')
            self.groupBox_forQuality.setVisible(False)
            self.pushButton.setVisible(False)
            self.label.setText('PLEASE WAIT..\nSTARTING DOWNLOAD...')
            sgs = QFileDialog.getExistingDirectory()
            print(sgs)
            data.add('loc', sgs)
            self.progressBar.setVisible(True)
            print(data)
            msg = self.Download_H()
            QMessageBox.question(self, 'ELITE', msg, QMessageBox.Ok)
            exit(0)

        if self.LowQual_radioButton.isChecked():
            print('LQ selected--fwding to manager')
            self.groupBox_forQuality.setVisible(False)
            self.pushButton.setVisible(False)
            self.label.setText('PLEASE WAIT..\nSTARTING DOWNLOAD...')
            sgs = QFileDialog.getExistingDirectory()
            print(sgs)
            data.add('loc', sgs)
            self.progressBar.setVisible(True)
            print(data)
            msg = self.Download_L()
            QMessageBox.question(self, 'ELITE', msg, QMessageBox.Ok)
            exit(0)

    def setupUi(self, facebook_dwn):
        facebook_dwn.setObjectName("facebook_dwn")
        facebook_dwn.resize(586, 379)
        self.centralwidget = QWidget(facebook_dwn)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QRect(220, 10, 250, 61))
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("Title_label")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QRect(460, 290, 88, 33))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.Selector())
        self.groupBox_forQuality = QGroupBox(self.centralwidget)
        self.groupBox_forQuality.setGeometry(QRect(200, 90, 141, 111))
        self.groupBox_forQuality.setObjectName("groupBox_for_videoFormats")
        self.HighQual_radioButton = QRadioButton(self.groupBox_forQuality)
        self.HighQual_radioButton.setGeometry(QRect(20, 30, 104, 23))
        self.HighQual_radioButton.setObjectName("mp4_radioButton")
        self.LowQual_radioButton = QRadioButton(self.groupBox_forQuality)
        self.LowQual_radioButton.setGeometry(QRect(20, 60, 104, 23))
        self.LowQual_radioButton.setObjectName("webm_radioButton")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QRect(110, 180, 391, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setVisible(False)
        facebook_dwn.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(facebook_dwn)
        self.menubar.setGeometry(QRect(0, 0, 586, 25))
        self.menubar.setObjectName("menubar")
        facebook_dwn.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(facebook_dwn)
        self.statusbar.setObjectName("statusbar")
        facebook_dwn.setStatusBar(self.statusbar)

        self.retranslateUi(facebook_dwn)
        QMetaObject.connectSlotsByName(facebook_dwn)

    def retranslateUi(self, facebook_dwn):
        _translate = QCoreApplication.translate
        facebook_dwn.setWindowTitle(_translate("facebook_dwn", "Facebook Video Download-ELITELOADER"))
        self.label.setText(_translate("facebook_dwn", "Select  Quality"))
        self.pushButton.setText(_translate("facebook_dwn", "Proceed"))
        self.groupBox_forQuality.setTitle(_translate("facebook_dwn", "Quality"))
        self.HighQual_radioButton.setText(_translate("facebook_dwn", "High Quality"))
        self.LowQual_radioButton.setText(_translate("facebook_dwn", "Low Quality"))


class UiStartPage(PageWindow):  # Starting Page UI
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("ELITELOADER")

    def initUI(self):
        self.setupUi(self)

    def ping(self):
        """ Pings youtube Streams"""
        data.add('url', self.url_txtbox.text())
        obj = UiYoutube.YoutubeManager()
        print('Please Wait..')
        QMessageBox.question(self, 'ELITE', 'It takes a while, please wait..', QMessageBox.Ok)
        streams = UiYoutube.YoutubeManager.ping(obj)
        if isinstance(streams, list):
            Mstream = ""
            for i in streams:
                Mstream += str(i) + '\n'
            QMessageBox.question(self, 'Streams', Mstream, QMessageBox.Ok)
            print(streams)
        if isinstance(streams, str):
            QMessageBox.question(self, 'ELITE', streams, QMessageBox.Ok)

    def TypeFinder(self):
        """ Identfies URL and calls resective pages"""
        print(self.url_txtbox.text(), 'All clear @ main page after getting link')
        data.add('url', self.url_txtbox.text())
        URl = self.url_txtbox.text()
        if URl != '':
            try:
                partition = URl.split('/')
                type = partition[2]
            except:
                QMessageBox.question(self, "ELITE_ERROR", 'Invalid URL !!!')
                exit(0)
            if type == 'www.youtube.com':
                print("Youtube link is found -> fwding to youtube page ")
                self.goto("Youtube")
            elif type == 'youtu.be':
                print("Youtube link is found -> fwding to youtube page ")
                self.goto("Youtube")
            elif type == 'www.facebook.com':
                print("facebook link is found -> forwarding to fb page ")
                self.goto("fb_setup")
            elif type == 'www.instagram.com':
                sg = QFileDialog.getSaveFileName(self)
                data.add('loc', sg[0])
                print("instagram link is found -> forwarding to insta page ")
                self.goto("insta")
            else:
                sg = QFileDialog.getSaveFileName(self)
                data.add('loc', sg[0])
                print(data, 'Before General manage call')
                self.goto("general")

    def setupUi(self, StartPage_Url):
        StartPage_Url.setObjectName("StartPage_Url")
        self.centralwidget = QWidget(StartPage_Url)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_go = QPushButton(self.centralwidget)
        self.btn_go.setGeometry(QRect(250, 150, 88, 33))
        self.btn_go.setObjectName("btn_go")
        self.btn_go.clicked.connect(lambda: self.TypeFinder())
        self.L_Heading = QLabel(self.centralwidget)
        self.L_Heading.setGeometry(QRect(120, 20, 331, 20))
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.L_Heading.setFont(font)
        self.L_Heading.setLayoutDirection(Qt.LeftToRight)
        self.L_Heading.setAutoFillBackground(True)
        self.L_Heading.setObjectName("L_Heading")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QRect(20, 200, 231, 111))
        self.groupBox.setObjectName("groupBox_for_typeSelection")
        self.label = QLabel(self.groupBox)
        self.label.setGeometry(QRect(40, 20, 111, 17))
        self.label.setObjectName("Title_label")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setGeometry(QRect(40, 40, 121, 17))
        self.label_2.setObjectName("label_info")
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setGeometry(QRect(40, 60, 141, 20))
        self.label_5.setObjectName("label_5")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setGeometry(QRect(40, 80, 141, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setGeometry(QRect(200, 310, 451, 20))
        self.label_4.setObjectName("label_info")
        self.url_txtbox = QLineEdit(self.centralwidget)
        self.url_txtbox.setGeometry(QRect(72, 70, 431, 33))
        self.url_txtbox.setObjectName("url_txtbox")
        self.url_txtbox.returnPressed.connect(self.TypeFinder)
        StartPage_Url.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(StartPage_Url)
        self.menubar.setGeometry(QRect(0, 0, 586, 25))
        self.menubar.setObjectName("menubar")
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.about_opt = QMenu(self.menubar)
        self.about_opt.setObjectName("about_opt")
        StartPage_Url.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(StartPage_Url)
        self.statusbar.setObjectName("statusbar")
        StartPage_Url.setStatusBar(self.statusbar)
        self.pings = QAction(StartPage_Url)
        self.pings.setObjectName("pings")
        self.menuAbout.addAction(self.pings)
        self.pings.triggered.connect(lambda: self.ping())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.retranslateUi(StartPage_Url)
        QMetaObject.connectSlotsByName(StartPage_Url)

    def retranslateUi(self, StartPage_Url):
        _translate = QCoreApplication.translate
        StartPage_Url.setWindowTitle(_translate("StartPage_Url", "ELITELOADER"))
        self.btn_go.setText(_translate("StartPage_Url", "Go"))
        self.L_Heading.setText(_translate("StartPage_Url", "General purpose video downloader"))
        self.groupBox.setTitle(_translate("StartPage_Url", "Downloadable Items"))
        self.label.setText(_translate("StartPage_Url", "# Youtube videos"))
        self.label_2.setText(_translate("StartPage_Url", "# Facebook videos"))
        self.label_5.setText(_translate("StartPage_Url", "# Instagram videos"))
        self.label_3.setText(_translate("StartPage_Url", "# Mp4 with source url"))
        self.label_4.setText(_translate("StartPage_Url", "*This app auto detects the url type and proceeds accordingly"))
        self.menuAbout.setTitle(_translate("StartPage_Url", "Available streams"))
        self.about_opt.setTitle(_translate("StartPage_Url", "About"))
        self.pings.setText(_translate("StartPage_Url", "Ping Youtube Streams"))


class Window(QMainWindow):  # For Managing Windows and transition
    def __init__(self, parent=None):
        """ Creates Qstacked Widgets and registers available pages"""
        super().__init__(parent)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.setGeometry(250, 250, 600, 389)
        self.m_pages = {}

        self.register(UiStartPage(), "main")
        self.register(UiYoutube(), "Youtube")
        self.register(UiFacebook(), "fb_setup")
        self.register(UiInstagram(), "insta")
        self.register(GeneralManager(), "general")
        self.goto("main")

    def register(self, widget, name):
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageWindow):
            widget.gotoSignal.connect(self.goto)

    @pyqtSlot(str)
    def goto(self, name):
        """ Window transition"""
        if name in self.m_pages:
            widget = self.m_pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())


if __name__ == "__main__":  # Execution Starts here
    data = DataBus()
    app = QApplication(argv)
    w = Window()
    w.setWindowIcon(QIcon("icon.png"))
    w.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
    process = Thread(target=w.show())
    process.start()
    app.exit(0)
    exit(app.exec_())
