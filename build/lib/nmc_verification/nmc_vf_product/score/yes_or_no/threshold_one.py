import nmc_verification.nmc_vf_base.basicdata as bd
import nmc_verification.nmc_vf_method.yes_or_no as yes_or_no

def ts(sta,threshold):
    data_names = bd.get_data_names(sta)
    ob = sta[data_names[0]].values
    fo_num = len(data_names) - 1

    ts_list = []
    for i in range(fo_num):
        fo = sta[data_names[i+1]].values
        ts = yes_or_no.threshold_one.ts(ob,fo,threshold)
        ts_list.append(ts)
    if len(ts_list) == 1:
        ts_list = ts_list[0]
    return ts_list