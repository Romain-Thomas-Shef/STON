"""
This file is part of the STON project (P.I. E. Dammer)
It contains the functions related to file exploration


Author: R. Thomas
Place: U. of Sheffield, RSE team
Year: 2024-2025
"""
###standard library
import os

###Third party library
from matplotlib import font_manager
import numpy
from PIL import Image, ImageDraw, ImageFont

def make_mashup(config, imageswithpath):
    '''
    This function creates a mashup from different images

    Parameters
    ----------
    Config  :   dict
                configuration of the mashup.

    imageswithpath:   list
                    of files with path

    Return
    ------
    mashupimage     str
                    path to new image
    '''
    ##retrieve the images with their path
    fullpath_images = {}
    for image in imageswithpath:
        for configimage in config:
            if configimage == os.path.basename(image):
                fullpath_images[image] = config[configimage]

    ##sort the dictionary
    sorted_images_by_order = sorted(fullpath_images, key=fullpath_images.get)

    ##load the images
    images = []
    for image in sorted_images_by_order:
        images.append(Image.open(image))

    ##get the sizes
    all_width = []
    all_height = []
    for i in images:
        all_width.append(i.size[0])
        all_height.append(i.size[1])

    ##final size
    total_width = sum(all_width)
    total_height = max(all_height)


    #create an empty image
    final_im = Image.new('RGB', (total_width, total_height))

    ##and finally the mashup
    x_offset = 0
    for i in images:
        final_im.paste(i, (x_offset, 0))
        x_offset += i.size[0]

    ###save the image
    final_im.save(config['name'])

    return config['name']

def create_meta_image(image_list, final_image_name, conf):
    '''
    This function creates a meta image with all the images
    given in the list

    The final image is made of N column (given in the configuration)
    and the number of lines depends on the number of images

    Parameters
    ----------
    image_list	list
                with paths to images             

    final_image_name    str
                        this is the name of the image that will be saved on disc

    conf        dictionary
                main configuration of ston
    '''
    ###In a single loop compute the number of lines and
    ###the height and width of each row
    colindiv = 0
    line = 0
    layout = {}
    for n,image in enumerate(image_list):
        del n ##we don't need it

        #update the dictionaries if we are on a newline
        if f'{line}' not in layout:
            layout[f'{line}'] = {}

        ##open the image
        im = Image.open(image)

        ##We downgrade the quality to avoid a heavy final image
        im.thumbnail((im.width/conf['Meta_image_options']['downgrade_factor'],
                      im.height/conf['Meta_image_options']['downgrade_factor']))

        if conf['Meta_image_options']['name_on_images'] is True:
            ###Find an available font and create the final font
            font = font_manager.FontProperties(family='sans-serif', weight='bold')
            pilfont = ImageFont.truetype(font_manager.findfont(font),
                                         conf['Meta_image_options']['meta_txt_fontsize'])

            ##Add the image name to the image
            draw = ImageDraw.Draw(im)
            draw.text((0,0), os.path.basename(image),
                      most_contrasted_color(compute_avg_color(numpy.array(im))),
                      font=pilfont)


        ##Fill up the dictionries
        layout[f'{line}'][f'{colindiv}'] = {'data': im}

        ###if we are at the last column we need to change line
        ###and reinitialise the column counter
        if colindiv >= conf['Meta_image_options']['ncol_meta_image'] - 1:
            colindiv = 0
            line += 1
        else:
            ##Go to next column
            colindiv += 1

    ###create the final width and height of each line
    ###between each image we add a space of 10 pix gap
    gap = 10
    all_line_sum_width = [] ##we will keep the width of each full line
    all_line_max_height = [] ##and the max height of each full line

    for line in layout:
        line_width = [] ##gather all widths of each image
        line_height = [] ##gather all height of each image

        for column in layout[line]:
            line_width.append(layout[line][column]['data'].width + gap)
            line_height.append(layout[line][column]['data'].height + gap)

        all_line_sum_width.append(sum(line_width)) ##keep the sum of the widths
        all_line_max_height.append(max(line_height)) ##and the max height on that line

    ##the width of the final image if the max width between each line
    ##and the height of the final image is the sum of each maximum height
    ##of each line
    final_image_width = max(all_line_sum_width)
    final_image_height = sum(all_line_max_height)

    ###prepare the final image
    final_image = Image.new("RGBA", (final_image_width, final_image_height) )

    ##create the final image
    width_offset = 0
    height_offset = 0
    l = 0 ###keep track of line
    for line in layout:
        for column in layout[line]:
            #Extract data
            data = layout[line][column]['data']

            ##add the individual image to the final image
            final_image.paste(data, (width_offset, height_offset))

            ##update the offset
            width_offset += data.width + gap

        ##when done with a line, reinitialise width and update height offset
        width_offset = 0
        height_offset += all_line_max_height[l]
        l += 1

    ##save it on disc
    final_image.save(final_image_name)


def compute_avg_color(data):
    '''
    This function computes the average color of an image
    
    Parameters
    ----------
    data    :   numpy array
                image data

    Return
    ------
    RGB     :   tuple
                R, G, B average color
    '''
    avg_color = data.mean(axis=(0,1))
    rgb = tuple(map(int, avg_color))

    return rgb


def most_contrasted_color(rgb):
    """
    Find the most contrasted color (black or white) for the given RGBA color.
    
    Parameters
    ----------
    tgb     tuple
            Input color as (R, G, B), where each value is in [0, 255].
    
    Returns
    -------
    font_color  : tuple
                  The most contrasted color as (R, G, B).
    """
    ##unpack the color
    r, g, b = rgb

    # Calculate the perceived brightness (source: https://www.w3.org/TR/AERT/#color-contrast)
    brightness = 0.299 * r + 0.587 * g + 0.114 * b

    # Choose black or white based on brightness
    if brightness > 128:
        font_color = (0, 0, 0)  # Black
    else:
        font_color = (255, 255, 255) #white

    return font_color
