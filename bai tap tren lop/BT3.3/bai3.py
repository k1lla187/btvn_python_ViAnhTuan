import time

# Lấy năm hiện tại từ hệ thống
x = time.localtime()
year_now = x[0]

# Nhập năm sinh
nam_sinh = int(input("Nhập vào năm sinh của bạn: "))

# Tính tuổi
tuoi = year_now - nam_sinh

# In kết quả theo mẫu
print(f"Năm sinh {nam_sinh}, vậy bạn {tuoi} tuổi.")
