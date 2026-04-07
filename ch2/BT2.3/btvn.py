# CHƯƠNG TRÌNH TỔNG HỢP GIẢI BÀI TẬP 2.3

# --- Bài 1: Tính tổng hai số nguyên ---
print("--- Bài 1 ---")
a1 = int(input("Nhập số nguyên thứ nhất: "))
b1 = int(input("Nhập số nguyên thứ hai: "))
print(f"Tổng của {a1} và {b1} là: {a1 + b1}\n")

# --- Bài 2: Nhập và in chuỗi ký tự ---
print("--- Bài 2 ---")
chuoi2 = input("Nhập vào một chuỗi ký tự bất kỳ: ")
print(f"Chuỗi bạn vừa nhập là: {chuoi2}\n")

# --- Bài 3: Tính toán với ba số nguyên ---
print("--- Bài 3 ---")
a3 = int(input("Nhập số nguyên thứ nhất: "))
b3 = int(input("Nhập số nguyên thứ hai: "))
c3 = int(input("Nhập số nguyên thứ ba: "))

# a) Tổng và tích
print(f"a) Tổng: {a3 + b3 + c3}, Tích: {a3 * b3 * c3}")

# b) Hiệu của 2 số bất kỳ (ví dụ a3 và b3)
print(f"b) Hiệu của {a3} và {b3} là: {a3 - b3}")

# c) Chia lấy phần nguyên, phần dư và chính xác (ví dụ a3 và b3)
if b3 != 0:
    print(f"c) {a3} chia {b3}: Nguyên = {a3 // b3}, Dư = {a3 % b3}, Chính xác = {a3 / b3}\n")
else:
    print("c) Không thể thực hiện phép chia vì số thứ hai bằng 0\n")

# --- Bài 4: Ghép ba chuỗi ký tự ---
print("--- Bài 4 ---")
s1 = input("Nhập chuỗi 1 (Họ): ")
s2 = input("Nhập chuỗi 2 (Tên đệm): ")
s3 = input("Nhập chuỗi 3 (Tên): ")
# Ghép các chuỗi lại, cách nhau bởi khoảng trắng
ho_ten = s1 + " " + s2 + " " + s3
print(f"Kết quả ghép chuỗi: '{ho_ten}'\n")

# --- Bài 5: Tính chu vi và diện tích hình tròn ---
print("--- Bài 5 ---")
R = float(input("Nhập bán kính hình tròn: "))
pi = 3.14
cv = 2 * R * pi
dt = pi * R * R
print(f"Chu vi hình tròn (CV): {cv}")
print(f"Diện tích hình tròn (DT): {dt}")

print("\n--- Hoàn thành tất cả bài tập ---")

