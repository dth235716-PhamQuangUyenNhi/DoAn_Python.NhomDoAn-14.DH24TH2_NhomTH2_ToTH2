import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import form_trangchu
import pyodbc

# --------------------------- KẾT NỐI SQL SERVER ---------------------------
def get_connection():
  conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=.\\SQLEXPRESS;"
    "DATABASE=QLGVTP;"
    "Trusted_Connection=yes;"
  )
  return conn

def center_window(win, w=700, h=500):
  ws = win.winfo_screenwidth()
  hs = win.winfo_screenheight()
  x = (ws // 2) - (w // 2)
  y = (hs // 2) - (h // 2)
  win.geometry(f'{w}x{h}+{x}+{y}')

# --------------------------- GIAO DIỆN CHÍNH ---------------------------
def main(role):
  timkiem = tk.Toplevel()
  timkiem.title("Đăng nhập hệ thống")
  center_window(timkiem, 300, 200)
  timkiem.resizable(False, False)

  # ======= Giao diện đăng nhập =======
  lbl_title = tk.Label(timkiem, text="Tìm kiếm giáo viên", font=("Times New Roman", 14, "bold"))
  lbl_title.pack(pady=10)

  frm_input = tk.Frame(timkiem)
  frm_input.pack(pady=5)

  # Ô nhập tài khoản
  tk.Label(frm_input, text="Mã số giáo viên:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
  txt_tkgv = tk.Entry(frm_input, width=25)
  txt_tkgv.grid(row=0, column=1, padx=5, pady=5)


  # ---------------------- HÀM TÌM KIẾM MÃ GIÁO VIÊN ------------------------ 
  def timmagv():
    magv = txt_tkgv.get().strip()

    if magv == "":
        messagebox.showwarning("Thông báo", "Vui lòng nhập mã giáo viên!")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT MaGV FROM GiaoVien WHERE MaGV = ?", magv)
        check = cursor.fetchone()

        if not check:
            messagebox.showerror("Thông báo", "Không tìm thấy giáo viên có mã này!")
            return
        Moform(magv)

    except Exception as e:
        messagebox.showerror("Lỗi SQL", str(e))

  # ----------------- MỞ FORM THÔNG TIN GIÁO VIÊN CẦN TÌM -----------------
  def Moform(magv):
    ttgv = tk.Toplevel()
    ttgv.title("Hệ thống quản lý giáo viên phổ thông")
    center_window(ttgv, 800, 700)
    ttgv.resizable(False, False)

    # ---- Hàm thoát ----
    # Hàm thoát về form_trangchu
    def vehoptk():
      ttgv.destroy()

    menubar = tk.Menu(ttgv)
    ttgv.config(menu=menubar)

    menu_tacvu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Tác vụ", menu=menu_tacvu)

    menu_tacvu.add_command(label="Thoát", command=vehoptk)

    # --------------------- CÁC HÀM CHỨC NĂNG ---------------------
    # ------------------ LOAD ẢNH --------------------------------
    def upload_image():
        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
        )
        if path:
            img = Image.open(path)
            img = img.resize((130, 160))  # chuẩn 4x6 gần đúng
            photo = ImageTk.PhotoImage(img)
            image_label.config(image=photo)
            image_label.image = photo  # tránh bị garbage collect

    # -------------------------- LOAD DỮ LIỆU --------------------------
    def load_data():
      try:
        magv = txt_tkgv.get().strip()  # Lấy mã giáo viên đúng entry
        conn = get_connection()

        # --- HIỂN THỊ THÔNG TIN CÁ NHÂN ---
        if magv == "":
            messagebox.showwarning("Thông báo", "Vui lòng nhập mã giáo viên!")
            return
        cursor = conn.cursor()

        cursor.execute("""
          SELECT
          (HovaTendem + ' ' + Ten) AS HoTen,
          Phai,
          NgaySinh,
          DiaChi,
          CCCD,
          SDT,
          DanToc,
          TonGiao
          FROM GIAOVIEN
          WHERE MaGV = ?
          """, magv)
        gv = cursor.fetchone()

        if not gv:
            messagebox.showerror("Lỗi", "Không tìm thấy giáo viên!")
            return

        entry_hoten.delete(0, tk.END)
        entry_hoten.insert(0, gv.HoTen)

        gender_var.set(gv.Phai)

        entry_Ngaysinh.delete(0, tk.END)
        entry_Ngaysinh.insert(0, gv.NgaySinh)

        entry_Diachi.delete(0, tk.END)
        entry_Diachi.insert(0, gv.DiaChi)

        entry_CCCD.delete(0, tk.END)
        entry_CCCD.insert(0, gv.CCCD)

        entry_SDT.delete(0, tk.END)
        entry_SDT.insert(0, gv.SDT)

        entry_Dantoc.delete(0, tk.END)
        entry_Dantoc.insert(0, gv.DanToc)

        entry_Tongiao.delete(0, tk.END)
        entry_Tongiao.insert(0, gv.TonGiao)

       # --- THÔNG TIN CHUYÊN MÔN ---
        cursor.execute("""
          SELECT 
            gv.HovaTendem + ' ' + gv.Ten AS HoTenGV,
            gv.TrangThai,
            gv.TrinhDo,
            mh.TenMon,
            N'Sư phạm ' + mh.TenMon AS ChuyenNganh,
            tb.TenTo AS ToBoMon,
            (gvtt.HovaTendem + ' ' + gvtt.Ten) AS TenToTruong
          FROM GIAOVIEN gv
          LEFT JOIN MONHOC mh ON gv.MaMon = mh.MaMon
          LEFT JOIN TOBOMON tb ON tb.MaToTruong = gv.MaGV  -- Nếu muốn lấy tổ mà GV làm tổ trưởng
          LEFT JOIN GIAOVIEN gvtt ON tb.MaToTruong = gvtt.MaGV
          WHERE GV.MaGV = ?;
          """, magv)
        cm = cursor.fetchone()

        if cm:
          trangthai_var.set(cm.TrangThai)

          entry_tento.delete(0, tk.END)
          entry_tento.insert(0, cm.ToBoMon)

          entry_totruong.delete(0, tk.END)
          entry_totruong.insert(0, cm.TenToTruong)

          entry_chuyennganh.delete(0, tk.END)
          entry_chuyennganh.insert(0, cm.ChuyenNganh)

          entry_trinhdo.delete(0, tk.END)
          entry_trinhdo.insert(0, cm.TrinhDo)

        # --- LỊCH PHÂN CÔNG ---
        cursor.execute("""
          SELECT 
            L.MaLop,
            L.TenLop,
            L.SiSo,
            M.TenMon,
            LPC.NamHoc,
            CASE WHEN L.MaGVCN = ? THEN N'Có' ELSE N'Không' END AS ChuNhiem,
            LPC.GhiChu
          FROM LICHPHANCONG LPC
          LEFT JOIN LOP L ON LPC.MaLop = L.MaLop
          LEFT JOIN MONHOC M ON LPC.MaMon = M.MaMon
          WHERE LPC.MaGV = ?
          """, (magv, magv))
        rows = cursor.fetchall()
        stt = 1
        for row in rows:
            tree.insert("", "end", values=(
                stt,
                row.TenLop,
                row.SiSo,
                row.TenMon,
                row.NamHoc,
                row.ChuNhiem,
                row.GhiChu
            ))
            stt += 1

      except Exception as e:
        messagebox.showerror("Lỗi SQL", str(e))
    
    # ------------------------- GIAO DIỆN FORM LÍ LỊCH GIÁO VIÊN -------------------------
    # --- THÔNG TIN CÁ NHÂN ---
    # Tiêu đề
    lbl_title = tk.Label(ttgv, text="SƠ YẾU LÍ LỊCH", font=("Times New Roman", 18, "bold"))
    lbl_title.pack(pady=10)

    lbl_thongtincn = tk.Label(ttgv, text="   I. THÔNG TIN CÁ NHÂN", font=("Times New Roman", 14))
    lbl_thongtincn.pack(anchor= "nw", pady=5)

    # Frame chính chứa 2 cột
    frm = tk.Frame(ttgv)
    frm.pack(pady=10)

    # Cột trái: Ảnh
    left = tk.Frame(frm)
    left.grid(row=0, column=0, padx=20)

    tk.Label(left, text="Mã giáo viên: ", font=("Times New Roman", 12)).grid(row=0, column=0, sticky="w")
    entry_Magv = tk.Entry(left, width=10)
    entry_Magv.grid(row=0, column=1, padx=5)

    entry_Magv.insert(0, magv)

    image_label = tk.Label(left, width=20, height=12, bg="white", relief="solid")
    image_label.grid(row=1, column=0, columnspan=2, pady=5)
    tk.Label(left, text="Ảnh màu\n(4 x 6 cm)", font=("Times New Roman", 10)).grid(row=2, column=0, columnspan=2)

    tk.Button(left, text="+", command=upload_image).grid(row=1, column=0, columnspan=2, pady=5)

    # Cột phải: Thông tin giáo viên
    right = tk.Frame(frm)
    right.grid(row=0, column=1,)
    right.grid_columnconfigure(1, weight=1)

    tk.Label(right, text="1) Họ và tên: ", font=("Times New Roman", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_hoten = tk.Entry(right)
    entry_hoten.grid(row=1, column=1, padx=5, pady=5, sticky="we")

    tk.Label(right, text="2) Phái: ", font=("Times New Roman", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
    gender_var = tk.StringVar(value="Nam")
    tk.Radiobutton(right, text="Nam", variable=gender_var, value="Nam").grid(row=2, column=1, padx=5, sticky="w")
    tk.Radiobutton(right, text="Nữ", variable=gender_var, value="Nữ").grid(row=2, column=1, padx=60, sticky="w")

    tk.Label(right, text="3) Ngày sinh: ", font=("Times New Roman", 12)).grid(row=2, column=2, padx=5, pady=5, sticky="w")
    entry_Ngaysinh = tk.Entry(right, width=20)
    entry_Ngaysinh.grid(row=2, column=3, padx=5, pady=5)

    tk.Label(right, text="4) Địa chỉ: ", font=("Times New Roman", 12)).grid(row=3, column=0, padx=5, pady=5, sticky="w")
    entry_Diachi = tk.Entry(right, width=35)
    entry_Diachi.grid(row=3, column=1, padx=5, pady=5, sticky="we")

    tk.Label(right, text="5) CCCD: ", font=("Times New Roman", 12)).grid(row=4, column=0, padx=5, pady=5, sticky="w")
    entry_CCCD = tk.Entry(right, width=20)
    entry_CCCD.grid(row=4, column=1, padx=5, pady=5, sticky="w")
  
    tk.Label(right, text="6) SĐT liên hệ: ", font=("Times New Roman", 12)).grid(row=4, column=2, padx=5, pady=5, sticky="w")
    entry_SDT = tk.Entry(right, width=20)
    entry_SDT.grid(row=4, column=3, padx=5, pady=5, sticky="w")

    tk.Label(right, text="7) Dân tộc: ", font=("Times New Roman", 12)).grid(row=5, column=0, padx=5, pady=5, sticky="w")
    entry_Dantoc = tk.Entry(right, width=20)
    entry_Dantoc.grid(row=5, column=1, padx=5, pady=5, sticky="w")

    tk.Label(right, text="8) Tôn giáo: ", font=("Times New Roman", 12)).grid(row=5, column=2, padx=5, pady=5, sticky="w")
    entry_Tongiao = tk.Entry(right, width=20)
    entry_Tongiao.grid(row=5, column=3, padx=5, pady=5, sticky="w")
  
    # --- THÔNG TIN CHUYÊN MÔN ---
    # tiêu đề
    lbl_thongtincn = tk.Label(ttgv, text="   II. THÔNG TIN CHUYÊN MÔN", font=("Times New Roman", 14))
    lbl_thongtincn.pack(anchor= "nw",padx=5, pady=10)

    frmsec = tk.Frame(ttgv)
    frmsec.pack(anchor="w", padx=20, pady=5)

    tk.Label(frmsec, text="1) Trạng thái: ", font=("Times New Roman", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    trangthai_var = tk.StringVar(value="Đang công tác")
    tk.Radiobutton(frmsec, text="Đang công tác", variable=trangthai_var, value="Đang công tác").grid(row=0, column=1, padx=5, sticky="w")
    tk.Radiobutton(frmsec, text="Đã nghỉ hưu", variable=trangthai_var, value="Đã nghỉ hưu").grid(row=0, column=2, padx=60, sticky="w")

    tk.Label(frmsec, text="2) Tổ bộ môn: ", font=("Times New Roman", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_tento = tk.Entry(frmsec)
    entry_tento.grid(row=1, column=1, padx=5, pady=5, sticky="we")

    tk.Label(frmsec, text="3) Tổ trưởng: ", font=("Times New Roman", 12)).grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_totruong = tk.Entry(frmsec)
    entry_totruong.grid(row=1, column=3, padx=5, pady=5, sticky="we")

    tk.Label(frmsec, text="4) Chuyên ngành đào tạo: ", font=("Times New Roman", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_chuyennganh = tk.Entry(frmsec)
    entry_chuyennganh.grid(row=2, column=1, padx=5, pady=5, sticky="we")

    tk.Label(frmsec, text="5) Trình độ chuyên môn: ", font=("Times New Roman", 12)).grid(row=2, column=2, padx=5, pady=5, sticky="w")
    entry_trinhdo = tk.Entry(frmsec)
    entry_trinhdo.grid(row=2, column=3, padx=5, pady=5, sticky="we")

    # --- LỊCH PHÂN CÔNG CÁ NHÂN ---
    lbl_thongtincn = tk.Label(ttgv, text="   III. LỊCH PHÂN CÔNG CÁ NHÂN", font=("Times New Roman", 14))
    lbl_thongtincn.pack(anchor= "w",padx=5, pady=10)

    columns = ("STT","Lớp", "Sỉ số","Môn học","Năm","Chủ nhiệm", "Ghi chú")
    tree = ttk.Treeview(ttgv, columns=columns, show="headings", height=5)

    for col in columns: tree.heading(col, text=col)

    tree.column("STT", width=50, anchor="center")
    tree.column("Lớp", width=70, anchor="center")
    tree.column("Sỉ số", width=50, anchor="center")
    tree.column("Môn học", width=100, anchor="center")
    tree.column("Năm", width=50, anchor="center")
    tree.column("Chủ nhiệm", width=50, anchor="center")
    tree.column("Ghi chú", width=200, anchor="center")

    tree.pack(padx=10, pady=5, fill="both")
    load_data()
  # ------------------------- KẾT THÚC FORM LÍ LỊCH GIÁO VIÊN -------------------------
  
  # --- CÁC NÚT CỦA GIAO DIỆN TÌM KIẾM ---
  # Hàm thoát về form_trangchu
  def thoat_action():
    timkiem.destroy()
    form_trangchu.HomeForm(role)

  # Frame chứa nút các nút ở form tim kiếm
  frame_buttons = tk.Frame(timkiem)
  frame_buttons.pack(pady=10)
  # Nút tìm
  btn_tim = tk.Button(frame_buttons, text="Tìm kiếm", width=10, command=timmagv)
  btn_tim.pack(side= 'left', padx=10)
  # Nút thoát
  btn_thoat = tk.Button(frame_buttons, text="Thoát", width=10, command = thoat_action)
  btn_thoat.pack(side= 'left', padx=10)
  
  timkiem.mainloop()

if __name__ == "__main__":
  main()
