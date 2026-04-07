import time

print("--- Bài 1: Chẵn/Lẻ ---")
n = int(input("Nhập số: "))
print("Đây là một số chẵn" if n % 2 == 0 else "Đây là một số lẻ")

print("\n--- Bài 2: Kiểm tra tam giác ---")
a = int(input("Cạnh a: "))
b = int(input("Cạnh b: "))
c = int(input("Cạnh c: "))
if (a + b > c) and (a + c > b) and (b + c > a):
    print("Độ dài ba cạnh tam giác")
else:
    print("Đây không phải độ dài ba cạnh tam giác")

print("\n--- Bài 3: Tính tuổi ---")
x = time.localtime()
current_year = x[0]
yob = int(input("Nhập năm sinh: "))
print(f"Năm sinh {yob}, vậy bạn {current_year - yob} tuổi.")
