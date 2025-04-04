import cv2
import numpy as np
import pyautogui
import time
import threading
import os
from pynput import keyboard

running = True
current_directory = os.path.dirname(__file__)

def get_window_position(full_screenshot_path):
    """通过完整截图找到软件窗口位置"""
    try:
        # 读取完整窗口模板
        template_rgb = cv2.imdecode(np.fromfile(full_screenshot_path, dtype=np.uint8), -1)
        if template_rgb is None:
            return None
            
        # 获取全屏截图
        screen = np.array(pyautogui.screenshot())
        
        # 转换颜色空间
        template = cv2.cvtColor(template_rgb, cv2.COLOR_RGB2BGR)
        screen_bgr = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
        
        # 模板匹配
        res = cv2.matchTemplate(screen_bgr, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        if max_val >= 0.8:  # 高阈值确保准确找到窗口
            return max_loc
        return None
    except Exception as e:
        return None

def check_status(screenshot, connected_path, disconnected_path):
    """检查连接状态"""
    try:
        # 读取两个状态的模板图片
        connected_rgb = cv2.imdecode(np.fromfile(connected_path, dtype=np.uint8), -1)
        disconnected_rgb = cv2.imdecode(np.fromfile(disconnected_path, dtype=np.uint8), -1)
        
        if connected_rgb is None or disconnected_rgb is None:
            return "unknown"
            
        # 转换颜色空间
        connected = cv2.cvtColor(connected_rgb, cv2.COLOR_RGB2BGR)
        disconnected = cv2.cvtColor(disconnected_rgb, cv2.COLOR_RGB2BGR)
        screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        
        # 模板匹配
        res_connected = cv2.matchTemplate(screenshot_bgr, connected, cv2.TM_CCOEFF_NORMED)
        res_disconnected = cv2.matchTemplate(screenshot_bgr, disconnected, cv2.TM_CCOEFF_NORMED)
        
        # 获取最佳匹配值
        _, max_val_connected, _, _ = cv2.minMaxLoc(res_connected)
        _, max_val_disconnected, _, max_loc_disconnected = cv2.minMaxLoc(res_disconnected)
        
        # 判断状态
        threshold = 0.8
        if max_val_disconnected >= threshold and max_val_disconnected > max_val_connected:
            return "disconnected", max_loc_disconnected, disconnected.shape[:2]
        elif max_val_connected >= threshold:
            return "connected", None, None
            
        return "unknown", None, None
        
    except Exception as e:
        return "error", None, None

def run():
    global running
    # 检查所需的图片文件
    full_path = os.path.join(current_directory, 'full.jpg')
    connected_path = os.path.join(current_directory, 'connected.jpg')
    disconnected_path = os.path.join(current_directory, 'disconnected.jpg')
    
    for path in [full_path, connected_path, disconnected_path]:
        if not os.path.exists(path):
            print(f"错误: 未找到图片 {os.path.basename(path)}")
            return
    
    print("监控已启动，按F12停止...")
    
    # 启动键盘监听
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    last_status = None
    while running:
        try:
            # 找到窗口位置
            window_pos = get_window_position(full_path)
            if window_pos:
                # 截取状态区域（左上角部分）
                x, y = window_pos
                screenshot = pyautogui.screenshot(region=(x, y, 500, 400))
                screenshot = np.array(screenshot)
                
                # 检查状态
                status, click_pos, template_size = check_status(screenshot, connected_path, disconnected_path)
                
                # 只在状态改变时显示
                if status != last_status:
                    if status == "connected":
                        print("✓ 连接正常")
                    elif status == "disconnected":
                        print("! 连接断开，尝试重连...")
                        if click_pos:
                            # 计算点击位置
                            click_x = x + click_pos[0] + template_size[1] // 2
                            click_y = y + click_pos[1] + template_size[0] // 2
                            pyautogui.click(click_x, click_y)
                            time.sleep(2)
                    
                last_status = status
            
            time.sleep(0.5)
                
        except Exception as e:
            time.sleep(0.5)

def on_press(key):
    global running
    try:
        if key == keyboard.Key.f12:
            print("监控已停止")
            running = False
            return False
    except:
        pass

if __name__ == "__main__":
    run() 