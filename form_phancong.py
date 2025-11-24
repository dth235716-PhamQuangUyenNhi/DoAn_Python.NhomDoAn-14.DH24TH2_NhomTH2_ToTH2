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


def main(role):
  phancong = tk.Toplevel()
  phancong.title("Hệ thống quản lý giáo viên phổ thông")
  center_window(phancong, 700, 400)
  phancong.resizable(False, False)

   # Phân quyền
  is_admin = (role == "Admin")

  # Tiêu đề
  lbl_title = tk.Label(phancong, text="Lịch phân công", font=("Times New Roman", 18, "bold"))
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
          LP.MaLich,
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
    
    values = tree.item(selected)['values']
    xoa_stt = values[0]       
    xoa_malich = values[1]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM LICHPHANCONG WHERE STT = ? AND MaLich = ?", (xoa_stt,xoa_malich))  #xóa dựa trên STT và MaLich
    conn.commit()
    conn.close()

    tree.delete(selected)
    

  def thoat_action():
    phancong.destroy()
    form_trangchu.HomeForm(role)

  # ------------------- FORM THÊM PHÂN CÔNG MỚI ------------------
  def Mo_form_thempc():
    win_pc = tk.Toplevel(phancong)
    win_pc.title("Tạo phân công dạy học")
    center_window(win_pc, 500, 300)
    win_pc.resizable(False, False)

    #tiêu đề
    tk.Label(win_pc, text="Thêm lịch phân công mới", font=("Times New Roman", 18, "bold")).pack(pady=10)

    # Frame nhập thông tin
    frame_info = tk.Frame(win_pc)
    frame_info.pack(pady=10, padx=10, fill="x")

    tk.Label(frame_info, text="Mã Năm: ").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_malich = tk.Entry(frame_info, width=20)
    entry_malich.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Mã giáo viên: ").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_magv = tk.Entry(frame_info, width=25)
    entry_magv.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Tên lớp: ").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_tenlop = tk.Entry(frame_info, width=20)
    entry_tenlop.grid(row=1, column=1, padx=5, pady=5)

    # TÊN MÔN (COMBOBOX)
    tk.Label(frame_info, text="Môn học: ").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    combo_mon = ttk.Combobox(frame_info, width=22, state="readonly")
    combo_mon.grid(row=1, column=3, padx=5, pady=5)

    # Load danh sách môn học vào combobox
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT TenMon FROM MONHOC ORDER BY TenMon")
    monhoc_list = [row[0] for row in cursor.fetchall()]
    conn.close()

    combo_mon['values'] = monhoc_list

    frame_ghichu = tk.Frame(win_pc)
    frame_ghichu.pack(pady=10, padx=10, fill="x")

    tk.Label(frame_ghichu, text="Ghi chú: ").grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    text_ghichu = tk.Text(frame_ghichu, width=60, height=4)
    text_ghichu.grid(row=0, column=1, columnspan=4, padx=5, pady=5, sticky="we")

    # --------------------- HÀM CHỨC NĂNG TRONG FORM THÊM --------------------
    # Hàm lưu phân công mới
    def add_data():
      malich = entry_malich.get()
      magv = entry_magv.get()
      tenlop = entry_tenlop.get().strip()
      tenmon = combo_mon.get().strip()
      ghichu = text_ghichu.get("1.0", tk.END).strip()

      # Kiểm tra dữ liệu có đầy đủ không
      if not malich or not magv or not tenlop or not tenmon:
          messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
          return

      conn = get_connection()
      cursor = conn.cursor()

      # Lấy MaLop từ TenLop
      cursor.execute("SELECT MaLop FROM LOP WHERE TenLop=?", (tenlop,))
      row_lop = cursor.fetchone()
      if not row_lop:
        messagebox.showerror("Lỗi", f"Không tìm thấy lớp '{tenlop}' trong database!")
        return
      malop = row_lop[0]

      # Lấy MaMon từ TenMon (combobox)
      cursor.execute("SELECT MaMon FROM MONHOC WHERE TenMon=?", (tenmon,))
      row_mon = cursor.fetchone()
      if not row_mon:
        messagebox.showerror("Lỗi", f"Không tìm thấy môn '{tenmon}' trong database!")
        return
      mamon = row_mon[0]

      # Lưu dữ liệu
      try:
        cursor.execute("""
        INSERT INTO LICHPHANCONG (MaLich, MaGV, MaMon, MaLop, Ghichu)
        VALUES (?, ?, ?, ?, ?)
        """, (malich, magv, mamon, malop, ghichu))

        conn.commit()
        messagebox.showinfo("Thành công", "Đã thêm phân công mới!")
        load_data(tree)

        win_pc.destroy()

      except Exception as e:
        messagebox.showerror("Lỗi", str(e))

      conn.close()

    # Nut Lưu và quay lại
    frame_buttons = tk.Frame(win_pc)
    frame_buttons.pack(anchor='se', pady=10, padx=10)

    btn_them = tk.Button(frame_buttons, text="Lưu", width=10, command=add_data)
    btn_them.pack(side='left', padx=5)
    btn_thoat = tk.Button(frame_buttons, text="Quay lại", width=10, command=win_pc.destroy)
    btn_thoat.pack(side='left', padx=5)
  # --------------------- KẾT THÚC FORM THÊM PHÂN CÔNG MỚI ---------------------

  # -------------------- DANH SÁCH GIÁO VIÊN ---------------------------
  # Bảng danh sách giáo viên
  lbl_ds = tk.Label(phancong, text="Danh sách phân công dạy học", font=("Times New Roman", 10))
  lbl_ds.pack(pady=5, anchor="w", padx=10)

  # chọn năm học để hiển thị dữ liệu
  def chon_nam(nam):
    lbl_ds.config(text=f"Danh sách phân công dạy học năm {nam}-{nam+1}")
    load_data(tree, nam)
        
  for year in years:
    year_menu.add_command(label=str(year), command=lambda y=year: chon_nam(y))


  columns = ("STT", "MaLich", "Mã GV", "Họ tên GV", "Lớp", "Môn học", "Sỉ số", "Ghi chú")
  tree = ttk.Treeview(phancong, columns=columns, show="headings", height=10)

  for col in columns:
    tree.heading(col, text="" if col=="MaLich" else col)

  tree.column("STT", width=50, anchor="center")
  tree.column("MaLich", width=0, stretch=False)  # ẩn cột Mã Lịch
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
  btn_xoa = tk.Button(frame_buttons, text="Xóa", width=10, command=delete_data)
  btn_thoat = tk.Button(frame_buttons, text="Thoát", width=10, command=thoat_action)
  
  if is_admin:  
    btn_them.pack(side='left', padx=5)
    btn_xoa.pack(side='left', padx=5)
  btn_thoat.pack(side='left', padx=5)

  phancong.mainloop()

if __name__ == "__main__":
  main()