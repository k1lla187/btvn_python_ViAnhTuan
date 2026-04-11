from math_utils import phanso, hinhhoc

def main():
    print("--- PHÂN SỐ ---")
    ts1, ms1 = 1, 2
    ts2, ms2 = 1, 3
    
    print(f"Phân số 1: {ts1}/{ms1}")
    print(f"Phân số 2: {ts2}/{ms2}")
    
    kq_cong = phanso.cong(ts1, ms1, ts2, ms2)
    print(f"Cộng: {kq_cong[0]}/{kq_cong[1]}")
    
    kq_tru = phanso.tru(ts1, ms1, ts2, ms2)
    print(f"Trừ: {kq_tru[0]}/{kq_tru[1]}")
    
    kq_nhan = phanso.nhan(ts1, ms1, ts2, ms2)
    print(f"Nhân: {kq_nhan[0]}/{kq_nhan[1]}")
    
    kq_chia = phanso.chia(ts1, ms1, ts2, ms2)
    print(f"Chia: {kq_chia[0]}/{kq_chia[1]}")
    
    print("\n--- HÌNH HỌC ---")
    r = 5
    dai, rong = 4, 6
    
    print(f"Hình tròn có bán kính: {r}")
    print(f"Chu vi tròn: {hinhhoc.chu_vi_tron(r):.2f}")
    print(f"Diện tích tròn: {hinhhoc.dien_tich_tron(r):.2f}")
    
    print(f"\nHình chữ nhật có cạnh {dai} x {rong}")
    print(f"Chu vi chữ nhật: {hinhhoc.chu_vi_chu_nhat(dai, rong)}")
    print(f"Diện tích chữ nhật: {hinhhoc.dien_tich_chu_nhat(dai, rong)}")

if __name__ == "__main__":
    main()
