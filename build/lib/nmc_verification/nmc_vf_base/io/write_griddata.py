
import numpy as np
import math
import nmc_verification.nmc_vf_base.basicdata as bd

def write_to_micaps4(da,path = "a.txt",effectiveNum = 6):
    """
    输出micaps4格式文件
    :param micaps_abspath:生成文件绝对路径
    :param grid_data:网格数据
    """
    grid = bd.get_grid_of_data(da)
    nlon = grid.nlon
    nlat = grid.nlat
    slon = grid.slon
    slat = grid.slat
    elon = grid.elon
    elat = grid.elat
    dlon = grid.dlon
    dlat = grid.dlat
    level = grid.levels[0]
    stime = grid.stime_str
    year = stime[0:4]
    month = stime[4:6]
    day = stime[6:8]
    hour = stime[8:10]
    hour_range = str(grid.ddt_int)
    values = da.values
    grid_values = np.squeeze(values)
    vmax = math.ceil(max(grid_values.flatten()))
    vmin = math.ceil(min(grid_values.flatten()))

    dif = (vmax - vmin) / 10.0
    if dif ==0:
        inte = 1
    else:
        inte = math.pow(10, math.floor(math.log10(dif)))
    # 用基本间隔，将最大最小值除于间隔后小数点部分去除，最后把间隔也整数化
    r = dif / inte
    if r < 3 and r >= 1.5:
        inte = inte * 2
    elif r < 4.5 and r >= 3:
        inte = inte * 4
    elif r < 5.5 and r >= 4.5:
        inte = inte * 5
    elif r < 7 and r >= 5.5:
        inte = inte * 6
    elif r >= 7:
        inte = inte * 8
    vmin = inte * ((int)(vmin / inte) - 1)
    vmax = inte * ((int)(vmax / inte) + 1)

    end = len(path)
    start = max(0, end - 16)

    title = ("diamond 4 " + path[start:end] + "\n"
             +year + " "+ month + " " + day+ " " +hour+ " " + hour_range +" " + str(level)+"\n"
            + str(grid.dlon) + " " + str(grid.dlat) + " " + str(grid.slon) + " " + str(grid.elon) + " "
            + str(grid.slat) + " " + str(grid.elat) + " " + str(grid.nlon) + " " + str(grid.nlat) + " "
            + str(inte) + " " + str(vmin) + " " + str(vmax) + " 1 0")


    # 第一行标题
    title0 = 'diamond 4 %s\n' % stime
    # 第二行标题
    title1 = '%s %s %s %s %s 999 %s %s %s %s %s %s %d %d 4 %s %s 2 0.00' \
             % (year, month, day, hour, hour_range,
                dlon, dlat,
                slon, elon, slat,
                elat, nlon, nlat, vmax, vmin)
    #title = title0 + title1
    # 二维数组写入micaps文件
    format_str = "%." + str(effectiveNum) + "f "

    np.savetxt(path, grid_values, delimiter=' ',
               fmt=format_str, header=title, comments='')
    print('Create [%s] success' % path)

def write_to_nc(da,path = "a.txt",scale_factor = 0.01):

    encodingdict = {da.name:{
                        'dtype': 'int16',
                        'scale_factor': scale_factor,
                        'zlib': True}
                    }
    da.to_netcdf(path,encoding = encodingdict)