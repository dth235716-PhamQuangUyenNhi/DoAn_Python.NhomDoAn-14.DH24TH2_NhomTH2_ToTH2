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

# căn giữa cửa sổ
def center_window(win, w=700, h=400):
  ws = win.winfo_screenwidth()
  hs = win.winfo_screenheight()
  x = (ws // 2) - (w // 2)
  y = (hs // 2) - (h // 2)
  win.geometry(f'{w}x{h}+{x}+{y}')


# ----------------  GIAO DIỆN CHÍNH ----------------
def main(role):
  thongtinbomon = tk.Toplevel()
  thongtinbomon.title("Hệ thống quản lý giáo viên phổ thông")
  center_window(thongtinbomon, 700, 400)
  thongtinbomon.resizable(False, False)

  #Phân quyền
  is_admin = (role == "Admin")

  # Giao diện đăng nhập 
  lbl_title = tk.Label(thongtinbomon, text="Thông tin bộ môn", font=("Times New Roman", 14, "bold"))
  lbl_title.pack(pady=10)

  # Frame nhập thông tin
  frame_info = tk.Frame(thongtinbomon)
  frame_info.pack(pady=10, padx=10, fill="x")

  tk.Label(frame_info, text="Mã tổ: ").grid(row=0, column=0, padx=5, pady=5, sticky="w")
  entry_mato = tk.Entry(frame_info, width=10)
  entry_mato.grid(row=0, column=1, padx=5, pady=5, sticky="w")

  tk.Label(frame_info, text="Tên tổ: ").grid(row=0, column=3, padx=5, pady=5, sticky="w")
  entry_tento = tk.Entry(frame_info, width=25)
  entry_tento.grid(row=0, column=4, padx=5, pady=5, sticky="w")

  tk.Label(frame_info, text="Mã tổ trưởng: ").grid(row=1, column=0, padx=5, pady=5, sticky="w")
  entry_matt = tk.Entry(frame_info, width=10)
  entry_matt.grid(row=1, column=1, padx=5, pady=5, sticky="w")

  tk.Label(frame_info, text="Tên tổ trưởng: ").grid(row=1, column=3, padx=5, pady=5, sticky="w")
  entry_tentt = tk.Entry(frame_info, width=30)
  entry_tentt.grid(row=1, column=4, padx=5, pady=5, sticky="w")

  tk.Label(frame_info, text="SĐT liên lạc: ").grid(row=3, column=0, padx=5, pady=5, sticky="w")
  entry_sdt = tk.Entry(frame_info, width=20)
  entry_sdt.grid(row=3, column=1, padx=5, pady=5, sticky="w")

  tk.Label(frame_info, text="Email: ").grid(row=3, column=3, padx=5, pady=5, sticky="w")
  entry_email = tk.Entry(frame_info, width=30)
  entry_email.grid(row=3, column=4, padx=5, pady=5, sticky="w")



  #CÁC HÀM XỬ LÝ DỮ LIỆU
  # ---------------- HÀM LOAD DỮ LIỆU VÀO TREEVIEW ----------------
  def load_data(tree):
    tree.delete(*tree.get_children())

    conn = get_connection()
    if conn:
        cursor = conn.cursor()

        query = """
            SELECT 
                TB.MaTo,
                TB.TenTo,
                TB.MaToTruong,
                CONCAT(GV.HovaTendem, ' ', GV.Ten) AS TenToTruong,
                GV.SDT,
                GV.Email
            FROM ToBoMon TB
            LEFT JOIN GiaoVien GV ON TB.MaToTruong = GV.MaGV;
        """

        cursor.execute(query)
        
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=tuple(row)) 
        conn.close()

  # ---------------- HÀM LẤY DỮ LIỆU KHI CHỌN DÒNG TRONG TREEVIEW ----------------
  def on_select(event):
    selected = tree.selection()  # trả về tuple các item được chọn
    if selected:
        values = tree.item(selected[0], 'values')  # lấy giá trị dòng đầu tiên
        entry_mato.delete(0, tk.END)
        entry_mato.insert(0, values[0])
        entry_tento.delete(0, tk.END)
        entry_tento.insert(0, values[1])
        entry_matt.delete(0, tk.END)
        entry_matt.insert(0, values[2])
        entry_tentt.delete(0, tk.END)
        entry_tentt.insert(0, values[3])
        entry_sdt.delete(0, tk.END)
        entry_sdt.insert(0, values[4])
        entry_email.delete(0, tk.END)
        entry_email.insert(0, values[5])

  # ---------------- HÀM THÊM DỮ LIỆU ----------------
  def add_data():
    mato = entry_mato.get()
    tento = entry_tento.get()
    matotruong = entry_matt.get()

    # Kiểm tra dữ liệu có đầy đủ không
    if not mato or not tento or not matotruong:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
        return

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Thêm dữ liệu vào database
            cursor.execute("""
                INSERT INTO ToBoMon (MaTo, TenTo, MaToTruong)
                VALUES (?, ?, ?)
            """, (mato, tento, matotruong))
            conn.commit()
            conn.close()

            # Thêm luôn vào Treeview để hiển thị ngay
            tree.insert("", tk.END, values=(mato, tento, matotruong))
            load_data(tree)

            # Xóa Entry sau khi thêm
            cancel_action()

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

  # ---------------- HÀM LƯU DỮ LIỆU ----------------
  def save_data():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chọn dòng", "Hãy chọn một dòng để lưu/sửa!")
        return
    
    # Lấy dữ liệu cũ từ Treeview
    old_values = tree.item(selected[0], 'values')
    mato = entry_mato.get() if entry_mato.get() else old_values[0]
    tento = entry_tento.get() if entry_tento.get() else old_values[1]
    matotruong = entry_matt.get() if entry_matt.get() else old_values[2]


    mato = entry_mato.get()
    tento = entry_tento.get()
    matotruong = entry_matt.get()

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Cập nhật dữ liệu trong database
            cursor.execute("""
                UPDATE ToBoMon
                SET TenTo = ?, MaToTruong = ?
                WHERE MaTo = ?
            """, (tento, matotruong, mato))
            conn.commit()
            conn.close()

            # Cập nhật luôn Treeview
            tree.item(selected[0], values=(mato, tento, matotruong))

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))


  # ---------------- HÀM SỬA DỮ LIỆU ----------------
  def edit_data():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chọn dòng", "Hãy chọn một dòng để sửa!")
        return

    # Lấy dữ liệu dòng đang chọn
    values = tree.item(selected[0], 'values')
    entry_mato.delete(0, tk.END)
    entry_mato.insert(0, str(values[0]))
    entry_tento.delete(0, tk.END)
    entry_tento.insert(0, str(values[1]))
    entry_matt.delete(0, tk.END)
    entry_matt.insert(0, str(values[2]))      

  # ---------------- HÀM HỦY THÔNG TIN TRÊN CÁC ENTRY VÀ BỎ CHỌN DÒNG ----------------
  def cancel_action():
    entry_mato.delete(0, tk.END)
    entry_tento.delete(0, tk.END)
    entry_matt.delete(0, tk.END)
    entry_tentt.delete(0, tk.END)
    entry_sdt.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    # Nếu muốn, có thể bỏ chọn dòng trong Treeview
    tree.selection_remove(tree.selection())

  # ---------------- HÀM XÓA ----------------
  def delete_data():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chọn dòng", "Hãy chọn một dòng để xóa!")
        return

    mato = tree.item(selected)['values'][0]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ToBoMon WHERE MaTo = ?", (mato,))
    conn.commit()
    conn.close()
    # --- Xóa luôn dòng trên Treeview ---
    for sel in selected:
        tree.delete(sel)
    load_data()

   # ---------------- HÀM THOÁT ----------------
  def thoat_action():
    thongtinbomon.destroy()
    form_trangchu.HomeForm(role)

  # ------------------------- GIAO DIỆN -----------------------------
  # Frame nút chức năng
  frm_btn = tk.Frame(thongtinbomon)
  frm_btn.pack(pady=10)

  btn_them = tk.Button(frm_btn, text="Thêm", width=12, command=add_data)
  btn_luu = tk.Button(frm_btn, text="Lưu", width=12, command=save_data)
  btn_sua = tk.Button(frm_btn, text="Sửa", width=12, command=edit_data)
  btn_huy = tk.Button(frm_btn, text="Hủy", width=12, command=cancel_action)
  btn_xoa = tk.Button(frm_btn, text="Xóa", width=12, command=delete_data)
  btn_thoat = tk.Button(frm_btn, text="Thoát", width=12, command=thoat_action)

  # Hiển thị nút theo phân quyền
  if is_admin:
    btn_them.grid(row=0, column=0, padx=5)
    btn_luu.grid(row=0, column=1, padx=5)
    btn_sua.grid(row=0, column=2, padx=5)
    btn_huy.grid(row=0, column=3, padx=5)
    btn_xoa.grid(row=0, column=4, padx=5)
  btn_thoat.grid(row=0, column=5, padx=5) 
      # Bảng danh sách giáo viên
  lbl_ds = tk.Label(thongtinbomon, text="Tổ bộ môn", font=("Times New Roman", 10))
  lbl_ds.pack(pady=5, anchor="w", padx=10)

  columns = ("mato", "tento", "matotruong", "tentotruong","sdt", "email")
  tree = ttk.Treeview(thongtinbomon, columns=columns, show="headings", height=8)

  for col in columns:
    tree.heading(col, text=col.capitalize())

  tree.column("mato", width=30, anchor="center")
  tree.column("tento", width=50)
  tree.column("matotruong", width=30, anchor="center")
  tree.column("tentotruong", width=100)
  tree.column("sdt", width=50, anchor="center")
  tree.column("email", width=100)
  tree.pack(padx=10, pady=5, fill="both")

  load_data(tree)
  tree.bind("<<TreeviewSelect>>", on_select)
  thongtinbomon.mainloop()

if __name__ == "__main__":
  main()