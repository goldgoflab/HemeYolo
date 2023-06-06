import cv2
import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from PIL import Image
def drawer(image = None, res_df=None, category='box', label_flag=False, counting=False):
    """

    :param res_df: df from computation
    :param image: input image
    :param category: 'box' or points
    :param label_flag: put label on the plots
    :param legend_flag: put legands besides the plots
    :return: a image
    """
    image = image.copy()
    name_list = list(set(res_df['prediction']))
    num_colors= 24#len(name_list)
    celltype_list = ['B1','B2', 'E1', 'E4', 'ER1','ER2','ER3','ER4','ER5','ER6',
                     'L2','L4', 'M1', 'M1a','M2', 'M3', 'M4', 'M5', 'M6',
                     'MO2','PL2','PL3','U1','U4']
    color_palette = [(int(list(_col)[0] *255), int(list(_col)[1] *255), int(list(_col)[2] *255 )) \
                     for _col in sns.color_palette("husl", num_colors)]
    color_palette_unit = [_col for _col in sns.color_palette("husl", num_colors)]
    color_mappings = {}
    color_mappings_unit = {}
    for _name in name_list:
        color_mappings[_name] = color_palette[celltype_list.index(_name)]
        color_mappings_unit[_name] = color_palette_unit[celltype_list.index(_name)]
    colors = [color_mappings[_name] for _name in res_df['prediction']]
    #print(colors[0])
    res_df['colors'] = colors





    assert category in ['box', 'points'], 'something wrong'
    if category =='box':
        print('Drawing boxes')
        for row in res_df.index:
            x1, x2, y1, y2, _color, pred= res_df.iloc[row][['x1', 'x2', 'y1', 'y2', 'colors', 'prediction']]
            image = cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), _color, 3)
            if label_flag == True:
                font = cv2.FONT_HERSHEY_SIMPLEX
                color = (255, 0, 0)
                thickness = 5
                fontScale = 5
                image = cv2.putText(image, pred, (int(x1), int(y1)), font,
                                    fontScale, color, thickness, cv2.LINE_AA)

    else:
        print('Drawing points')
        for row in res_df.index:
            _center, _color, pred= res_df.iloc[row][['center', 'colors', 'prediction']]
            x_c, y_c = _center
            image = cv2.circle(image, (x_c, y_c), 0, _color, 10)
            if label_flag == True:
                font = cv2.FONT_HERSHEY_SIMPLEX
                color = (0, 0, 0)
                thickness = 5
                fontScale = 1
                image = cv2.putText(image, pred, (int(x_c) -20, int(y_c)-20), font,
                                    fontScale, color, thickness, cv2.LINE_AA)


    if counting == True:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        #plt.subplot(1, 2, 1)  # row 1, col 2 index 1
        ax1.imshow(Image.fromarray(image))
        ax1.tick_params(
    axis='both',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off
        ax1.set_yticks([])




        plt.subplot(1, 2, 2)  # index 2
        color_list = [color_mappings_unit[_name] for _name in name_list]
        height = [list(res_df['prediction']).count(_name) for _name in name_list]
        bars = name_list
        #x_pos = np.arange(max(height)+5)
        x_pos = np.arange(len(bars))
        # Create bars with different colors
        ax2.barh(x_pos, height, color=color_list)  # , orientation='horizontal'
        plt.yticks(x_pos, name_list)
        # Create names on the x-axis
        #plt.xticks(x_pos, bars)
    else:
        return plt.matshow(image)


