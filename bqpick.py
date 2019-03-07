"""
This stuff enables picking of interface points
from cross-section images or other images
"""

import bqplot as bq
import ipywidgets as widgets
import numpy as np


def import_cs(image_path):
    """Import the image of the cross-section"""
    with open(image_path, 'rb') as fid:
        raw_img = fid.read()

    ipyimg = widgets.Image(value=raw_img, format=image_path[-3:])
    return ipyimg


def set_cs_dim(x_dim, z_dim):
    """Set the scale of the cross section in model coordinates"""

    scales = {'x': bq.LinearScale(min=np.min(x_dim), max=np.max(x_dim)),
              'y': bq.LinearScale(min=np.min(z_dim), max=np.max(z_dim))}

    return scales


def add_del(scale, img):
    """Add function for ipywidget buttons to add and delete points"""

    scat = bq.Scatter(x=[], y=[], scales=scale, colors=['orange'],
                      enable_move=True)

    image = bq.Image(x=np.array([scale['x'].min, scale['x'].max]),
                     y=np.array([scale['y'].min, scale['y'].max]),
                     image=img, scales=scale, enable_hover=False)

    interact_control = widgets.ToggleButtons(options=['Add', 'Delete'],
                                             style={'button_width': '130px'})

    def change_interact(shape):
        """Give a meaning to the buttons."""
        interact_params = {
            'Add': {'interactions': {'click': 'add'},
                    'enable_move': True},
            'Delete': {'interactions': {'click': 'delete'},
                       'enable_move': False}
        }

        for param, value in interact_params[interact_control.value].items():
            setattr(scat, param, value)
    interact_control.observe(change_interact)

    fig = bq.Figure(title='Cross-section', marks=[image, scat],
                    padding_x=0, padding_y=0)
    fig.axes = [bq.Axis(scale=scale['x']), bq.Axis(scale=scale['y'],
                                                   orientation='vertical')]

    return widgets.VBox([fig, interact_control])
    # return widgets.HBox([widgets.VBox([fig, interact_control]),
    #                    print(scat.x, scat.y)])
