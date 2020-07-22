"""
MIT License

Copyright (c) [2020] [Jan Niederau]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import bqplot as bq
import ipywidgets as widgets
import numpy as np
import pandas as pd


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

def write_data(fig, profile_direction: str = 'x', formation: str = 'basement') -> pd.DataFrame:
    """Write picked data to a dataframe

    Args:
        fig (widget): widget object with coordinate data
        profile_direction (string, optional): direction of profile. If 'x', 'y' will be set
        to 1, if 'y', 'x' will be set to one. Defaults to 'x'.
        formation (string, optional): Name of picked formation. Defaults to 'basement'.
    """
    if profile_direction=='x':
        x = fig.children[0].marks[1].x
        y = np.ones_like(x)
        z = fig.children[0].marks[1].y
    elif profile_direction=='y':
        y = fig.children[0].marks[1].x
        x = np.ones_like(y)
        z = fig.children[0].marks[1].y
    df_dict = {'X':x, 'Y':y, 'Z':z, 'formation':formation}
    df = pd.DataFrame.from_dict(df_dict)
    
    return df

def save_data(df: pd.DataFrame, path: str='./'):
    """Safe a generated dataframe with data of a formation.
    Args:
        df (pd.DataFrame): dataframe containing picked interface data
        path (str, optional): path to save file. Defaults to './'.
    """
    try:
        name = df['formation'].unique()[0]
    except IndexError:
        print("Formation name could not be read.")
    df.to_csv(path_or_buf=path+name+'.csv', index=False)
    print(f"File saved to {path} with name {name}.csv")