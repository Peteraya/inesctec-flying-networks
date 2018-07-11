import numpy as np
import pandas as pd

def rotate(size, x, y, angle):
    if angle == 90:
        return y, size - 1 - x
    elif angle == 180:
        return size - 1 - x, size - 1 - y
    elif angle == 270:
        return size - 1 - y, x


def simmetric(size, x, y, angle_axis):
    if angle_axis == 0:
        return x, size - 1 - y
    elif angle_axis == 45:
        return y, x
    elif angle_axis == 90:
        return size - 1 - x, y
    elif angle_axis == 135:
        return size - 1 - y, size - 1 - x 

#transform_scenarios(frame, 10, rotate, 90)
#transform_scenarios(frame, 10, simmetric, 0)
def transform_scenarios(df, size, function, angle):
    new_df = pd.DataFrame(columns = ['x', 'y', 'dataRateMbps'])
    for y in range(0, size):
        for x in range(0, size):
            i = y * size + x
            new_df.loc[i, 'x'] = x
            new_df.loc[i, 'y'] = y

    for y in range(0, size):
        for x in range(0, size):
            i = y * size + x
            new_x, new_y = function(size, df.loc[i, 'x'], df.loc[i, 'y'], angle)
            new_df.loc[new_y*size + new_x, 'dataRateMbps'] = df.loc[i, 'dataRateMbps']
    return new_df
