import sys
from pathlib import Path

from PyQt6.QtCore import QEvent, QSettings, QSize, Qt, QUrl
from PyQt6.QtGui import QFont
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (
    QApplication, QButtonGroup, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QMessageBox, QPushButton, QScrollArea, QStackedWidget, QVBoxLayout, QWidget,
)

VIDEO_FOLDER = Path(__file__).resolve().parent / 'videos'
FAVORITES_FILE = VIDEO_FOLDER.parent / 'favorites.ini'


DATA = {
    'Спина': {
        'Тяга верхнего блока к груди': {
            "video": 'IMG_7184.mov', "sets": '2 подхода', "reps": '8–12 повторений',
            "rest": '120 сек между подходами', "time": '32–48 сек на подход',
            "note": 'Подбирай вес, с которым получается двигаться плавно и без рывков.',
        },
        'Горизонтальная тяга блока': {
            "video": 'IMG_7185.MOV', "sets": '2 подхода', "reps": '8–12 повторений',
            "rest": '120 сек между подходами', "time": '32–48 сек на подход',
            "note": 'Начни с небольшой нагрузки и сохраняй контроль над движением.',
        },
        'Тяга гантели одной рукой': {
            "video": 'IMG_7183.mov', "sets": '2 подхода', "reps": '8–12 повторений',
            "rest": '120 сек после обеих сторон', "time": '64–96 сек на обе стороны',
            "note": 'Повторения указаны для каждой руки. Один подход включает обе стороны; при смене руки можно сделать короткую паузу по необходимости.',
        },
        'Гиперэкстензия': {
            "video": 'IMG_7188.mov', "sets": '2 подхода', "reps": '8–12 повторений',
            "rest": '90 сек между подходами', "time": '32–48 сек на подход',
            "note": 'Для знакомства с упражнением начни без дополнительного отягощения.',
        },
        'Тяга прямыми руками в кроссовере': {
            "video": 'copy_0B890460-FF3C-45FD-96D0-3C85034A3869.mov', "sets": '2 подхода', "reps": '8–12 повторений',
            "rest": '90 сек между подходами', "time": '32–48 сек на подход',
            "note": 'Выбирай небольшой вес, который позволяет контролировать движение.',
        },
    },
    'Грудь': {
        'Жим гантелей лёжа': {
            "video": 'IMG_7182.mov', "sets": '2 подхода', "reps": '8–12 повторений',
            "rest": '120 сек между подходами', "time": '32–48 сек на подход',
            "note": 'Начни с лёгких гантелей. Двигайся плавно, без рывков.',
        },
        'Отжимание от пола': {
            "video": 'IMG_7192.mov', "sets": '2 подхода', "reps": '8–12 повторений',
            "rest": '120 сек между подходами', "time": '32–48 сек на подход',
            "note": 'Сохраняй контроль над движением. Если вариант от пола пока тяжёлый, начни с отжиманий от стены.',
        },
        'Жим гантелей на наклонной скамье': {
            "video": 'IMG_7191.mov', "sets": '2 подхода', "reps": '8–12 повторений',
            "rest": '120 сек между подходами', "time": '32–48 сек на подход',
            "note": 'Проверь устойчивость скамьи. Выбери вес, который позволяет двигаться без рывков.',
        },
        'Сведение рук в тренажёре «Бабочка»': {
            "video": 'IMG_7200.mov', "sets": '2 подхода', "reps": '8–12 повторений',
            "rest": '90 сек между подходами', "time": '32–48 сек на подход',
            "note": 'Настрой сиденье под свой рост. Своди и разводи руки плавно, без боли в плечах.',
        },
        'Сведение рук в кроссовере': {
            "video": 'IMG_7202.mov', "sets": '2 подхода', "reps": '8–12 повторений',
            "rest": '90 сек между подходами', "time": '32–48 сек на подход',
            "note": 'Начни с небольшой нагрузки. Не помогай движению рывком корпуса.',
        },
    },
    'Ноги': {
        'Жим ногами в тренажёре': {
            "video": 'copy_A24204F8-4D28-4433-B4E1-D4906AC600FD 2.mov', "sets": '2 подхода', "reps": '8–12 повторений',
            "rest": '120 сек между подходами', "time": '32–48 сек на подход',
            "note": 'Перед началом настрой тренажёр. Выбирай комфортную глубину движения и лёгкую начальную нагрузку.',
        },
        'Приседание': {
            "video": 'IMG_7194.mov', "sets": '2 подхода', "reps": '8–12 повторений',
            "rest": '120 сек между подходами', "time": '32–48 сек на подход',
            "note": 'Начни без дополнительного веса. Приседай на удобную глубину, сохраняя равновесие.',
        },
        'Разгибание ног в тренажёре': {
            "video": 'IMG_7195.mov', "sets": '2 подхода', "reps": '8–12 повторений',
            "rest": '90 сек между подходами', "time": '32–48 сек на подход',
            "note": 'Настрой сиденье и валик. Подбирай нагрузку, с которой движение остаётся плавным и комфортным.',
        },
        'Сгибание ног в тренажёре': {
            "video": 'IMG_7196.MOV', "sets": '2 подхода', "reps": '8–12 повторений',
            "rest": '90 сек между подходами', "time": '32–48 сек на подход',
            "note": 'Настрой тренажёр под свой рост. Не бросай вес при возвращении в исходное положение.',
        },
        'Подъём на носки': {
            "video": 'IMG_7197.MOV', "sets": '2 подхода', "reps": '8–12 повторений',
            "rest": '60 сек между подходами', "time": '32–48 сек на подход',
            "note": 'Поднимай и опускай пятки медленно. При необходимости используй устойчивую опору.',
        },
    },
    'Реабилитация': {
        'Кошка-корова': {
            "video": 'IMG_7209.mov', "sets": '1 подход', "reps": '5 полных циклов',
            "rest": '30–60 сек при необходимости', "time": 'Около 30 сек на подход',
            "note": 'Один цикл — плавно округлить спину и вернуться через обратное движение. Не выполняй через боль.',
            "timing": 'Для оценки времени взято около 6 сек на полный цикл. Амплитуда и темп должны быть комфортными.',
        },
        'Ягодичный мостик': {
            "video": 'IMG_7205.MOV', "sets": '1 подход', "reps": '5–8 повторений',
            "rest": '30–60 сек при необходимости', "time": '20–32 сек на подход',
            "note": 'Ознакомительный вариант без дополнительного веса. Поднимай и опускай таз плавно, в комфортной амплитуде.',
        },
        'Разгибание ноги сидя': {
            "video": 'IMG_7195.mov', "sets": '1 подход', "reps": '5 повторений на каждую ногу',
            "rest": '30–60 сек при необходимости', "time": 'Около 40 сек на обе ноги',
            "note": 'Используй тренажёр в зале. Повторения указаны отдельно для каждой ноги; выполняй без дополнительного веса.',
        },
        'Отжимание от стены': {
            "video": 'IMG_7216.MOV', "sets": '1 подход', "reps": '5 повторений',
            "rest": '30–60 сек при необходимости', "time": 'Около 20 сек на подход',
            "note": 'Выбери удобное расстояние до стены и небольшую амплитуду. Не продолжай через боль.',
        },
        'Подъём на носки с опорой': {
            "video": 'IMG_7198.MOV', "sets": '1 подход', "reps": '5 повторений',
            "rest": '30–60 сек при необходимости', "time": 'Около 20 сек на подход',
            "note": 'Держись за устойчивую опору. Медленно поднимай обе пятки и плавно опускай их.',
        },
    },
    'Растяжка': {
        'Растяжка икроножных мышц у стены': {
            "video": 'IMG_7210.MOV', "sets": '2 подхода', "reps": '15–20 сек на каждую сторону',
            "rest": '15–30 сек между подходами', "time": '30–40 сек на обе стороны',
            "note": 'Растягивай по одной ноге. Ощущение должно быть комфортным, без боли и пружинящих движений.',
        },
        'Растяжка передней поверхности бедра': {
            "video": 'IMG_7212.MOV', "sets": '2 подхода', "reps": '15–20 сек на каждую сторону',
            "rest": '15–30 сек между подходами', "time": '30–40 сек на обе стороны',
            "note": 'Удерживай растяжку отдельно для каждой ноги. Если выполняешь стоя, используй опору для равновесия.',
        },
        'Растяжка задней поверхности бедра сидя': {
            "video": 'IMG_7214.MOV', "sets": '2 подхода', "reps": '15–20 сек на каждую сторону',
            "rest": '15–30 сек между подходами', "time": '30–40 сек на обе стороны',
            "note": 'Выполняй растяжку отдельно для каждой ноги. Наклоняйся только до комфортного натяжения.',
        },
        'Растяжка грудных мышц у стены': {
            "video": 'IMG_7217.MOV', "sets": '2 подхода', "reps": '15–20 сек на каждую сторону',
            "rest": '15–30 сек между подходами', "time": '30–40 сек на обе стороны',
            "note": 'Растягивай по одной стороне. Не допускай боли в плече и резких поворотов корпуса.',
        },
        'Растяжка ягодичных мышц лёжа': {
            "video": 'IMG_7215.MOV', "sets": '2 подхода', "reps": '15–20 сек на каждую сторону',
            "rest": '15–30 сек между подходами', "time": '30–40 сек на обе стороны',
            "note": 'Выполняй отдельно для каждой стороны. Удерживай положение спокойно, без рывков.',
        },
    },
    'Для начинающих': {
        'Отжимания от стены': {
            "video": 'IMG_7216.MOV', "sets": '1 подход', "reps": '5–8 повторений',
            "rest": '60 сек при необходимости', "time": '20–32 сек на подход',
            "note": 'Начни с удобного расстояния до стены. Сначала освой плавное движение, затем постепенно увеличивай нагрузку.',
        },
        'Приседания до стула': {
            "video": 'IMG_7218.MOV', "sets": '1 подход', "reps": '5 повторений',
            "rest": '60 сек при необходимости', "time": 'Около 20 сек на подход',
            "note": 'Выбери устойчивый стул без колёс. Медленно садись и вставай; при необходимости помогай себе руками.',
        },
        'Ягодичный мостик': {
            "video": 'IMG_7205.MOV', "sets": '1 подход', "reps": '5–8 повторений',
            "rest": '60 сек при необходимости', "time": '20–32 сек на подход',
            "note": 'Начни без дополнительного веса. Поднимай и опускай таз плавно, в комфортной амплитуде.',
        },
        'Подъём коленей на месте': {
            "video": 'IMG_7224.MOV', "sets": '1 подход', "reps": '30 секунд в удобном темпе',
            "rest": '30–60 сек при необходимости', "time": '30 сек на подход',
            "note": 'Шагай на месте спокойно, поднимая колени на удобную высоту. При необходимости держись за устойчивую опору.',
            "timing": 'Здесь движение выполняется по времени: 30 секунд в удобном темпе. Число шагов не фиксируется.',
        },
        'Подъём противоположных руки и ноги на четвереньках': {
            "video": 'IMG_7221.MOV', "sets": '1 подход', "reps": '5 повторений на каждую сторону',
            "rest": '60 сек при необходимости', "time": 'Около 40 сек на обе стороны',
            "note": 'Чередуй стороны. Поднимай противоположные руку и ногу на комфортную высоту без разворота корпуса.',
        },
    },
}

STYLE = """
QMainWindow, QWidget#home, QWidget#content, QStackedWidget { background: #17191b; }
QWidget { color: #f4f5f2; font: 14px Arial; }
QLabel#brand { font-size: 34px; font-weight: bold; }
QLabel#title { font-size: 23px; font-weight: bold; }
QLabel#small { color: #a5aaa9; font-size: 13px; }
QLabel#badge { color: #bddf91; background: #242e20; padding: 9px 14px; border-radius: 12px; }
QLineEdit { background: #101214; border: 1px solid #393d40; border-radius: 14px; padding: 0px 18px; font-size: 16px; }
QLineEdit:focus, QPushButton:focus { border: 1px solid #b8dc8b; }
QLineEdit { selection-background-color: #b8dc8b; selection-color: #17191b; }
QPushButton { background: #252a25; border: 1px solid #465044; border-radius: 10px; padding: 10px 16px; }
QPushButton:hover { background: #36412e; }
QPushButton:checked { background: #b8dc8b; color: #192012; font-weight: bold; }
QPushButton:disabled { color: #777e78; border-color: #303733; }
QListWidget { background: transparent; border: none; outline: none; }
QListWidget::item { background: #222528; border: 1px solid #303538; border-radius: 14px; padding: 16px; margin-bottom: 10px; }
QListWidget::item:hover { border-color: #6b795e; }
QListWidget::item:selected { background: #2b3525; border-color: #b8dc8b; }
QFrame#stat { background: #222528; border-radius: 12px; }
QLabel#value { color: #c4e69e; font-size: 17px; font-weight: bold; }
QScrollArea { border: none; background: #17191b; }
QLabel#placeholder { background: #101214; border-radius: 14px; font-size: 20px; font-weight: bold; }
QScrollBar:vertical { background: #17191b; width: 10px; margin: 0px; }
QScrollBar::handle:vertical { background: #465044; border-radius: 5px; min-height: 32px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }
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
        self.settings = QSettings(str(FAVORITES_FILE), QSettings.Format.IniFormat)

        self.pages = QStackedWidget()
        self.setCentralWidget(self.pages)
        self.make_home()
        self.make_detail()

        self.player = QMediaPlayer(self)
        self.sound = QAudioOutput(self)
        self.sound.setVolume(0.5)
        self.player.setAudioOutput(self.sound)
        self.player.setVideoOutput(self.video)
        self.player.playbackStateChanged.connect(self.update_play)
        self.player.errorOccurred.connect(self.video_error)
        self.video.installEventFilter(self)
        self.play_button.setEnabled(False)
        self.stop_button.setEnabled(False)

        # Мне можно выбрать только одну категорию.
        self.group = QButtonGroup(self)
        for button in self.buttons:
            self.group.addButton(button)
            button.clicked.connect(self.filter_exercises)
        self.group.addButton(self.favorites_button)
        self.favorites_button.clicked.connect(self.show_favorites)
        self.search.textChanged.connect(self.filter_exercises)
        self.all_button.clicked.connect(self.all_exercises)
        self.list.itemClicked.connect(self.open_exercise)
        self.list.itemActivated.connect(self.open_exercise)
        self.list.installEventFilter(self)
        self.back_button.clicked.connect(self.go_back)
        self.favorite_button.toggled.connect(self.update_favorite_button)
        self.favorite_button.clicked.connect(self.save_favorite)
        self.play_button.clicked.connect(self.play_video)
        self.stop_button.clicked.connect(self.player.stop)
        self.filter_exercises()

    def label(self, text, style=''):
        label = QLabel(text)
        label.setObjectName(style)
        if style not in ('brand', 'badge', 'title'):
            label.setWordWrap(True)
        return label

    def make_home(self):
        self.home = QWidget()
        self.home.setObjectName('home')
        layout = QVBoxLayout(self.home)
        layout.setContentsMargins(32, 26, 32, 22)
        layout.setSpacing(16)

        header = QHBoxLayout()
        header.addWidget(self.label('FitTrack', 'brand'))
        header.addStretch()
        header.addWidget(self.label('30 упражнений · 6 категорий', 'badge'))
        layout.addLayout(header)
        layout.addWidget(self.label('Упражнения и комплексы для твоих целей', 'small'))
        self.search = QLineEdit()
        self.search.setPlaceholderText('Поиск по названию, категории или оборудованию…')
        self.search.setMinimumHeight(56)
        self.search.setClearButtonEnabled(True)
        layout.addWidget(self.search)
        layout.addWidget(self.label('ВЫБЕРИ КАТЕГОРИЮ', 'small'))

        grid = QGridLayout()
        grid.setSpacing(12)
        self.buttons = []
        names = ['Спина', 'Грудь', 'Ноги', 'Реабилитация', 'Растяжка', 'Для начинающих']
        for number, name in enumerate(names):
            button = QPushButton(name)
            button.setCheckable(True)
            button.setMinimumHeight(76)
            self.buttons.append(button)
            grid.addWidget(button, number // 3, number % 3)
        layout.addLayout(grid)

        row = QHBoxLayout()
        self.title = self.label('', 'title')
        self.all_button = QPushButton('Все упражнения')
        self.favorites_button = QPushButton('★ Избранное')
        self.favorites_button.setCheckable(True)
        row.addWidget(self.title)
        row.addStretch()
        row.addWidget(self.favorites_button)
        row.addWidget(self.all_button)
        layout.addLayout(row)
        self.count = self.label('', 'small')
        self.message = self.label('', 'small')
        layout.addWidget(self.count)
        layout.addWidget(self.message)
        self.list = QListWidget()
        self.list.setMinimumHeight(140)
        self.list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(self.list, 1)
        layout.addWidget(self.label('Нажми на любое упражнение, чтобы открыть видео и параметры.', 'small'))
        self.pages.addWidget(self.home)

    def make_detail(self):
        self.detail = QScrollArea()
        self.detail.setWidgetResizable(True)
        content = QWidget()
        content.setObjectName('content')
        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(12)
        row = QHBoxLayout()
        self.back_button = QPushButton('← Назад к упражнениям')
        self.favorite_button = QPushButton('☆ В избранное')
        self.favorite_button.setCheckable(True)
        row.addWidget(self.back_button)
        row.addStretch()
        row.addWidget(self.favorite_button)
        layout.addLayout(row)
        self.name = self.label('', 'title')
        self.tools = self.label('', 'small')
        layout.addWidget(self.name)
        layout.addWidget(self.tools)

        self.video_box = QStackedWidget()
        self.video_box.setMinimumHeight(210)
        self.placeholder = self.label('Видео недоступно', 'placeholder')
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video = QVideoWidget()
        self.video_box.addWidget(self.placeholder)
        self.video_box.addWidget(self.video)
        layout.addWidget(self.video_box, 1)
        self.status = self.label('', 'small')
        layout.addWidget(self.status)

        row = QHBoxLayout()
        self.play_button = QPushButton('Смотреть')
        self.stop_button = QPushButton('Стоп')
        row.addWidget(self.play_button)
        row.addWidget(self.stop_button)
        row.addStretch()
        layout.addLayout(row)

        grid = QGridLayout()
        grid.setSpacing(10)
        self.sets = self.stat(grid, 0, 0, 'Подходы')
        self.reps = self.stat(grid, 0, 1, 'Повторения / время')
        self.rest = self.stat(grid, 1, 0, 'Отдых — ориентир')
        self.time = self.stat(grid, 1, 1, 'Время подхода — примерно')
        layout.addLayout(grid)
        self.note = self.label('')
        layout.addWidget(self.note)
        self.timing = self.label('', 'small')
        layout.addWidget(self.timing)
        self.tip = self.label('', 'small')
        layout.addWidget(self.tip)
        self.source = self.label('')
        self.source.setOpenExternalLinks(True)
        layout.addWidget(self.source)
        self.detail.setWidget(content)
        self.pages.addWidget(self.detail)

    def stat(self, grid, row, column, text):
        card = QFrame()
        card.setObjectName('stat')
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        value = self.label('', 'value')
        layout.addWidget(self.label(text, 'small'))
        layout.addWidget(value)
        grid.addWidget(card, row, column)
        return value

    def filter_exercises(self):
        query = self.search.text().strip().lower().replace('ё', 'е')
        favorites_only = self.favorites_button.isChecked()
        category = ''
        for button in self.buttons:
            if button.isChecked():
                category = button.text()
        found = []
        for name, group, tools in self.exercises:
            if category and group != category:
                continue
            if favorites_only and not self.settings.value(f'favorites/{group}/{name}', False, type=bool):
                continue
            text = f'{name} {group} {tools}'.lower().replace('ё', 'е')
            if query in text:
                found.append((name, group, tools))
        if not query and not category and not self.show_all and not favorites_only:
            found = found[:2]

        self.list.clear()
        for name, group, tools in found:
            item = QListWidgetItem(f'{name}\n{group} · {tools}')
            item.setSizeHint(QSize(0, 102))
            item.setData(Qt.ItemDataRole.UserRole, (name, group, tools))
            self.list.addItem(item)
        self.count.setText(f'Найдено: {len(found)}')
        self.message.setText('Ничего не найдено. Попробуй другое название.')
        self.message.setVisible(len(found) == 0)
        if favorites_only:
            self.title.setText('Избранное')
            if not query:
                self.message.setText('В избранном пока нет упражнений. Открой карточку и нажми «В избранное».')
        elif query:
            self.title.setText('Результаты поиска')
        elif category:
            self.title.setText(f'Упражнения: {category}')
        elif self.show_all:
            self.title.setText('Все упражнения')
        else:
            self.title.setText('Популярные упражнения')

    def all_exercises(self):
        self.show_all = True
        self.group.setExclusive(False)
        for button in self.group.buttons():
            button.setChecked(False)
        self.group.setExclusive(True)
        self.search.clear()
        self.filter_exercises()

    def show_favorites(self):
        self.search.clear()
        self.filter_exercises()

    def update_favorite_button(self, checked):
        self.favorite_button.setText('★ Убрать из избранного' if checked else '☆ В избранное')

    def save_favorite(self, checked):
        self.settings.setValue(self.favorite_key, checked)
        self.settings.sync()
        if self.settings.status() != QSettings.Status.NoError:
            QMessageBox.warning(self, 'Избранное', 'Не удалось сохранить изменения на диск.')
        if self.favorites_button.isChecked():
            self.filter_exercises()

    def open_exercise(self, item):
        name, group, tools = item.data(Qt.ItemDataRole.UserRole)
        data = DATA[group][name]
        self.favorite_key = f'favorites/{group}/{name}'
        self.favorite_button.setChecked(self.settings.value(self.favorite_key, False, type=bool))
        self.sets.setText(data['sets'])
        self.reps.setText(data['reps'])
        self.name.setText(name)
        self.tools.setText(f'{group} · {tools}')
        self.rest.setText(data['rest'])
        self.time.setText(data['time'])
        self.note.setText(data['note'])
        timing = 'Время оценено при темпе около 4 сек на повторение, без пауз. Сохраняй удобный контролируемый темп.'
        self.timing.setText(data.get('timing', timing))
        self.tip.setText('Стартовый пример для взрослого новичка. Нагрузку и состав тренировки подбирай по своей подготовке.')
        link = 'https://www.nhs.uk/live-well/exercise/how-to-improve-strength-flexibility/'
        text = 'Общие рекомендации NHS по силовым упражнениям'
        if group == 'Растяжка':
            self.timing.setText('Один подход: по 15–20 сек на каждую сторону. Время перехода между сторонами не учтено.')
            self.tip.setText('Удерживай растяжку до комфортного натяжения, без боли и пружинящих движений.')
            link = 'https://www.nhs.uk/live-well/exercise/how-to-stretch-after-exercising/'
            text = 'Общие рекомендации NHS по растяжке'
        elif group == 'Реабилитация':
            self.tip.setText('Это ознакомительный пример, а не лечебный план. После травмы или операции нагрузку и допустимые движения подбирает специалист. При боли остановись.')
            link = 'https://services.eastcheshire.nhs.uk/physiotherapy-service/self-help/back-and-neck-pain'
            text = 'NHS: примеры упражнений и ограничения самостоятельного подбора'
        elif group == 'Для начинающих':
            link = 'https://www.nhs.uk/live-well/exercise/strength-exercises/'
            text = 'NHS: простые упражнения и постепенное начало'
        self.source.setText(f'<a style="color:#a5aaa9" href="{link}">{text}</a>')
        self.load_video(VIDEO_FOLDER / data['video'])
        self.pages.setCurrentWidget(self.detail)
        self.detail.verticalScrollBar().setValue(0)
        self.back_button.setFocus()

    def go_back(self):
        self.player.stop()
        self.player.setSource(QUrl())
        self.play_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.pages.setCurrentWidget(self.home)
        self.list.setFocus()

    def load_video(self, path):
        self.player.stop()
        self.player.setSource(QUrl())
        self.video_box.setCurrentWidget(self.placeholder)
        self.play_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.status.setToolTip('')
        path = Path(path).resolve()
        if not path.is_file():
            self.status.setText(f'Файл видео не найден: videos/{path.name}')
            return
        self.status.setText(f'Видео: {path.name}')
        self.video_box.setCurrentWidget(self.video)
        self.play_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.player.setSource(QUrl.fromLocalFile(str(path)))

    def play_video(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def update_play(self, state):
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.play_button.setText('Пауза')
        else:
            self.play_button.setText('Смотреть')

    def video_error(self, error, message):
        if error != QMediaPlayer.Error.NoError:
            self.player.stop()
            self.video_box.setCurrentWidget(self.placeholder)
            self.play_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.status.setText('Не удалось воспроизвести видео.')
            self.status.setToolTip(message)

    def eventFilter(self, widget, event):
        if widget is self.list and event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                item = self.list.currentItem()
                if item is not None:
                    self.open_exercise(item)
                return True
        if widget is self.video and event.type() == QEvent.Type.MouseButtonRelease:
            if event.button() == Qt.MouseButton.LeftButton and self.play_button.isEnabled():
                self.play_video()
                return True
        return super().eventFilter(widget, event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape and self.pages.currentWidget() is self.detail:
            self.go_back()
        else:
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
