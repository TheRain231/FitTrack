import sys
from pathlib import Path

from PyQt6.QtCore import QEvent, QSize, Qt, QUrl
from PyQt6.QtGui import QFont
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (
    QApplication, QAbstractItemView, QButtonGroup, QFileDialog, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QScrollArea, QStackedWidget, QVBoxLayout, QWidget,
)


VIDEO_DIR = Path(__file__).resolve().parent / 'videos'

BACK_EXERCISES = {
    'Тяга верхнего блока к груди': {
        'sets': 2,
        'reps': '8–12 повторений',
        'rest': '120 сек между подходами',
        'duration': '32–48 сек на подход',
        'note': 'Подбирай вес, с которым получается двигаться плавно и без рывков.',
        'video': 'lat_pulldown.mp4',
    },
    'Горизонтальная тяга блока': {
        'sets': 2,
        'reps': '8–12 повторений',
        'rest': '120 сек между подходами',
        'duration': '32–48 сек на подход',
        'note': 'Начни с небольшой нагрузки и сохраняй контроль над движением.',
        'video': 'seated_row.mp4',
    },
    'Тяга гантели одной рукой': {
        'sets': 2,
        'reps': '8–12 повторений',
        'rest': '120 сек после обеих сторон',
        'duration': '64–96 сек на обе стороны',
        'note': 'Повторения указаны для каждой руки. Один подход включает обе стороны; '
                'при смене руки можно сделать короткую паузу по необходимости.',
        'video': 'one_arm_row.mp4',
    },
    'Гиперэкстензия': {
        'sets': 2,
        'reps': '8–12 повторений',
        'rest': '90 сек между подходами',
        'duration': '32–48 сек на подход',
        'note': 'Для знакомства с упражнением начни без дополнительного отягощения.',
        'video': 'hyperextension.mp4',
    },
    'Тяга прямыми руками в кроссовере': {
        'sets': 2,
        'reps': '8–12 повторений',
        'rest': '90 сек между подходами',
        'duration': '32–48 сек на подход',
        'note': 'Выбирай небольшой вес, который позволяет контролировать движение.',
        'video': 'straight_arm_pulldown.mp4',
    },
}

STYLE = """
QMainWindow, QWidget#centralwidget { background-color: #17191b; }
QWidget { color: #f4f5f2; font-family: "Arial"; font-size: 14px; }
QLabel#brandLabel { font-size: 34px; font-weight: 700; }
QLabel#subtitleLabel { color: #a5aaa9; font-size: 15px; }
QLabel#catalogInfoLabel {
    color: #bddf91; background: #242e20; border-radius: 12px;
    padding: 9px 14px; font-size: 12px;
}
QLabel#categoryHeadingLabel { color: #a5aaa9; font-size: 12px; }
QLineEdit {
    background: #101214; border: 1px solid #393d40; border-radius: 14px;
    padding: 0px 18px; color: #f4f5f2; font-size: 16px;
    selection-background-color: #b8dc8b; selection-color: #17191b;
}
QLineEdit:focus { border: 1px solid #b8dc8b; }
QPushButton {
    background: #202326; border: 1px solid #393d40; border-radius: 14px;
    padding: 10px 18px; color: #edf0ea; font-size: 15px;
}
QPushButton:hover { background: #2a302b; border-color: #6b795e; }
QPushButton:pressed { background: #36412e; }
QPushButton:checked {
    background: #b8dc8b; color: #192012; border-color: #b8dc8b; font-weight: 700;
}
QPushButton:focus { border: 1px solid #b8dc8b; }
QPushButton#allExercisesButton { font-size: 13px; padding: 10px 16px; }
QLabel#sectionTitleLabel { font-size: 23px; font-weight: 700; }
QLabel#resultCountLabel { color: #a5aaa9; font-size: 13px; }
QListWidget { background: transparent; border: none; outline: none; }
QListWidget::item {
    background: #222528; border: 1px solid #303538;
    border-radius: 14px; padding: 16px; margin-bottom: 10px;
}
QListWidget::item:hover { border-color: #6b795e; }
QListWidget::item:selected { background: #2b3525; border-color: #b8dc8b; }
QFrame#exerciseCard {
    background: #222528; border: 1px solid #303538; border-radius: 14px; margin-bottom: 10px;
}
QLabel#exerciseName { background: transparent; font-size: 16px; font-weight: 700; }
QLabel#exerciseMeta { background: transparent; color: #a5aaa9; font-size: 13px; }
QLabel#emptyStateLabel { color: #a5aaa9; padding: 18px; font-size: 15px; }
QLabel#footerLabel { color: #838a88; font-size: 12px; }
QScrollBar:vertical { background: #17191b; width: 10px; margin: 0px; }
QScrollBar::handle:vertical { background: #465044; border-radius: 5px; min-height: 32px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }

            QDialog { background: #17191b; }
            QWidget { color: #f4f5f2; font-family: Arial; font-size: 14px; }
            QLabel#exerciseTitle { font-size: 25px; font-weight: 700; }
            QLabel#muted, QLabel#videoHint, QLabel#videoStatus { color: #a5aaa9; font-size: 13px; }
            QLabel#videoPlaceholderTitle { font-size: 20px; font-weight: 700; }
            QWidget#videoPlaceholder { background: #101214; border-radius: 14px; }
            QFrame#statCard { background: #222528; border-radius: 12px; }
            QLabel#statCaption { color: #a5aaa9; font-size: 12px; }
            QLabel#statValue { color: #c4e69e; font-size: 17px; font-weight: 700; }
            QPushButton {
                background: #252a25; border: 1px solid #465044;
                border-radius: 10px; padding: 10px 16px;
            }
            QPushButton:hover { background: #36412e; }
            QPushButton:disabled { color: #777e78; border-color: #303733; }
            QPushButton#chooseVideoButton { background: #b8dc8b; color: #192012; font-weight: 700; }

QWidget#catalogPage, QWidget#detailContents, QStackedWidget#pages { background: #17191b; }
QScrollArea { border: none; background: #17191b; }
QPushButton#videoPlaceholder {
    background: #101214; border: 1px dashed #465044; border-radius: 14px;
    font-size: 20px; font-weight: 700; color: #f4f5f2;
}
QPushButton#videoPlaceholder:hover { border-color: #b8dc8b; background: #1c231a; }
QLabel#noticeLabel { color: #c4e69e; padding: 6px; }
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FitTrack')
        self.resize(1100, 840)
        self.setMinimumSize(760, 640)
        self.setStyleSheet(STYLE)
        self.exercises = [
            ('Тяга верхнего блока к груди', 'Спина', 'Тренажёр'),
            ('Горизонтальная тяга блока', 'Спина', 'Тренажёр'),
            ('Тяга гантели одной рукой', 'Спина', 'Гантель'),
            ('Гиперэкстензия', 'Спина', 'Скамья для гиперэкстензии'),
            ('Тяга прямыми руками в кроссовере', 'Спина', 'Кроссовер'),

            ('Жим гантелей лёжа', 'Грудь', 'Гантели'),
            ('Отжимание от пола', 'Грудь', 'Собственный вес'),
            ('Жим гантелей на наклонной скамье', 'Грудь', 'Гантели и наклонная скамья'),
            ('Сведение рук в тренажёре «Бабочка»', 'Грудь', 'Тренажёр'),
            ('Сведение рук в кроссовере', 'Грудь', 'Кроссовер'),

            ('Жим ногами в тренажёре', 'Ноги', 'Тренажёр'),
            ('Приседание', 'Ноги', 'Собственный вес'),
            ('Разгибание ног в тренажёре', 'Ноги', 'Тренажёр'),
            ('Сгибание ног в тренажёре', 'Ноги', 'Тренажёр'),
            ('Подъём на носки', 'Ноги', 'Собственный вес'),

            ('Кошка-корова', 'Реабилитация', 'Коврик'),
            ('Ягодичный мостик', 'Реабилитация', 'Коврик'),
            ('Разгибание ноги сидя', 'Реабилитация', 'Стул'),
            ('Отжимание от стены', 'Реабилитация', 'Стена'),
            ('Подъём на носки с опорой', 'Реабилитация', 'Стул или стена'),

            ('Растяжка икроножных мышц у стены', 'Растяжка', 'Стена'),
            ('Растяжка передней поверхности бедра', 'Растяжка', 'Без оборудования'),
            ('Растяжка задней поверхности бедра сидя', 'Растяжка', 'Коврик'),
            ('Растяжка грудных мышц у стены', 'Растяжка', 'Стена'),
            ('Растяжка ягодичных мышц лёжа', 'Растяжка', 'Коврик'),

            ('Отжимания от стены', 'Для начинающих', 'Стена'),
            ('Приседания до стула', 'Для начинающих', 'Стул'),
            ('Ягодичный мостик', 'Для начинающих', 'Коврик'),
            ('Подъём коленей на месте', 'Для начинающих', 'Без оборудования'),
            ('Подъём противоположных руки и ноги на четвереньках', 'Для начинающих', 'Коврик'),
        ]
        self.show_all = False
        self.current_exercise = None
        self.video_paths = {}


        self.pages = QStackedWidget()
        self.pages.setObjectName('pages')
        self.setCentralWidget(self.pages)
        self.create_catalog_page()
        self.create_exercise_page()

        self.player = QMediaPlayer(self)
        self.audioOutput = QAudioOutput(self)
        self.audioOutput.setVolume(0.5)
        self.player.setAudioOutput(self.audioOutput)
        self.player.setVideoOutput(self.videoWidget)
        self.player.playbackStateChanged.connect(self.update_play_button)
        self.player.errorOccurred.connect(self.show_video_error)
        self.videoWidget.installEventFilter(self)
        self.playButton.setEnabled(False)
        self.stopButton.setEnabled(False)

        self.category_group = QButtonGroup(self)
        self.category_group.setExclusive(True)
        for button in self.buttons:
            self.category_group.addButton(button)
            button.clicked.connect(self.filter_exercises)
        self.searchEdit.textChanged.connect(self.filter_exercises)
        self.allExercisesButton.clicked.connect(self.show_all_exercises)
        self.exerciseList.itemClicked.connect(self.open_exercise)
        self.exerciseList.itemActivated.connect(self.open_exercise)
        self.exerciseList.installEventFilter(self)
        self.backToListButton.clicked.connect(self.show_catalog)
        self.videoPlaceholder.clicked.connect(self.choose_video)
        self.chooseVideoButton.clicked.connect(self.choose_video)
        self.playButton.clicked.connect(self.toggle_video)
        self.stopButton.clicked.connect(self.player.stop)
        self.filter_exercises()
        self.pages.setCurrentWidget(self.catalogPage)

    def create_catalog_page(self):
        self.catalogPage = QWidget()
        self.catalogPage.setObjectName('catalogPage')
        layout = QVBoxLayout(self.catalogPage)
        layout.setContentsMargins(32, 26, 32, 22)
        layout.setSpacing(16)

        header = QHBoxLayout()
        brand = QLabel('FitTrack')
        brand.setObjectName('brandLabel')
        header.addWidget(brand)
        header.addStretch()
        catalog_info = QLabel('30 упражнений · 6 категорий')
        catalog_info.setObjectName('catalogInfoLabel')
        header.addWidget(catalog_info)
        layout.addLayout(header)
        subtitle = QLabel('Упражнения и комплексы для твоих целей')
        subtitle.setObjectName('subtitleLabel')
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        self.searchEdit = QLineEdit()
        self.searchEdit.setMinimumHeight(56)
        self.searchEdit.setPlaceholderText('Поиск по названию, категории или оборудованию…')
        self.searchEdit.setClearButtonEnabled(True)
        self.searchEdit.setAccessibleName('Поиск упражнений')
        layout.addWidget(self.searchEdit)
        heading = QLabel('ВЫБЕРИ КАТЕГОРИЮ')
        heading.setObjectName('categoryHeadingLabel')
        layout.addWidget(heading)

        grid = QGridLayout()
        grid.setSpacing(12)
        self.buttons = []
        categories = [
            ('backButton', 'Спина'), ('chestButton', 'Грудь'), ('legsButton', 'Ноги'),
            ('rehabButton', 'Реабилитация'), ('stretchButton', 'Растяжка'),
            ('beginnerButton', 'Для начинающих'),
        ]
        for index, (attribute, title) in enumerate(categories):
            button = QPushButton(title)
            button.setCheckable(True)
            button.setMinimumHeight(76)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            setattr(self, attribute, button)
            self.buttons.append(button)
            grid.addWidget(button, index // 3, index % 3)
        layout.addLayout(grid)

        section = QHBoxLayout()
        titles = QVBoxLayout()
        titles.setSpacing(5)
        self.sectionTitleLabel = QLabel()
        self.sectionTitleLabel.setObjectName('sectionTitleLabel')
        self.resultCountLabel = QLabel()
        self.resultCountLabel.setObjectName('resultCountLabel')
        titles.addWidget(self.sectionTitleLabel)
        titles.addWidget(self.resultCountLabel)
        section.addLayout(titles)
        section.addStretch()
        self.allExercisesButton = QPushButton('Все упражнения')
        self.allExercisesButton.setObjectName('allExercisesButton')
        section.addWidget(self.allExercisesButton)
        layout.addLayout(section)

        self.noticeLabel = QLabel()
        self.noticeLabel.setObjectName('noticeLabel')
        self.noticeLabel.setWordWrap(True)
        self.noticeLabel.hide()
        layout.addWidget(self.noticeLabel)
        self.emptyStateLabel = QLabel()
        self.emptyStateLabel.setObjectName('emptyStateLabel')
        self.emptyStateLabel.setWordWrap(True)
        layout.addWidget(self.emptyStateLabel)
        self.exerciseList = QListWidget()
        self.exerciseList.setMinimumHeight(140)
        self.exerciseList.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.exerciseList.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.exerciseList.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(self.exerciseList, 1)
        footer = QLabel('Нажми на упражнение, чтобы открыть видео и параметры. Пока заполнена «Спина».')
        footer.setObjectName('footerLabel')
        footer.setWordWrap(True)
        layout.addWidget(footer)
        self.pages.addWidget(self.catalogPage)

    def create_exercise_page(self):
        # Прокрутка позволяет просматривать параметры в небольшом окне.
        self.detailPage = QScrollArea()
        self.detailPage.setWidgetResizable(True)
        contents = QWidget()
        contents.setObjectName('detailContents')
        layout = QVBoxLayout(contents)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(12)
        top = QHBoxLayout()
        self.backToListButton = QPushButton('← Назад к упражнениям')
        top.addWidget(self.backToListButton)
        top.addStretch()
        layout.addLayout(top)
        self.exerciseTitleLabel = QLabel()
        self.exerciseTitleLabel.setObjectName('exerciseTitle')
        self.exerciseTitleLabel.setWordWrap(True)
        layout.addWidget(self.exerciseTitleLabel)
        self.equipmentLabel = QLabel()
        self.equipmentLabel.setObjectName('muted')
        layout.addWidget(self.equipmentLabel)

        self.videoStack = QStackedWidget()
        self.videoStack.setMinimumHeight(210)
        self.videoPlaceholder = QPushButton('▶\nНажми, чтобы добавить своё видео')
        self.videoPlaceholder.setObjectName('videoPlaceholder')
        self.videoPlaceholder.setCursor(Qt.CursorShape.PointingHandCursor)
        self.videoWidget = QVideoWidget()
        self.videoWidget.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        self.videoWidget.setCursor(Qt.CursorShape.PointingHandCursor)
        self.videoStack.addWidget(self.videoPlaceholder)
        self.videoStack.addWidget(self.videoWidget)
        layout.addWidget(self.videoStack, 1)
        self.videoStatus = QLabel()
        self.videoStatus.setObjectName('videoStatus')
        self.videoStatus.setWordWrap(True)
        layout.addWidget(self.videoStatus)

        controls = QHBoxLayout()
        self.chooseVideoButton = QPushButton('Выбрать своё видео')
        self.chooseVideoButton.setObjectName('chooseVideoButton')
        self.playButton = QPushButton('Смотреть')
        self.stopButton = QPushButton('Стоп')
        controls.addWidget(self.chooseVideoButton)
        controls.addWidget(self.playButton)
        controls.addWidget(self.stopButton)
        controls.addStretch()
        layout.addLayout(controls)
        self.videoHintLabel = QLabel()
        self.videoHintLabel.setObjectName('videoHint')
        self.videoHintLabel.setWordWrap(True)
        layout.addWidget(self.videoHintLabel)

        stats = QGridLayout()
        stats.setSpacing(10)
        for index, (caption, attribute) in enumerate([
            ('Подходы', 'setsLabel'), ('Повторения', 'repsLabel'),
            ('Отдых — ориентир', 'restLabel'), ('Время подхода — примерно', 'durationLabel'),
        ]):
            card = QFrame()
            card.setObjectName('statCard')
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(16, 12, 16, 12)
            label = QLabel(caption)
            label.setObjectName('statCaption')
            value = QLabel()
            value.setObjectName('statValue')
            value.setWordWrap(True)
            setattr(self, attribute, value)
            card_layout.addWidget(label)
            card_layout.addWidget(value)
            stats.addWidget(card, index // 2, index % 2)
        layout.addLayout(stats)
        self.noteLabel = QLabel()
        self.noteLabel.setWordWrap(True)
        layout.addWidget(self.noteLabel)
        timing_note = QLabel('Время оценено при темпе около 4 сек на повторение, без пауз. '
                             'Сохраняй удобный контролируемый темп.')
        timing_note.setObjectName('muted')
        timing_note.setWordWrap(True)
        layout.addWidget(timing_note)
        training_note = QLabel('Стартовый пример для взрослого новичка. Нагрузку подбирай по своей подготовке.')
        training_note.setObjectName('muted')
        training_note.setWordWrap(True)
        layout.addWidget(training_note)
        source = QLabel('<a style="color:#a5aaa9" '
                        'href="https://www.nhs.uk/live-well/exercise/how-to-improve-strength-flexibility/">'
                        'Основа подходов и повторений: рекомендации NHS</a>')
        source.setOpenExternalLinks(True)
        source.setWordWrap(True)
        layout.addWidget(source)
        self.detailPage.setWidget(contents)
        self.pages.addWidget(self.detailPage)

    def filter_exercises(self):
        self.noticeLabel.hide()
        query = self.searchEdit.text().strip().lower().replace('ё', 'е')
        category = ''
        for button in self.buttons:
            if button.isChecked():
                category = button.text()
        found = []
        for name, group, equipment in self.exercises:
            if category and group != category:
                continue
            text = f'{name} {group} {equipment}'.lower().replace('ё', 'е')
            if query in text:
                found.append((name, group, equipment))
        if not query and not category and not self.show_all:
            found = found[:2]

        self.exerciseList.clear()
        for name, group, equipment in found:
            item = QListWidgetItem(f'{name}\n{group} · {equipment}')
            item.setSizeHint(QSize(0, 102))
            # Храним саму запись, чтобы поиск не путал упражнения по номерам строк.
            item.setData(Qt.ItemDataRole.UserRole, (name, group, equipment))
            item.setToolTip('Нажми, чтобы открыть упражнение')
            self.exerciseList.addItem(item)
        self.resultCountLabel.setText(f'Найдено: {len(found)}')
        self.emptyStateLabel.setVisible(len(found) == 0)
        if query:
            self.sectionTitleLabel.setText('Результаты поиска')
            self.emptyStateLabel.setText('Ничего не найдено. Попробуй другое название.')
        elif category:
            self.sectionTitleLabel.setText(f'Упражнения: {category}')
            self.emptyStateLabel.setText('В этой категории пока нет упражнений.')
        elif self.show_all:
            self.sectionTitleLabel.setText('Все упражнения')
        else:
            self.sectionTitleLabel.setText('Популярные упражнения')

    def show_all_exercises(self):
        self.show_all = True
        self.category_group.setExclusive(False)
        for button in self.buttons:
            button.setChecked(False)
        self.category_group.setExclusive(True)
        self.searchEdit.clear()
        self.filter_exercises()

    def eventFilter(self, watched, event):
        if watched is self.exerciseList and event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                item = self.exerciseList.currentItem()
                if item is not None:
                    self.open_exercise(item)
                return True
        if watched is self.videoWidget and event.type() == QEvent.Type.MouseButtonRelease:
            if event.button() == Qt.MouseButton.LeftButton and self.playButton.isEnabled():
                self.toggle_video()
                return True
        return super().eventFilter(watched, event)

    def open_exercise(self, item):
        name, group, equipment = item.data(Qt.ItemDataRole.UserRole)
        if group != 'Спина' or name not in BACK_EXERCISES:
            self.noticeLabel.setText('Описание и видео пока подготовлены только для упражнений на спину.')
            self.noticeLabel.show()
            return
        self.noticeLabel.hide()
        self.current_exercise = name
        plan = BACK_EXERCISES[name]
        self.exerciseTitleLabel.setText(name)
        self.equipmentLabel.setText(f'{group} · {equipment}')
        self.setsLabel.setText(f'{plan["sets"]} подхода')
        self.repsLabel.setText(plan['reps'])
        self.restLabel.setText(plan['rest'])
        self.durationLabel.setText(plan['duration'])
        self.noteLabel.setText(plan['note'])
        self.videoHintLabel.setText(f'Для автоматической загрузки положи ролик в videos/{plan["video"]}')
        path = self.video_paths.get(name, VIDEO_DIR / plan['video'])
        self.load_video(path)
        self.pages.setCurrentWidget(self.detailPage)
        self.detailPage.verticalScrollBar().setValue(0)
        self.backToListButton.setFocus()

    def show_catalog(self):
        self.player.stop()
        self.player.setSource(QUrl())
        self.playButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.pages.setCurrentWidget(self.catalogPage)
        self.exerciseList.setFocus()

    def load_video(self, path):
        self.player.stop()
        self.player.setSource(QUrl())
        self.videoStack.setCurrentWidget(self.videoPlaceholder)
        self.playButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.video_path = Path(path).resolve()
        if not self.video_path.is_file():
            self.videoStatus.setText('Видео пока не добавлено. Нажми на поле видео или кнопку ниже.')
            return
        self.videoStatus.setText(f'Видео: {self.video_path.name}')
        self.videoStack.setCurrentWidget(self.videoWidget)
        self.player.setSource(QUrl.fromLocalFile(str(self.video_path)))
        self.playButton.setEnabled(True)
        self.stopButton.setEnabled(True)

    def choose_video(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, 'Выбери видео упражнения', str(VIDEO_DIR),
            'Видео (*.mp4 *.mov *.m4v *.avi *.mkv *.webm);;Все файлы (*)',
        )
        if filename:
            self.video_paths[self.current_exercise] = filename
            self.load_video(filename)

    def toggle_video(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def update_play_button(self, state):
        self.playButton.setText('Пауза' if state == QMediaPlayer.PlaybackState.PlayingState else 'Смотреть')

    def show_video_error(self, error, message):
        if error == QMediaPlayer.Error.NoError:
            return
        self.player.stop()
        self.videoStack.setCurrentWidget(self.videoPlaceholder)
        self.playButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.videoStatus.setText('Не удалось воспроизвести файл. Попробуй MP4 с видео H.264 и звуком AAC.')
        self.videoStatus.setToolTip(message)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape and self.pages.currentWidget() is self.detailPage:
            self.show_catalog()
            event.accept()
            return
        super().keyPressEvent(event)

    def closeEvent(self, event):
        self.player.stop()
        self.player.setSource(QUrl())
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setFont(QFont('Arial', 10))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
