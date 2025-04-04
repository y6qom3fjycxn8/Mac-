from setuptools import setup

APP = ['monitor_connection.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['cv2', 'numpy', 'pyautogui', 'pynput'],
    'iconfile': 'icon.icns',  # 如果你有图标文件的话
    'plist': {
        'CFBundleName': "连接监控",
        'CFBundleDisplayName': "连接监控",
        'CFBundleGetInfoString': "监控并自动重连",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 