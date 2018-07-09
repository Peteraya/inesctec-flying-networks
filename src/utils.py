import numpy as np

def rotate(size, x, y, angle):
    if angle == 90:
        return y, size - 1 - x
    elif angle == 180:
        return size - 1 - x, size - 1 - y
    elif angle == 270:
        return size - 1 - y, x

def rotation(df, size, angle):
    for i in range(0, len(df)):
        new_x, new_y = rotate(size, df.loc[i, 'x'], df.loc[i, 'y'], angle)
        df.loc[i, 'x'] = new_x
        df.loc[i, 'y'] = new_y

def simmetric(size, x, y, angle_axis):
    if angle_axis == 0:
        return x, size - 1 - y
    elif angle_axis == 45:
        return y, x
    elif angle_axis == 90:
        return size - 1 - x, y
    elif angle_axis == 135:
        return size - 1 - y, size - 1 - x 


def simmetry(df, size, angle_axis):
    for i in range(0, len(df)):
        new_x, new_y = simmetric(size, df.loc[i, 'x'], df.loc[i, 'y'], angle_axis)
        df.loc[i, 'x'] = new_x
        df.loc[i, 'y'] = new_y