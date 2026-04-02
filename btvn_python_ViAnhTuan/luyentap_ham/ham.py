import math

# 1. Viết hàm tính tổng 2 số truyền vào
def tinh_tong_hai_so(a, b):
    return a + b

# 2. Viết hàm tính tổng các số truyền vào (Sử dụng *args để nhận số lượng số bất kỳ)
def tinh_tong_nhieu_so(*args):
    return sum(args)

# 3. Viết hàm kiểm tra một số nguyên tố
def la_so_nguyen_to(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# 4. Viết chương trình tìm các số nguyên tố trong khoảng [a, b]
def tim_snt_trong_khoang(a, b):
    ket_qua = [i for i in range(a, b + 1) if la_so_nguyen_to(i)]
    return ket_qua

# 5. Viết hàm kiểm tra số hoàn hảo
# Số hoàn hảo là số có tổng các ước thực sự (không kể chính nó) bằng chính nó.
def la_so_hoan_hao(n):
    if n < 1:
        return False
    tong_uoc = sum([i for i in range(1, n) if n % i == 0])
    return tong_uoc == n

# 6. Viết chương trình tìm các số hoàn hảo trong khoảng [a, b]
def tim_shh_trong_khoang(a, b):
    ket_qua = [i for i in range(a, b + 1) if la_so_hoan_hao(i)]
    return ket_qua

# => Viết chương trình menu chọn thực thi các hàm ở trên
def hien_thi_menu():
    while True:
        print("\n--- MENU LUYỆN TẬP PYTHON ---")
        print("1. Tính tổng 2 số")
        print("2. Tính tổng các số truyền vào")
        print("3. Kiểm tra số nguyên tố")
        print("4. Tìm số nguyên tố trong khoảng [a, b]")
        print("5. Kiểm tra số hoàn hảo")
        print("6. Tìm số hoàn hảo trong khoảng [a, b]")
        print("0. Thoát")
        
        chon = input("Mời bạn chọn (0-6): ")
        
        if chon == '1':
            x = float(input("Nhập số thứ nhất: "))
            y = float(input("Nhập số thứ hai: "))
            print(f"Tổng là: {tinh_tong_hai_so(x, y)}")
            
        elif chon == '2':
            ds = input("Nhập các số cách nhau bởi dấu cách: ").split()
            ds_so = [float(x) for x in ds]
            print(f"Tổng dãy số là: {tinh_tong_nhieu_so(*ds_so)}")
            
        elif chon == '3':
            n = int(input("Nhập số cần kiểm tra: "))
            if la_so_nguyen_to(n):
                print(f"{n} là số nguyên tố.")
            else:
                print(f"{n} không phải là số nguyên tố.")
                
        elif chon == '4':
            a = int(input("Nhập a: "))
            b = int(input("Nhập b: "))
            print(f"Các SNT trong khoảng [{a}, {b}] là: {tim_snt_trong_khoang(a, b)}")
            
        elif chon == '5':
            n = int(input("Nhập số cần kiểm tra: "))
            if la_so_hoan_hao(n):
                print(f"{n} là số hoàn hảo.")
            else:
                print(f"{n} không phải là số hoàn hảo.")
                
        elif chon == '6':
            a = int(input("Nhập a: "))
            b = int(input("Nhập b: "))
            print(f"Các số hoàn hảo trong khoảng [{a}, {b}] là: {tim_shh_trong_khoang(a, b)}")
            
        elif chon == '0':
            print("Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng thử lại.")

# Chạy chương trình
if __name__ == "__main__":
    hien_thi_menu()