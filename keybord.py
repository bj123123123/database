import win32con
import win32api
import time,sys
import keyboard

key_map = {
    "0": 49, "1": 50, "2": 51, "3": 52, "4": 53, "5": 54, "6": 55, "7": 56, "8": 57, "9": 58,
    "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
    "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
    "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90, 
    "a": 97, "b": 98, "c": 99, "d": 100, "e": 101, "f": 102, "g": 103, "h": 104, "i": 105, "j": 106,
    "k": 107, "l": 108, "m": 109, "n": 110, "o": 111, "p": 112, "q": 113, "r": 114, "s": 115, "t": 116,
    "u": 117, "v": 118, "w": 119, "x": 120, "y": 121, "z": 122, 
    "VK_ALT": 18, "VK_CRTL":17, "VK_RETURN":13
}
  
  
def key_down(key):
    """
    函数功能：按下按键
    参    数：key:按键值
    """
    key = key.upper()
    vk_code = key_map[key]
    win32api.keybd_event(vk_code,win32api.MapVirtualKey(vk_code,0),0,0)
  
  
def key_up(key):
    """
    函数功能：抬起按键
    参    数：key:按键值
    """
    key = key.upper()
    vk_code = key_map[key]
    win32api.keybd_event(vk_code, win32api.MapVirtualKey(vk_code, 0), win32con.KEYEVENTF_KEYUP, 0)
  
  
def key_press(key):
    """
    函数功能：点击按键（按下并抬起）
    参    数：key:按键值
    """
    key_down(key)
    time.sleep(0.02)
    key_up(key)

def move(x, y):
  """
  函数功能：移动鼠标到指定位置
  参  数：x:x坐标
       y:y坐标
  """
  win32api.SetCursorPos((x, y))
 
 
def get_cur_pos():
  """
  函数功能：获取当前鼠标坐标
  """
  p={"x":0,"y":0}
  pos = win32api.GetCursorPos()
  print(pos)
  p['x']=pos[0]
  p['y']=pos[1]
  return p
 
 
def left_click():
  """
  函数功能：鼠标左键点击
  """
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
 
 
def right_click():
  """
  函数功能：鼠标右键点击
  """
  win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN | win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
 
 
def left_down():
  """
  函数功能：鼠标左键按下
  """
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
 
 
def left_up():
  """
  函数功能：鼠标左键抬起
  """
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
 
 
def right_down():
  """
  函数功能：鼠标右键按下
  """
  win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
 
 
def right_up():
  """
  函数功能：鼠标右键抬起
  """
  win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)


def run():
    #time.sleep(5)
    #get_cur_pos()
    pos1=[166,1070]
    move(pos1[0],pos1[1])
    left_click()
    time.sleep(0.5)
    pos1=[217,13]
    move(pos1[0],pos1[1])
    left_click()
    time.sleep(0.5)

    pos1=[533,508]
    move(pos1[0],pos1[1])
    left_click()
    left_click()
    time.sleep(0.5)

    right_click()
    pos1=[580,522]
    move(pos1[0],pos1[1])
    time.sleep(0.5)

    left_click()
    time.sleep(0.5)




    pos1=[214,1070]
    move(pos1[0],pos1[1])
    left_click()
    time.sleep(0.5)

    pos1=[69,30]
    move(pos1[0],pos1[1])
    left_click()
    time.sleep(0.5)
    pos1=[98,142]
    move(pos1[0],pos1[1])
    left_click()
    time.sleep(0.5)

    key_press("VK_RETURN")

    #pos1=[316,18]
    #move(pos1[0],pos1[1])


TABPOS=[50,15]
CLOSEPOS=[215,15]
def run1():
    SLEEPTIME=0.8
    pos1=[166,1070]
    move(pos1[0],pos1[1])
    left_click()
    time.sleep(SLEEPTIME)
	
    pos1=[83,968]
    move(pos1[0],pos1[1])
    left_click()
    time.sleep(0.5)
		
		
    move(TABPOS[0],TABPOS[1])
    left_click()
    time.sleep(SLEEPTIME)

    pos1=[533,508]
    move(pos1[0],pos1[1])
    left_click()
    left_click()
    time.sleep(SLEEPTIME)
        
    keyboard.press_and_release('ctrl+c')
    time.sleep(SLEEPTIME)

    keyboard.press_and_release('ctrl+w')
    time.sleep(SLEEPTIME)

    pos1=[1803,12]
    move(pos1[0],pos1[1])
    left_click()
    time.sleep(SLEEPTIME)

    pos1=[214,1070]
    move(pos1[0],pos1[1])
    left_click()
    time.sleep(SLEEPTIME)

    keyboard.press_and_release('ctrl+v')
    key_press("VK_RETURN")
    time.sleep(SLEEPTIME)

    pos1=[1803,12]
    move(pos1[0],pos1[1])
    left_click()
    time.sleep(SLEEPTIME)


get_cur_pos()
count=20
for i in range(0,count):
    run1()
   