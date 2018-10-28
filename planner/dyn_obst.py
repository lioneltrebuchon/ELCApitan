def dyn_obst(drone_bl, drone_tr, xwidth,ywidth):

    dox, doy = [],[]

    #x coordinates
    for i in range(drone_bl[0],drone_tr[0]):
        # y coordinates 
        for j in range(drone_bl[1],drone_tr[1]):
            # store indices of the obstacle 
            dox.append(i)
            doy.append(j)

    #turn indices in matrix 
    obmap_dyn = [[False for i in range(xwidth)] for i in range(ywidth)]
    for i in dox:
        for j in doy: 
            obmap_dyn[i][j] = True

    return dox, doy, obmap_dyn
