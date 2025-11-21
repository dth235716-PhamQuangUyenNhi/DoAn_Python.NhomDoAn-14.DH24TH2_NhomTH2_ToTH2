import tkinter as tk
from tkinter import ttk, messagebox
import form_trangchu
import pyodbc

def get_connection():
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=.\\SQLEXPRESS;"
            "DATABASE=QLGVTP;"
            "Trusted_Connection=yes;"
        )
        return conn


def center_window(win, w=700, h=400):
  ws = win.winfo_screenwidth()
  hs = win.winfo_screenheight()
  x = (ws // 2) - (w // 2)
  y = (hs // 2) - (h // 2)
  win.geometry(f'{w}x{h}+{x}+{y}')


def main():
  phancong = tk.Tk()
  phancong.title("Quản lý giáo viên phổ thông")
  center_window(phancong, 700, 400)
  phancong.resizable(False, False)

  # Tiêu đề
  lbl_title = tk.Label(phancong, text="Lịch phân công", font=("Arial", 18, "bold"))
  lbl_title.pack(pady=10)

    # MENU BAR (dạng VS Code)
  menubar = tk.Menu(phancong)
  phancong.config(menu=menubar)

    # Menu Năm học
  year_menu = tk.Menu(menubar, tearoff=0)
  menubar.add_cascade(label="Năm học", menu=year_menu)

  # Lấy danh sách các năm học từ database
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT DISTINCT NamHoc FROM LICHPHANCONG ORDER BY NamHoc")
  years = [row[0] for row in cursor.fetchall()]
  conn.close()
 

  # --------------------- CÁC HÀM CHỨC NĂNG ---------------------
  # --------------------- HIỂN THỊ DỮ LIỆU ---------------------
  def load_data(tree, nam=None):
    tree.delete(*tree.get_children())
    conn = get_connection()
    if conn:
        cur = conn.cursor()

        query = """
            SELECT 
                LP.STT,
                LP.MaGV,
                GV.HovaTendem + ' ' + GV.Ten AS HoTenGV,
                L.TenLop,
                TBM.TenTo AS BoMon,
                L.Siso AS Siso,
                LP.Ghichu
            FROM LICHPHANCONG LP
            INNER JOIN GIAOVIEN GV ON LP.MaGV = GV.MaGV
            INNER JOIN LOP L ON LP.MaLop = L.MaLop
            INNER JOIN TOBOMON TBM ON GV.MaGV = TBM.MaToTruong
        """
        params = []
        if nam is not None:
            query += " WHERE LP.NamHoc = ?"
            params.append(nam)
        query += " ORDER BY LP.NamHoc, L.TenLop;"
        cur.execute(query, params)
        
        for row in cur.fetchall():
            tree.insert("", tk.END, values=tuple(row)) 
        conn.close()

  # ---------------- HÀM XÓA ----------------
  def delete_data():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chọn dòng", "Hãy chọn một dòng để xóa!")
        return
    
    xoa_lpc = tree.item(selected)['values'][0]


    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM LICHPHANCONG WHERE STT = ?", (xoa_lpc,))  #chỉnh lại cái này, xóa theo năm nhưng giữ nguyên mã lịch
    conn.commit()
    conn.close()

    tree.delete(selected)
    

  # Hàm thoát về form_trangchu
  def thoat_action():
        phancong.destroy()  # đóng cửa sổ hiện tại
        form_trangchu.main()

  # ------------------- FORM THÊM PHÂN CÔNG MỚI ------------------
  def Mo_form_thempc():
    win_pc = tk.Toplevel(phancong)
    win_pc.title("Tạo phân công dạy học")
    center_window(win_pc, 500, 300)
    win_pc.resizable(False, False)

    #tiêu đề
    lbl_pcmoi= tk.Label(win_pc, text="Thêm lịch phân công mới", font=("Arial", 18, "bold")).pack(pady=10)

    # Frame nhập thông tin
    frame_info = tk.Frame(win_pc)
    frame_info.pack(pady=10, padx=10, fill="x")

    tk.Label(frame_info, text="Mã Năm: ").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_malich = tk.Entry(frame_info, width=20)
    entry_malich.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="mã giáo viên: ").grid(row=0, column=3, padx=5, pady=5, sticky="w")
    entry_magv = tk.Entry(frame_info, width=25)
    entry_magv.grid(row=0, column=4, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Mã lớp: ").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_mal = tk.Entry(frame_info, width=20)
    entry_mal.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Mã môn: ").grid(row=1, column=3, padx=5, pady=5, sticky="w")
    entry_mamon = tk.Entry(frame_info, width=25)
    entry_mamon.grid(row=1, column=4, padx=5, pady=5, sticky="w")

    frame_ghichu = tk.Frame(win_pc)
    frame_ghichu.pack(pady=10, padx=10, fill="x")

    tk.Label(frame_ghichu, text="Ghi chú: ").grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    text_ghichu = tk.Text(frame_ghichu, width=60, height=4)
    text_ghichu.grid(row=0, column=1, columnspan=4, padx=5, pady=5, sticky="we")

    # --------------------- HÀM CHỨC NĂNG TRONG FORM THÊM --------------------
    # Làm mới các trường nhập liệu
    def clear_action():
        entry_malich.delete(0, tk.END)
        entry_magv.delete(0, tk.END)
        entry_mal.delete(0, tk.END)
        entry_mamon.delete(0, tk.END)
        text_ghichu.delete("1.0", tk.END)

    # Hàm lưu phân công mới
    def add_data():
        malich = entry_malich.get()
        magv = entry_magv.get()
        malop = entry_mal.get()
        mamon = entry_mamon.get()
        ghichu = text_ghichu.get("1.0", tk.END).strip()

        # Kiểm tra dữ liệu có đầy đủ không
        if not malich or not magv or not malop or not mamon:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
            return

        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                # Thêm dữ liệu vào database
                cursor.execute("""
                    INSERT INTO LICHPHANCONG (MaLich, MaGV, MaMon, MaLop, Ghichu)
                    VALUES (?, ?, ?, ?, ?)
                    """, (malich, magv, mamon, malop, ghichu))
                conn.commit()
                conn.close()

                # Xóa Entry sau khi thêm
                clear_action()

                # Hiển thị thông báo thành công
                messagebox.showinfo("Thành công", "Đã thêm dữ liệu phân công mới thành công!")

            except Exception as e:
                messagebox.showerror("Lỗi", str(e))


    # Nut Lưu và quay lại
    frame_buttons = tk.Frame(win_pc)
    frame_buttons.pack(anchor='se', pady=10, padx=10)

    btn_them = tk.Button(frame_buttons, text="Lưu", width=10, command=add_data)
    btn_them.pack(side='left', padx=5)
    btn_thoat = tk.Button(frame_buttons, text="Quay lại", width=10, command=win_pc.destroy)
    btn_thoat.pack(side='left', padx=5)


  # -------------------- DANH SÁCH GIÁO VIÊN ---------------------------
  # Bảng danh sách giáo viên
  lbl_ds = tk.Label(phancong, text="Danh sách phân công dạy học", font=("Arial", 10))
  lbl_ds.pack(pady=5, anchor="w", padx=10)

  # chọn năm học để hiển thị dữ liệu
  def chon_nam(nam):
        lbl_ds.config(text=f"Danh sách phân công dạy học năm {nam}-{nam+1}")
        load_data(tree, nam)
        
  for year in years:
    year_menu.add_command(label=str(year), command=lambda y=year: chon_nam(y))


  columns = ("STT", "Mã GV", "Họ tên GV", "Lớp", "Môn học", "Sỉ số", "Ghi chú")
  tree = ttk.Treeview(phancong, columns=columns, show="headings", height=10)

  for col in columns:
    tree.heading(col, text=col.capitalize())

  tree.column("STT", width=50, anchor="center")
  tree.column("Mã GV", width=60, anchor="center")
  tree.column("Họ tên GV", width=100, anchor="center")
  tree.column("Lớp", width=50, anchor="center")
  tree.column("Môn học", width=70, anchor="center")
  tree.column("Sỉ số", width=50, anchor="center")
  tree.column("Ghi chú", width=200, anchor="center")

  tree.pack(padx=10, pady=5, fill="both")
  

  # --------------------- NÚT Ở PORM CHÍNH ---------------------
  # Frame chứa nút ở góc dưới bên phải
  frame_buttons = tk.Frame(phancong)
  frame_buttons.pack(anchor='se', pady=10, padx=10)

  btn_them = tk.Button(frame_buttons, text="Thêm", width=10, command=Mo_form_thempc)
  btn_them.pack(side='left', padx=5)
  btn_them = tk.Button(frame_buttons, text="Xóa", width=10, command=delete_data)
  btn_them.pack(side='left', padx=5)
  btn_thoat = tk.Button(frame_buttons, text="Thoát", width=10, command=thoat_action)
  btn_thoat.pack(side='left', padx=5)


  phancong.mainloop()

if __name__ == "__main__":
  main()