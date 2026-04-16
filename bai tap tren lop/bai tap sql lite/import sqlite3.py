import sqlite3
import os

# --- KẾT NỐI VÀ KHỞI TẠO DATABASE ---
def init_db():
    # Lấy đường dẫn thư mục chứa file script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'nhansu.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nhan_su (
            cccd TEXT PRIMARY KEY,
            ho_ten TEXT NOT NULL,
            ngay_sinh TEXT,
            gioi_tinh TEXT,
            dia_chi TEXT
        )
    ''')
    conn.commit()
    return conn

# --- CÁC CHỨC NĂNG CHÍNH ---

def them_nhan_su(conn):
    print("\n--- THÊM MỚI NHÂN SỰ ---")
    cccd = input("Nhập số CCCD: ")
    ten = input("Nhập họ và tên: ")
    ngay_sinh = input("Nhập ngày sinh (dd/mm/yyyy): ")
    gioi_tinh = input("Nhập giới tính: ")
    dia_chi = input("Nhập địa chỉ thường trú: ")
    
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO nhan_su VALUES (?, ?, ?, ?, ?)", 
                       (cccd, ten, ngay_sinh, gioi_tinh, dia_chi))
        conn.commit()
        print("Thêm thành công!")
    except sqlite3.IntegrityError:
        print("Lỗi: Số CCCD này đã tồn tại trong hệ thống.")

def xem_danh_sach(conn):
    print("\n--- DANH SÁCH NHÂN SỰ ---")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nhan_su")
    rows = cursor.fetchall()
    
    if not rows:
        print("Danh sách trống.")
    else:
        for row in rows:
            print(f"CCCD: {row[0]} | Tên: {row[1]} | NS: {row[2]} | GT: {row[3]} | ĐC: {row[4]}")

def sua_nhan_su(conn):
    cccd = input("\nNhập số CCCD của nhân sự cần sửa: ")
    ten = input("Họ tên mới: ")
    dia_chi = input("Địa chỉ mới: ")
    
    cursor = conn.cursor()
    cursor.execute("UPDATE nhan_su SET ho_ten = ?, dia_chi = ? WHERE cccd = ?", (ten, dia_chi, cccd))
    conn.commit()
    if cursor.rowcount > 0:
        print("Cập nhật thành công!")
    else:
        print("Không tìm thấy nhân sự có số CCCD này.")

def xoa_nhan_su(conn):
    cccd = input("\nNhập số CCCD của nhân sự cần xóa: ")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM nhan_su WHERE cccd = ?", (cccd,))
    conn.commit()
    if cursor.rowcount > 0:
        print("Đã xóa nhân sự.")
    else:
        print("Không tìm thấy nhân sự.")

def tim_kiem(conn):
    print("\n--- TÌM KIẾM NHÂN SỰ ---")
    keyword = input("Nhập nội dung cần tìm (CCCD, Tên hoặc Địa chỉ): ")
    cursor = conn.cursor()
    # Tìm kiếm gần đúng sử dụng LIKE
    query = "SELECT * FROM nhan_su WHERE cccd LIKE ? OR ho_ten LIKE ? OR dia_chi LIKE ?"
    val = f"%{keyword}%"
    cursor.execute(query, (val, val, val))
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)

# --- MENU ĐIỀU KHIỂN ---
def main():
    conn = init_db()
    while True:
        print("\n--- QUẢN LÝ NHÂN SỰ ---")
        print("1. Thêm nhân sự")
        print("2. Xem danh sách")
        print("3. Sửa thông tin")
        print("4. Xóa nhân sự")
        print("5. Tìm kiếm")
        print("6. Thoát")
        
        choice = input("Chọn chức năng (1-6): ")
        
        if choice == '1': them_nhan_su(conn)
        elif choice == '2': xem_danh_sach(conn)
        elif choice == '3': sua_nhan_su(conn)
        elif choice == '4': xoa_nhan_su(conn)
        elif choice == '5': tim_kiem(conn)
        elif choice == '6': break
        else: print("Lựa chọn không hợp lệ!")
    
    conn.close()

if __name__ == "__main__":
    main()