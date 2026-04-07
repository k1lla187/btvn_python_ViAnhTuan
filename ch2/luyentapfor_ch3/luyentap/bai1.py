n = int(input("Nhập số nguyên n: "))
for i in range(1, n):
    print(f"{2 * i}", end=", " if i < n - 1 else "")
# Ví dụ n=4: In ra 2, 4, 6
