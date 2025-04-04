import cv2
import numpy as np
import pyautogui
import time
import os
from pynput import keyboard

running = True
current_directory = os.path.dirname(__file__)

def on_press(key):
    global running
    try:
        if key == keyboard.Key.f12:
            print("监控已停止")
            running = False
    except:
        pass

def find_and_click(image_path, screenshot, region):
    try:
        # 读取模板图片
        template_rgb = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
        if template_rgb is None:
            return False
            
        # 转换颜色空间
        template = cv2.cvtColor(template_rgb, cv2.COLOR_RGB2BGR)
        screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        # 模板匹配
        res = cv2.matchTemplate(screenshot_bgr, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.5
        loc = np.where(res >= threshold)
        
        if len(loc[0]) > 0:
            # 获取最佳匹配位置
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            template_h, template_w = template.shape[:2]
            
            # 计算点击位置（模板中心）
            center_x = max_loc[0] + template_w // 2
            center_y = max_loc[1] + template_h // 2
            
            # 转换为屏幕坐标
            screen_x = center_x + region[0]
            screen_y = center_y + region[1]
            
            # 执行点击
            pyautogui.click(screen_x, screen_y)
            print("✓ 已点击断开状态的开关")
            return True
        return False
    except Exception as e:
        print(f"错误：{str(e)}")
        return False

def run():
    global running
    disconnected_path = os.path.join(current_directory, 'disconnected.png')
    
    if not os.path.exists(disconnected_path):
        print("错误: 未找到模板图片")
        return
    
    print("监控已启动，按F12停止...")
    
    # 设置监控区域
    print("=== 设置监控区域 ===")
    print("1. 请将鼠标移动到断开连接开关的位置")
    print("2. 保持鼠标位置不动")
    print("3. 等待3秒记录位置...")
    time.sleep(3)
    
    # 获取鼠标位置
    mouse_x, mouse_y = pyautogui.position()
    print(f"记录的鼠标位置: x={mouse_x}, y={mouse_y}")
    
    # 计算监控区域
    x = mouse_x - 100
    y = mouse_y - 100
    width = 200
    height = 200
    region = (x, y, width, height)
    
    print(f"将监控以下区域：")
    print(f"x={x}, y={y}, width={width}, height={height}")
    input("按回车继续，Ctrl+C取消...")
    
    while running:
        try:
            # 截取屏幕区域
            screenshot = pyautogui.screenshot(region=region)
            screenshot = np.array(screenshot)
            
            # 检查是否断开
            if find_and_click(disconnected_path, screenshot, region):
                time.sleep(2)
            
            time.sleep(0.5)
                
        except Exception as e:
            print(f"错误：{str(e)}")
            time.sleep(0.5)

if __name__ == "__main__":
    # 启动键盘监听
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    # 运行主程序
    run() 