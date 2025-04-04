#!/bin/bash

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "未安装Python3，正在安装..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && brew install python3
fi

# 检查pip3
if ! command -v pip3 &> /dev/null; then
    echo "未安装pip3，正在安装..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
fi

# 检查并安装依赖
echo "检查依赖..."
pip3 install --quiet opencv-python numpy pyautogui pynput

# 运行程序
cd "$SCRIPT_DIR"
echo "启动监控程序..."
python3 monitor_connection.py 