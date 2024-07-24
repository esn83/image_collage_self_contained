import pygame as pg
from functions import get_first_element_that_has_n_equal_elements

def remove_image_borders(surface, guess_border_color=True, border_color_rgb_list=None):
    w = surface.get_width() -1
    h = surface.get_height() -1
    left_pixel = None
    right_pixel = None
    top_pixel = None
    bottom_pixel = None
    has_borders = False

    def get_corner_pixel_colors_list(surface):
        top_left = surface.get_at((0,0))
        top_right = surface.get_at((surface.get_width()-1,0))
        bottom_right = surface.get_at((surface.get_width()-1,surface.get_height()-1))
        bottom_left = surface.get_at((0,surface.get_height()-1))
        corner_list = [top_left,top_right,bottom_right,bottom_left]
        return corner_list

    def compare_pixel_color_to_border_color(surface, pixel_coords, border_color_rgb_list):
        pixel = surface.get_at(pixel_coords)
        color_match = pixel.r == border_color_rgb_list[0] and pixel.g == border_color_rgb_list[1] and pixel.b == border_color_rgb_list[2]
        return color_match

    if border_color_rgb_list == None and guess_border_color:
        border_color = get_first_element_that_has_n_equal_elements(get_corner_pixel_colors_list(surface), 3)
        if isinstance(border_color,pg.Color):
            border_color_rgb_list = [border_color.r,border_color.g,border_color.b]
            has_borders = True
    else:
        border_color = None

    if border_color_rgb_list != None:
        # find left pixel
        for x in range(0,w):
            for y in range(0,h):
                if not compare_pixel_color_to_border_color(surface,(x,y),border_color_rgb_list):
                    left_pixel = (x,y)
                    break
            if left_pixel != None:
                break
        # find right pixel
        for x in range(w,0,-1):
            for y in range(0,h):
                if not compare_pixel_color_to_border_color(surface,(x,y),border_color_rgb_list):
                    right_pixel = (x,y)
                    break
            if right_pixel != None:
                break
        # find top pixel
        for x in range(0,h):
            for y in range(0,w):
                if not compare_pixel_color_to_border_color(surface,(y,x),border_color_rgb_list):
                    top_pixel = (y,x)
                    break
            if top_pixel != None:
                break
        # find bottom pixel
        for x in range(h,0,-1):
            for y in range(0,w):
                if not compare_pixel_color_to_border_color(surface,(y,x),border_color_rgb_list):
                    bottom_pixel = (y,x)
                    break
            if bottom_pixel != None:
                break

        crop_rect = pg.Rect(left_pixel[0],
                            top_pixel[1],
                            right_pixel[0]-left_pixel[0]+1,
                            bottom_pixel[1]-top_pixel[1]+1
                            )
        cropped_surface = surface.subsurface(crop_rect)
        return cropped_surface, has_borders, border_color
    else:
        return surface, has_borders, border_color