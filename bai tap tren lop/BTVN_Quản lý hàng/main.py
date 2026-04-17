import sqlite3
import os
import sys

# Đặt encoding cho stdout để hỗ trợ tiếng Việt trên Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')

# --- PHẦN 1: THIẾT LẬP DATABASE ---
def setup_database():
    # Đường dẫn database trong cùng thư mục với file main.py
    db_path = os.path.join(os.path.dirname(__file__), 'quan_ly_ban_hang.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Bật khóa ngoại
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute('''CREATE TABLE IF NOT EXISTS MatHang (
                        MaMH TEXT PRIMARY KEY, TenMH TEXT, NguonGoc TEXT, DonGia REAL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS KhachHang (
                        MaKH TEXT PRIMARY KEY, TenKH TEXT, DiaChi TEXT, SDT TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS DonHang (
                        MaDH TEXT PRIMARY KEY, MaKH TEXT,
                        FOREIGN KEY (MaKH) REFERENCES KhachHang(MaKH))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ChiTietDonHang (
                        MaDH TEXT, MaMH TEXT, SoLuong INTEGER,
                        PRIMARY KEY (MaDH, MaMH),
                        FOREIGN KEY (MaDH) REFERENCES DonHang(MaDH) ON DELETE CASCADE,
                        FOREIGN KEY (MaMH) REFERENCES MatHang(MaMH))''')
    conn.commit()
    conn.close()

# --- PHẦN 2: LỚP QUẢN LÝ TỔNG HỢP ---
class QuanLyBanHang:
    def __init__(self, db_name):
        self.db_name = db_name

    def execute_query(self, query, params=(), fetch=False):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            conn.commit()

    # --- CHỨC NĂNG MẶT HÀNG ---
    def ql_mathang(self, action, data=None):
        if action == "view":
            return self.execute_query("SELECT * FROM MatHang", fetch=True)
        elif action == "add":
            self.execute_query("INSERT INTO MatHang VALUES (?,?,?,?)", data)
        elif action == "edit":
            self.execute_query("UPDATE MatHang SET TenMH=?, NguonGoc=?, DonGia=? WHERE MaMH=?", data)
        elif action == "delete":
            self.execute_query("DELETE FROM MatHang WHERE MaMH=?", (data,))
        elif action == "search":
            return self.execute_query("SELECT * FROM MatHang WHERE MaMH LIKE ? OR TenMH LIKE ? OR NguonGoc LIKE ?",
                                     (f'%{data}%', f'%{data}%', f'%{data}%'), fetch=True)

    # --- CHỨC NĂNG KHÁCH HÀNG ---
    def ql_khachhang(self, action, data=None):
        if action == "view":
            return self.execute_query("SELECT * FROM KhachHang", fetch=True)
        elif action == "add":
            self.execute_query("INSERT INTO KhachHang VALUES (?,?,?,?)", data)
        elif action == "edit":
            self.execute_query("UPDATE KhachHang SET TenKH=?, DiaChi=?, SDT=? WHERE MaKH=?", data)
        elif action == "delete":
            self.execute_query("DELETE FROM KhachHang WHERE MaKH=?", (data,))
        elif action == "search":
            return self.execute_query("SELECT * FROM KhachHang WHERE MaKH LIKE ? OR TenKH LIKE ? OR DiaChi LIKE ? OR SDT LIKE ?",
                                     (f'%{data}%', f'%{data}%', f'%{data}%', f'%{data}%'), fetch=True)

    # --- CHỨC NĂNG ĐƠN HÀNG ---
    def list_don_hang(self):
        query = '''
            SELECT DH.MaDH, DH.MaKH, SUM(CT.SoLuong * MH.DonGia)
            FROM DonHang DH
            LEFT JOIN ChiTietDonHang CT ON DH.MaDH = CT.MaDH
            LEFT JOIN MatHang MH ON CT.MaMH = MH.MaMH
            GROUP BY DH.MaDH
        '''
        return self.execute_query(query, fetch=True)

    def xem_chi_tiet(self, ma_dh):
        query = '''
            SELECT MH.TenMH, CT.SoLuong, MH.DonGia, (CT.SoLuong * MH.DonGia)
            FROM ChiTietDonHang CT
            JOIN MatHang MH ON CT.MaMH = MH.MaMH
            WHERE CT.MaDH = ?
        '''
        return self.execute_query(query, (ma_dh,), fetch=True)

    def ql_donhang(self, action, data=None):
        if action == "view":
            return self.execute_query("SELECT * FROM DonHang", fetch=True)
        elif action == "add":
            self.execute_query("INSERT INTO DonHang VALUES (?,?)", data)
        elif action == "edit":
            self.execute_query("UPDATE DonHang SET MaKH=? WHERE MaDH=?", data)
        elif action == "delete":
            self.execute_query("DELETE FROM DonHang WHERE MaDH=?", (data,))
        elif action == "search_madh":
            return self.execute_query("SELECT * FROM DonHang WHERE MaDH LIKE ?", (f'%{data}%',), fetch=True)
        elif action == "search_makh":
            return self.execute_query("SELECT * FROM DonHang WHERE MaKH LIKE ?", (f'%{data}%',), fetch=True)
        elif action == "add_chitiet":
            self.execute_query("INSERT OR REPLACE INTO ChiTietDonHang VALUES (?,?,?)", data)
        elif action == "delete_chitiet":
            self.execute_query("DELETE FROM ChiTietDonHang WHERE MaDH=? AND MaMH=?", data)

# --- PHẦN 3: MENU ĐIỀU KHIỂN ---
def main():
    setup_database()
    db_path = os.path.join(os.path.dirname(__file__), 'quan_ly_ban_hang.db')
    ql = QuanLyBanHang(db_path)

    while True:
        print("\n" + "="*50)
        print("        HỆ THỐNG QUẢN LÝ BÁN HÀNG")
        print("="*50)
        print("1. Quản lý mặt hàng")
        print("2. Quản lý khách hàng")
        print("3. Quản lý đơn hàng")
        print("0. Thoát")
        print("="*50)

        chon = input("Chọn chức năng: ")

        # --- MENU MẶT HÀNG ---
        if chon == "1":
            while True:
                print("\n--- QUẢN LÝ MẶT HÀNG ---")
                print("1. Xem danh sách mặt hàng")
                print("2. Thêm mặt hàng mới")
                print("3. Sửa thông tin mặt hàng")
                print("4. Xóa mặt hàng")
                print("5. Tìm kiếm mặt hàng")
                print("0. Quay lại")
                c = input("Chọn: ")

                if c == "1":
                    items = ql.ql_mathang("view")
                    print(f"\n{'Mã MH':<10} | {'Tên MH':<20} | {'Nguồn gốc':<15} | {'Đơn giá':>10}")
                    print("-"*70)
                    for i in items:
                        print(f"{i[0]:<10} | {i[1]:<20} | {i[2]:<15} | {i[3]:>10,.2f}")

                elif c == "2":
                    print("\n--- THÊM MẶT HÀNG MỚI ---")
                    while True:
                        ma = input("Mã MH: ").strip()
                        if ma:
                            break
                        print("Mã MH không được để trống!")

                    while True:
                        ten = input("Tên MH: ").strip()
                        if ten:
                            break
                        print("Tên MH không được để trống!")

                    nguon = input("Nguồn gốc: ").strip()

                    while True:
                        gia_input = input("Đơn giá: ").strip()
                        if gia_input:
                            try:
                                gia = float(gia_input)
                                if gia >= 0:
                                    break
                                else:
                                    print("Đơn giá phải >= 0!")
                            except ValueError:
                                print("Vui lòng nhập số hợp lệ!")
                        else:
                            print("Đơn giá không được để trống!")

                    ql.ql_mathang("add", (ma, ten, nguon, gia))
                    print("Đã thêm mặt hàng!")

                elif c == "3":
                    print("\n--- SỬA THÔNG TIN MẶT HÀNG ---")
                    ma = input("Nhập mã MH cần sửa: ")
                    items = ql.ql_mathang("search", ma)
                    if items:
                        old_item = items[0]
                        print(f"Thông tin hiện tại: {old_item}")
                        ten = input(f"Tên MH mới [{old_item[1]}]: ").strip()
                        nguon = input(f"Nguồn gốc mới [{old_item[2]}]: ").strip()
                        gia_input = input(f"Đơn giá mới [{old_item[3]}]: ").strip()

                        # Giữ nguyên giá trị cũ nếu để trống
                        ten = ten if ten else old_item[1]
                        nguon = nguon if nguon else old_item[2]
                        gia = float(gia_input) if gia_input else old_item[3]

                        ql.ql_mathang("edit", (ten, nguon, gia, ma))
                        print("Đã cập nhật!")
                    else:
                        print("Không tìm thấy mặt hàng!")

                elif c == "4":
                    print("\n--- XÓA MẶT HÀNG ---")
                    ma = input("Nhập mã MH cần xóa: ")
                    ql.ql_mathang("delete", ma)
                    print("Đã xóa!")

                elif c == "5":
                    print("\n--- TÌM KIẾM MẶT HÀNG ---")
                    key = input("Nhập mã/tên/nguồn gốc: ")
                    results = ql.ql_mathang("search", key)
                    print(f"\n{'Mã MH':<10} | {'Tên MH':<20} | {'Nguồn gốc':<15} | {'Đơn giá':>10}")
                    print("-"*70)
                    for r in results:
                        print(f"{r[0]:<10} | {r[1]:<20} | {r[2]:<15} | {r[3]:>10,.2f}")

                elif c == "0":
                    break

        # --- MENU KHÁCH HÀNG ---
        elif chon == "2":
            while True:
                print("\n--- QUẢN LÝ KHÁCH HÀNG ---")
                print("1. Xem danh sách khách hàng")
                print("2. Thêm khách hàng mới")
                print("3. Sửa thông tin khách hàng")
                print("4. Xóa khách hàng")
                print("5. Tìm kiếm khách hàng")
                print("0. Quay lại")
                c = input("Chọn: ")

                if c == "1":
                    khs = ql.ql_khachhang("view")
                    print(f"\n{'Mã KH':<10} | {'Tên KH':<20} | {'Địa chỉ':<25} | {'SĐT':<12}")
                    print("-"*75)
                    for k in khs:
                        print(f"{k[0]:<10} | {k[1]:<20} | {k[2]:<25} | {k[3]:<12}")

                elif c == "2":
                    print("\n--- THÊM KHÁCH HÀNG MỚI ---")
                    while True:
                        ma = input("Mã KH: ").strip()
                        if ma:
                            break
                        print("Mã KH không được để trống!")

                    while True:
                        ten = input("Tên KH: ").strip()
                        if ten:
                            break
                        print("Tên KH không được để trống!")

                    diachi = input("Địa chỉ: ").strip()
                    sdt = input("SĐT: ").strip()

                    ql.ql_khachhang("add", (ma, ten, diachi, sdt))
                    print("Đã thêm khách hàng!")

                elif c == "3":
                    print("\n--- SỬA THÔNG TIN KHÁCH HÀNG ---")
                    ma = input("Nhập mã KH cần sửa: ")
                    khs = ql.ql_khachhang("search", ma)
                    if khs:
                        old_kh = khs[0]
                        print(f"Thông tin hiện tại: {old_kh}")
                        ten = input(f"Tên KH mới [{old_kh[1]}]: ").strip()
                        diachi = input(f"Địa chỉ mới [{old_kh[2]}]: ").strip()
                        sdt = input(f"SĐT mới [{old_kh[3]}]: ").strip()

                        ten = ten if ten else old_kh[1]
                        diachi = diachi if diachi else old_kh[2]
                        sdt = sdt if sdt else old_kh[3]

                        ql.ql_khachhang("edit", (ten, diachi, sdt, ma))
                        print("Đã cập nhật!")
                    else:
                        print("Không tìm thấy khách hàng!")

                elif c == "4":
                    print("\n--- XÓA KHÁCH HÀNG ---")
                    ma = input("Nhập mã KH cần xóa: ")
                    ql.ql_khachhang("delete", ma)
                    print("Đã xóa!")

                elif c == "5":
                    print("\n--- TÌM KIẾM KHÁCH HÀNG ---")
                    key = input("Nhập mã/tên/địa chỉ/SĐT: ")
                    results = ql.ql_khachhang("search", key)
                    print(f"\n{'Mã KH':<10} | {'Tên KH':<20} | {'Địa chỉ':<25} | {'SĐT':<12}")
                    print("-"*75)
                    for r in results:
                        print(f"{r[0]:<10} | {r[1]:<20} | {r[2]:<25} | {r[3]:<12}")

                elif c == "0":
                    break

        # --- MENU ĐƠN HÀNG ---
        elif chon == "3":
            while True:
                print("\n--- QUẢN LÝ ĐƠN HÀNG ---")
                print("1. Xem danh sách hóa đơn (có tổng tiền)")
                print("2. Thêm đơn hàng mới")
                print("3. Sửa đơn hàng")
                print("4. Xóa đơn hàng")
                print("5. Tìm kiếm đơn hàng theo mã đơn hàng")
                print("6. Tìm kiếm đơn hàng theo mã khách hàng")
                print("7. Xem chi tiết hóa đơn (nhấn vào mã DH)")
                print("0. Quay lại")
                c = input("Chọn: ")

                if c == "1":
                    orders = ql.list_don_hang()
                    print(f"\n{'Mã ĐH':<10} | {'Mã KH':<10} | {'Tổng tiền':>15}")
                    print("-"*40)
                    for o in orders:
                        print(f"{o[0]:<10} | {o[1]:<10} | {o[2] or 0:>15,.2f}")

                elif c == "2":
                    print("\n--- THÊM ĐƠN HÀNG MỚI ---")
                    while True:
                        ma_dh = input("Mã đơn hàng: ").strip()
                        if ma_dh:
                            break
                        print("Mã đơn hàng không được để trống!")

                    while True:
                        ma_kh = input("Mã khách hàng: ").strip()
                        if ma_kh:
                            break
                        print("Mã khách hàng không được để trống!")

                    ql.ql_donhang("add", (ma_dh, ma_kh))
                    print("Đã thêm đơn hàng!")

                    # Thêm chi tiết đơn hàng
                    them_ct = input("Thêm chi tiết đơn hàng? (y/n): ")
                    while them_ct.lower() == 'y':
                        ma_mh = input("Mã mặt hàng: ")
                        while True:
                            sl_input = input("Số lượng: ").strip()
                            if sl_input:
                                try:
                                    sl = int(sl_input)
                                    if sl > 0:
                                        break
                                    else:
                                        print("Số lượng phải lớn hơn 0!")
                                except ValueError:
                                    print("Vui lòng nhập số nguyên hợp lệ!")
                            else:
                                print("Số lượng không được để trống!")

                        ql.ql_donhang("add_chitiet", (ma_dh, ma_mh, sl))
                        print("Đã thêm chi tiết!")
                        them_ct = input("Tiếp tục thêm? (y/n): ")

                elif c == "3":
                    print("\n--- SỬA ĐƠN HÀNG ---")
                    ma_dh = input("Nhập mã đơn hàng cần sửa: ")
                    # Kiểm tra đơn hàng tồn tại
                    orders = ql.ql_donhang("view")
                    order_exists = any(o[0] == ma_dh for o in orders)
                    if order_exists:
                        # Chỉ có thể sửa mã khách hàng
                        ma_kh_input = input("Mã khách hàng mới [Enter để giữ nguyên]: ").strip()
                        if ma_kh_input:
                            ql.ql_donhang("edit", (ma_kh_input, ma_dh))
                            print("Đã cập nhật!")
                        else:
                            print("Không có thay đổi.")
                    else:
                        print("Không tìm thấy đơn hàng!")

                elif c == "4":
                    print("\n--- XÓA ĐƠN HÀNG ---")
                    ma_dh = input("Nhập mã đơn hàng cần xóa: ")
                    ql.ql_donhang("delete", ma_dh)
                    print("Đã xóa!")

                elif c == "5":
                    print("\n--- TÌM KIẾM THEO MÃ ĐƠN HÀNG ---")
                    key = input("Nhập mã đơn hàng: ")
                    results = ql.ql_donhang("search_madh", key)
                    print(f"\n{'Mã ĐH':<10} | {'Mã KH':<10}")
                    print("-"*25)
                    for r in results:
                        print(f"{r[0]:<10} | {r[1]:<10}")

                elif c == "6":
                    print("\n--- TÌM KIẾM THEO MÃ KHÁCH HÀNG ---")
                    key = input("Nhập mã khách hàng: ")
                    results = ql.ql_donhang("search_makh", key)
                    print(f"\n{'Mã ĐH':<10} | {'Mã KH':<10}")
                    print("-"*25)
                    for r in results:
                        print(f"{r[0]:<10} | {r[1]:<10}")

                elif c == "7":
                    print("\n--- XEM CHI TIẾT HÓA ĐƠN ---")
                    ma_dh = input("Nhập mã hóa đơn: ")
                    details = ql.xem_chi_tiet(ma_dh)
                    if details:
                        print(f"\nChi tiết đơn hàng {ma_dh}:")
                        print(f"{'Tên MH':<20} | {'Số lượng':>10} | {'Đơn giá':>12} | {'Thành tiền':>15}")
                        print("-"*65)
                        for d in details:
                            print(f"{d[0]:<20} | {d[1]:>10} | {d[2]:>12,.2f} | {d[3]:>15,.2f}")
                    else:
                        print("Không có chi tiết hoặc mã đơn hàng không tồn tại!")

                elif c == "0":
                    break

        elif chon == "0":
            print("Tạm biệt!")
            break

if __name__ == "__main__":
    main()
