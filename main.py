import time
import screenshot_maker
import minimap_segmenter


print("starting")
time.sleep(4)

start_time = time.time()
screen_infos = screenshot_maker.screen_info(True)
print("%s sec" % (time.time() - start_time))

map_info = minimap_segmenter.minimap_info(screen_infos.minimap, True)

print("done")
