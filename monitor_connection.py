import cv2
import numpy as np
import pyautogui
import time
from pynput import keyboard
import os
import threading
import subprocess

running = True
current_directory = os.path.dirname(__file__)


def get_window_rect():
    """获取aiOS窗口的位置和大小"""
    try:
        # 使用 osascript 获取窗口信息
        script = '''
        tell application "System Events"
            set frontApp to first application process whose frontmost is true
            if name of frontApp contains "Hyperspace" then
                set appWindow to first window of frontApp
                return {position, size} of appWindow
            end if
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        if result.stdout.strip():
            # 解析窗口位置和大小
            pos_size = eval(result.stdout.strip())
            left, top = pos_size[0]
            width, height = pos_size[1]
            # 计算监控区域（在窗口右上角）
            x = left + width - 350  # 距离右边 350 像素
            y = top + 150  # 距离顶部 150 像素
            monitor_width = 200
            monitor_height = 200
            return (x, y, monitor_width, monitor_height)
    except Exception as e:
        print(f"获取窗口位置时出错: {str(e)}")
        return None


def find_and_click(image_path, screenshot, region):
    try:
        template_rgb = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
        if template_rgb is None:
            return False

        template = cv2.cvtColor(template_rgb, cv2.COLOR_RGB2BGR)
        screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        res = cv2.matchTemplate(screenshot_bgr, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.5
        loc = np.where(res >= threshold)

        if len(loc[0]) > 0:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            template_h, template_w = template.shape[:2]
            center_x = max_loc[0] + template_w // 2
            center_y = max_loc[1] + template_h // 2
            screen_x = center_x + region[0]
            screen_y = center_y + region[1]
            pyautogui.click(screen_x, screen_y)
            print("✓ 已点击断开状态的开关")
            return True
        return False
    except Exception as e:
        print(f"匹配图片时出错: {str(e)}")
        return False


def is_aios_window():
    """检查当前窗口是否是 aios"""
    try:
        script = '''
        tell application "System Events"
            set frontApp to first application process whose frontmost is true
            return name of frontApp contains "Hyperspace"
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        return result.stdout.strip().lower() == 'true'
    except:
        return False


def run():
    global running
    disconnected_path = os.path.join(current_directory, 'disconnected.png')

    if not os.path.exists(disconnected_path):
        print("错误: 未找到模板图片 'disconnected.png'")
        return

    print("监控已启动，按F12停止...")

    while running:
        try:
            if is_aios_window():
                region = get_window_rect()
                if region:
                    screenshot = pyautogui.screenshot(region=region)
                    screenshot = np.array(screenshot)
                    if find_and_click(disconnected_path, screenshot, region):
                        time.sleep(2)
            time.sleep(0.5)

        except Exception as e:
            print(f"运行时出错: {str(e)}")
            time.sleep(0.5)


def on_press(key):
    global running
    if key == keyboard.Key.f12:
        print("\n停止监控")
        running = False
        return False


if __name__ == "__main__":
    # 启动键盘监听
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # 运行主程序
    run()