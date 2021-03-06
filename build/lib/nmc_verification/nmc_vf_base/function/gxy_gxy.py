import numpy as np
import nmc_verification.nmc_vf_base.basicdata as bd
import math
#格点到格点插值
def interpolation_linear(grd, grid, other_info='left'):
    if (grd is None):
        return None

    # 六维转换为二维的值
    dat0 = grd.values
    dat = np.squeeze(dat0)

    grd0 = bd.get_grid_of_data(grd)
    if (grd0.dlon * grd0.nlon >= 360):
        grd1 = bd.grid([grd0.slon, grd0.dlon, grd0.elon + grd0.dlon],[grd0.slat, grd0.dlat, grd0.elat])
        dat1 = np.zeros((grd1.nlat,grd1.nlon))
        dat1[:,0:-1] = dat[:,:]
        dat1[:, -1] = dat[:, 0]
    else:
        dat1 = dat
        grd1 = grd0
    if other_info=='left':
        grd2 = bd.grid(grid.glon,grid.glat,grd0.gtime,grd0.gdtime,grd0.levels,grd0.members)
    else:
        grd2 = grid.copy()

    if (grd2.elon > grd1.elon or grd2.slon < grd1.slon or grd2.elat > grd1.elat or grd2.slat < grd1.slat):
        print("object grid is out range of original grid")
        return None

    #插值处理
    x = ((np.arange(grd2.nlon) * grd2.dlon + grd2.slon - grd1.slon) / grd1.dlon)
    ig = x[:].astype(dtype='int16')
    dx = x - ig
    y = (np.arange(grd2.nlat) * grd2.dlat + grd2.slat - grd1.slat) / grd1.dlat
    jg = y[:].astype(dtype='int16')
    dy = y[:] - jg
    ii, jj = np.meshgrid(ig, jg)
    ii1 = np.minimum(ii + 1, grd1.nlon - 1)
    jj1 = np.minimum(jj + 1, grd1.nlat - 1)
    ddx, ddy = np.meshgrid(dx, dy)
    c00 = (1 - ddx) * (1 - ddy)
    c01 = ddx * (1 - ddy)
    c10 = (1 - ddx) * ddy
    c11 = ddx * ddy
    dat2 = (c00 *dat1[jj, ii] + c10 * dat1[jj1, ii] + c01 * dat1[jj, ii1] + c11 * dat1[jj1, ii1])

    #print(grd2.tostring())
    #print(dat2)
    grd_new = bd.grid_data(grd2,dat2)

    return grd_new

def add(grd1,grd2,other_info = 'left'):
    if(grd1 is None):
        return grd2
    elif(grd2 is None):
        return grd1
    else:
        grid1 = bd.get_grid_of_data(grd1)
        grid2 = bd.get_grid_of_data(grd2)
        slon = max(grid1.slon,grid2.slon)
        elon = min(grid1.elon,grid2.elon)
        slat = max(grid1.slat,grid2.slat)
        elat = min(grid1.elat,grid2.elat)
        if other_info == 'left':
            grid_in = bd.grid([slon,elon,grid1.dlon],[slat,elat,grid1.dlat],grid1.gtime,grid1.gdtime,grid1.levels,grid1.members)
        else:
            grid_in = bd.grid([slon, elon, grid2.dlon], [slat, elat, grid2.dlat], grid2.gtime, grid2.gdtime, grid2.levels,
                              grid2.members)
        grd1_in = interpolation_linear(grd1, grid_in)
        grd2_in = interpolation_linear(grd2, grid_in)
        grd = bd.grid_data(grid_in,grd1_in.values + grd2_in.values)
        return grd
