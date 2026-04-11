import math

def chu_vi_tron(radius):
    """Tính chu vi hình tròn."""
    return 2 * math.pi * radius

def dien_tich_tron(radius):
    """Tính diện tích hình tròn."""
    return math.pi * (radius ** 2)

def chu_vi_chu_nhat(chieu_dai, chieu_rong):
    """Tính chu vi hình chữ nhật."""
    return 2 * (chieu_dai + chieu_rong)

def dien_tich_chu_nhat(chieu_dai, chieu_rong):
    """Tính diện tích hình chữ nhật."""
    return chieu_dai * chieu_rong
