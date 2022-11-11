# In depth explanation of the clicker helper class

This class contains coordinates of UI buttons. They are exposed by several functions.

### select_group(int)

Takes an int and selects the corresponding group.

### select_idle_workers()

Selects all idle workers using the button on top of the map.

### select_army()

Selects all army units using the button on top of the map.

### click_right_window(int, int)

Clicks the corresponding button on the right window of the game. First int is the row, second is the column.
Ex: when having selected an SCV, if you want to build a barrack do click_right_window(2, 0) then click_right_window(1, 0)

### click_middle_window(int, int)

Clicks the corresponding object on the middle window of the game. When multiple elements are selected, this can be used to get on of them.

### put_selected_in_group(int)

Put selected element(s) in the corresponding group. This uses keyboards keys and therefore can change depending on your keybinds in the game.
