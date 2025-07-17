from setuptools import setup

APP = ['SignalBox.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'signal-box_icon.icns',
    'plist': 'info.plist',
    'packages': ['librosa', 'numpy', 'PySide6', 'soundfile', 'scipy', 'matplotlib', 'pyaudio'],
    'includes': ['sklearn']

}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
