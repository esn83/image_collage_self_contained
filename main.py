import os
import pygame as pg
from pg_tools import remove_image_borders
from pg_camera import Camera
import random

display_w = 1800
display_h = 900

pg.init()
pg.display.set_mode((display_w,display_h))

# get files in folder and subfolders with ext(s). casesensitive if chosen.
def get_ext_file_paths(folder, ext_list, case_sensitive=False):
    if not isinstance(ext_list, list):
        raise Exception('extension list not list', str(ext_list), type(ext_list))
    for ext in ext_list:
        if not isinstance(ext, str):
            raise Exception('extension not string', str(ext), type(ext))
    if not isinstance(folder, str):
        raise Exception('folder not string', str(folder), type(folder))
    elif not os.path.isdir(folder):
        raise Exception('folder does not exist', folder)
    else:
        res_files = []
        for current_folder, subfolders, files in os.walk(folder):
            for f in files:
                res_path = os.path.join(current_folder, f)
                if len(ext_list) == 0:
                    res_files.append(res_path)
                else:
                    for ext in ext_list:
                        if not case_sensitive:
                            if f.upper().endswith('.'+ext.upper()):
                                res_files.append(res_path)
                        else:
                            if f.endswith('.'+ext):
                                res_files.append(res_path)
        return res_files

image_path = 'images_1'
image_path_list = get_ext_file_paths(image_path, [])

# load images from file to surface
def load_all_images(image_path_list):
    image_list = []
    for img_path in image_path_list:
        img = pg.image.load(img_path)
        if img.get_alpha():
            img = img.convert_alpha()
        else:
            img = img.convert()
            # if colorkey != None:
            #     img.set_colorkey(colorkey)
        image_list.append(img)
    return image_list

image_list = load_all_images(image_path_list)

image_list_cropped = []
for img in image_list:
    cropped_img, has_borders, border_color = remove_image_borders(img, True, None)
    if has_borders:
        if border_color != pg.Color(0,0,0):
            print('non-black border removed :',image_path_list[image_list.index(img)], border_color)
        else:
            print('black border removed     :',image_path_list[image_list.index(img)])
    image_list_cropped.append(cropped_img)

# scale images
def scale_image(img: pg.Surface, desired_height):
    w, h = img.get_width(), img.get_height()
    scale = desired_height/h
    w *= scale
    h *= scale
    return pg.transform.scale(img.copy(), (int(w), int(h)))

image_scaled_list = []
img_scaled_height = 421
for img in image_list_cropped:
    image_scaled_list.append(scale_image(img, img_scaled_height))
# print(len(image_scaled_list))

def shuffle_list():
    random.shuffle(image_scaled_list)

def scatter_blit_images(surface, image_list, min_x, max_x, min_y, max_y, loops):
    for _ in range(loops):
        x = random.randint(min_x,max_x)
        y = random.randint(min_y,max_y)
        img = random.choice(image_list_cropped)
        img_rect = img.get_rect()
        img_rect.x = x
        img_rect.y = y
        surface.blit(img, img_rect)

# blit images to screen
screen = pg.display.get_surface()
collage_surf_w = 10000
collage_surf_h = 7000
collage_surf = pg.Surface((collage_surf_w,collage_surf_h))
collage_rect = collage_surf.get_rect()

# scatter_blit_images(collage_surf, image_scaled_list, 100, 9000, 100, 6000, 2500)

def blit_images():
    x_start = 150
    max_width = 10000
    y_start = 100
    x_min_spacing = 5
    y = y_start
    y_spacing = 5
    used_surfs = []

    def get_row():
        width_count = x_start*2
        surf_row = []
        for surf in image_scaled_list:
            if surf in used_surfs:
                continue
            elif (width_count + surf.get_width()) > max_width:
                continue
            else:
                width_count += surf.get_width() + x_min_spacing
                used_surfs.append(surf)
                surf_row.append(surf)
        return surf_row

    surf_rows = []
    while len(used_surfs) < len(image_scaled_list):
        surf_rows.append(get_row())

    def get_surf_row_width(surf_row):
        width = 0
        for surf in surf_row:
            width += surf.get_width()
        return width

    for surf_row in surf_rows:
        row_width = get_surf_row_width(surf_row)
        try:
            x_spacing_row = (max_width - row_width - 2*x_start - len(surf_row)*x_min_spacing) / (len(surf_row)-1) + x_min_spacing
        except ZeroDivisionError as e:  # if len(surf_row) is 1 in the above code '(len(surf_row)-1)' it results in zero division error
            x_spacing_row = x_min_spacing
        x = x_start
        for temp_surf in surf_row:
            rect = temp_surf.get_rect()
            rect.x = x
            rect.y = y
            collage_surf.blit(temp_surf,rect)
            x += temp_surf.get_width() + x_spacing_row
        y += img_scaled_height + y_spacing        

    print("rows : ", len(surf_rows))
    print("images : ", len(used_surfs))
    if len(surf_rows) > 0:
        img_height_cm = (collage_surf_h - y_start*2 - y_spacing*(len(surf_rows))) / len(surf_rows) / 100
        print("img_h cm: ",img_height_cm)

# save image as file
def save_surf_to_file(surf, file_name):
    pg.image.save(surf, file_name)

# camera
camera = Camera(display_area_p=(0,0,display_w,display_h),
                world_surf_p=collage_surf,
                enable_mouse_edge_scroll_p=True,   # bool
                enable_right_mouse_pan_p=True,     # bool
                enable_zoom_p=True,                # bool
                enable_smoothness_p=False,         # bool
                zoom_scale_p=3.1,                  # zoom scale, larger means zoomed in, smaller means zoomed out
                zoom_scale_min_p=1,                # min zoom scale
                zoom_scale_max_p=10,               # max zoom scale
                zoom_step_p=0.3,                   # increase/decrease of zoom_scale pr zoom step
                )

shuffle_list()
blit_images()

clock = pg.time.Clock()

# simple game loop
keepGameRunning = True
while keepGameRunning:
    for event in pg.event.get():
        if event.type == pg.QUIT:
           keepGameRunning = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                keepGameRunning = False
            elif event.key == pg.K_r:
                screen.fill(pg.Color(0,0,0))
                collage_surf.fill(pg.Color(0,0,0))
                shuffle_list()
                blit_images()
            elif event.key == pg.K_p:
                save_surf_to_file(collage_surf, 'collage.png')
        camera.events(event)
    camera.update()
    camera.draw(screen, 0)
    pg.display.update()
    clock.tick(60)