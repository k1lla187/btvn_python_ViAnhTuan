n = int(input("Nhập số nguyên dương n: "))

if n < 2:
    print("Không phải số nguyên tố")
else:
    check = True
    i = 2
    while i <= n**0.5: # Kiểm tra đến căn bậc hai của n để tối ưu
        if n % i == 0:
            check = False
            break
        i += 1
    
    if check:
        print("Đây là số nguyên tố")
    else:
        print("Không phải số nguyên tố")
