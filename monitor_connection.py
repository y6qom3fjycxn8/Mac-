import cv2
import numpy as np
import pyautogui
import time
from pynput import keyboard
import os
import sys

def check_permissions():
    """检查必要的权限"""
    print("\n=== 权限检查 ===")
    print("1. 请打开系统偏好设置 -> 安全性与隐私 -> 隐私 -> 辅助功能")
    print("2. 点击左下角的锁图标解锁设置")
    print("3. 找到并勾选 Terminal 或 iTerm2（取决于你使用的终端）")
    print("4. 如果没有找到终端程序，请点击 + 号添加")
    print("\n设置完成后按回车继续...")
    input()

def main():
    # 检查权限
    check_permissions()
    
    # 设置pyautogui的安全设置
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    
    print("\n监控已启动，按F12停止...")
    print("=== 设置监控区域 ===")
    print("1. 请将鼠标移动到断开连接开关的位置")
    print("2. 保持鼠标位置不动")
    print("3. 等待3秒记录位置...")
    
    # 等待3秒记录位置
    time.sleep(3)
    x, y = pyautogui.position()
    print(f"记录的鼠标位置: x={x}, y={y}")
    
    # 设置监控区域（以鼠标位置为中心，上下左右各100像素）
    region = (x-100, y-100, 200, 200)
    print(f"将监控以下区域：")
    print(f"x={region[0]}, y={region[1]}, width={region[2]}, height={region[3]}")
    print("按回车继续，Ctrl+C取消...")
    input()
    
    # 加载模板图片
    template = cv2.imread('disconnected.png')
    if template is None:
        print("错误：找不到模板图片 'disconnected.png'")
        return
    
    # 转换模板图片为灰度图
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    
    # 设置匹配阈值
    threshold = 0.8
    
    # 创建键盘监听器
    def on_press(key):
        if key == keyboard.Key.f12:
            print("\n停止监控")
            return False
    
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    print("开始监控...")
    
    try:
        while listener.running:
            try:
                # 截取屏幕指定区域
                screenshot = pyautogui.screenshot(region=region)
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
                
                # 模板匹配
                result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                # 如果匹配度超过阈值，执行点击
                if max_val >= threshold:
                    print(f"检测到断开状态，匹配度: {max_val:.2f}")
                    # 计算点击位置（相对于监控区域）
                    click_x = region[0] + region[2]//2
                    click_y = region[1] + region[3]//2
                    # 执行点击
                    pyautogui.click(click_x, click_y)
                    print(f"已点击位置: x={click_x}, y={click_y}")
                    # 等待一段时间再继续监控
                    time.sleep(2)
                else:
                    print(f"当前匹配度: {max_val:.2f}", end='\r')
                
                # 短暂延迟，避免CPU占用过高
                time.sleep(0.5)
                
            except Exception as e:
                print(f"\n发生错误: {str(e)}")
                print("请检查权限设置是否正确")
                time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n程序已停止")
    finally:
        listener.stop()

if __name__ == "__main__":
    main()