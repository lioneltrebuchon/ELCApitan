from math import ceil, floor
def obstrange(twr,wt,res):
    x = twr[0]
    y = twr[1]
    range_bl = [int(i) for i in [x-wt/2, y-wt/2, 0]]
    range_tr = [int(i) for i in [x+wt/2, y+wt/2, 0]]
    return range_bl,range_tr
