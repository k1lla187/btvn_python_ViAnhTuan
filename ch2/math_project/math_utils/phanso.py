import math

def rut_gon(tu_so, mau_so):
    """Rút gọn phân số."""
    if mau_so == 0:
        raise ValueError("Mẫu số không thể bằng 0.")
    ucln = math.gcd(tu_so, mau_so)
    return tu_so // ucln, mau_so // ucln

def cong(ts1, ms1, ts2, ms2):
    """Cộng hai phân số: ts1/ms1 + ts2/ms2"""
    ts_moi = ts1 * ms2 + ts2 * ms1
    ms_moi = ms1 * ms2
    return rut_gon(ts_moi, ms_moi)

def tru(ts1, ms1, ts2, ms2):
    """Trừ hai phân số: ts1/ms1 - ts2/ms2"""
    ts_moi = ts1 * ms2 - ts2 * ms1
    ms_moi = ms1 * ms2
    return rut_gon(ts_moi, ms_moi)

def nhan(ts1, ms1, ts2, ms2):
    """Nhân hai phân số: (ts1/ms1) * (ts2/ms2)"""
    ts_moi = ts1 * ts2
    ms_moi = ms1 * ms2
    return rut_gon(ts_moi, ms_moi)

def chia(ts1, ms1, ts2, ms2):
    """Chia hai phân số: (ts1/ms1) / (ts2/ms2)"""
    if ts2 == 0:
        raise ValueError("Không thể chia cho phân số có tử số bằng 0.")
    ts_moi = ts1 * ms2
    ms_moi = ms1 * ts2
    return rut_gon(ts_moi, ms_moi)
