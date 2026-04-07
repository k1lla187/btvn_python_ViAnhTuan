# --- Bài 3: Tính toán với ba số nguyên ---
print("--- Bài 3 ---")
a3 = int(input("Nhập số nguyên thứ nhất: "))
b3 = int(input("Nhập số nguyên thứ hai: "))
c3 = int(input("Nhập số nguyên thứ ba: "))

# a) Tổng và tích
print(f"a) Tổng: {a3 + b3 + c3}, Tích: {a3 * b3 * c3}")

# b) Hiệu
print(f"b) Hiệu của {a3} và {b3} là: {a3 - b3}")

# c) Chia
if b3 != 0:
    print(f"c) {a3} chia {b3}: Nguyên = {a3 // b3}, Dư = {a3 % b3}, Chính xác = {a3 / b3}")
else:
    print("c) Không thể chia cho 0")