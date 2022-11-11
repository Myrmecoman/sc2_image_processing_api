import pyautogui


# provides clicking locations
class clicker_helper:

    idle_workers = (40, 780)
    army = (115, 780)

    # clicking positions for control group buttons
    control_groups = [(560, 843), (627, 843), (695, 843), (765, 843), (830, 843), (900, 843), (970, 843), (1035, 843), (1105, 843), (1175, 843)]

    right_window = [ # if you want to click instead of using hotkeys
        [(1575, 880), (1640, 880), (1713, 880), (1780, 880), (1853, 880)],
        [(1575, 950), (1640, 950), (1713, 950), (1780, 950), (1853, 950)],
        [(1575, 1020), (1640, 1020), (1713, 1020), (1780, 1020), (1853, 1020)]
    ]
    middle_window = [ # might be useful for removing units from selected group
        [(690, 920), (746, 920), (805, 920), (862, 920), (920, 920), (980, 920), (1035, 920), (1090, 920),],
        [(690, 975), (746, 975), (805, 975), (862, 975), (920, 975), (980, 975), (1035, 975), (1090, 975),],
        [(690, 1035), (746, 1035), (805, 1035), (862, 1035), (920, 1035), (980, 1035), (1035, 1035), (1090, 1035),]
    ]

    def __init__(self):
        return

    def select_group(self, id):
        pyautogui.moveTo(self.control_groups[id][0], self.control_groups[id][1], duration=0.0, _pause=False)
        pyautogui.click()
    
    def select_idle_workers(self):
        pyautogui.moveTo(self.idle_workers[0], self.idle_workers[1], duration=0.0, _pause=False)
        pyautogui.click()
    
    def select_army(self):
        pyautogui.moveTo(self.army[0], self.army[1], duration=0.0, _pause=False)
        pyautogui.click()
    
    def click_right_window(self, x, y):
        pyautogui.moveTo(self.right_window[x][y][0], self.right_window[x][y][1], duration=0.0, _pause=False)
        pyautogui.click()
    
    def click_middle_window(self, x, y):
        pyautogui.moveTo(self.middle_window[x][y][0], self.middle_window[x][y][1], duration=0.0, _pause=False)
        pyautogui.click()

    def put_selected_in_group(self, id):
        pyautogui.keyDown("shift") # shift + number adds units to a control group on my keybinds, change accordingly to yours
        pyautogui.press(str(id))
        pyautogui.keyUp("shift")