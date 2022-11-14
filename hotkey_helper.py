import pyautogui


# provides keys to do actions
# /!\ Everything here is keybind dependent !!!
class hotkey_helper:

    scv_build_structure = "w"
    scv_build_advanced_structure = "x"

    build_scv = "a"

    scv_build_command_center = "a"
    scv_build_gas = "z"
    scv_build_depot = "e"
    scv_build_barracks = "q"
    scv_build_eng_bay = "s"
    scv_build_bunker = "w"
    scv_build_turret = "x"
    scv_build_sensor = "c"

    scv_build_ghost_academy = "a"
    scv_build_factory = "q"
    scv_build_armory = "s"
    scv_build_starport = "w"
    scv_build_fusion_core = "x"

    barracks_build_marine = "a"
    barracks_build_reaper = "z"
    barracks_build_marauder = "e"
    barracks_build_ghost = "r"
    
    build_add_on_tech_lab = "w"
    build_add_on_reactor = "x"

    go_to_random_base = "space"
    select_idle_workers = "tab"
    select_army = "F2"

    attack_command = "T"

    def __init__(self):
        return
    
    def put_selected_in_group(self, id):
        pyautogui.keyDown("shift") # shift + number adds units to a control group on my keybinds, change accordingly to yours
        pyautogui.press(str(id))
        pyautogui.keyUp("shift")
    
    # not working yet for some reason
    def select_control_group(self, id):
        pyautogui.press(str(id))
