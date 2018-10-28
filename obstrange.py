from math import ceil, floor
def obstrange(twr,wt,res):
    x = twr[0]
    y = twr[1]
    range_bl = [floor(i/res) for i in [x-wt/2, y-wt/2, 0]]
    range_tr = [ceil(i/res) for i in [x+wt/2, y+wt/2, 0]]
    return range_bl,range_tr
