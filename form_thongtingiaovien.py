import tkinter as tk
from tkinter import ttk, messagebox
import form_trangchu
from tkcalendar import DateEntry
import pyodbc
"""try:
  from tkcalendar import DateEntry
except Exception:
  DateEntry = None"""

  # Hàm kết nối cơ sở dữ liệu
def get_connection():
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=.\\SQLEXPRESS;"
            "DATABASE=QLGVTP;"
            "Trusted_Connection=yes;"
        )
        return conn
  # Căn giữa cửa sổ
def center_window(win, w=700, h=500):
  ws = win.winfo_screenwidth()
  hs = win.winfo_screenheight()
  x = (ws // 2) - (w // 2)
  y = (hs // 2) - (h // 2)
  win.geometry(f'{w}x{h}+{x}+{y}')


def main():
  thongtingiaovien = tk.Tk()
  thongtingiaovien.title("Quản lý giáo viên phổ thông")
  center_window(thongtingiaovien, 700, 500)
  thongtingiaovien.resizable(False, False)

  # Tiêu đề
  lbl_title = tk.Label(thongtingiaovien, text="Quản lý giáo viên phổ thông", font=("Arial", 18, "bold"))
  lbl_title.pack(pady=10)

  # Frame nhập thông tin
  frame_info = tk.Frame(thongtingiaovien)
  frame_info.pack(pady=5, padx=10, fill="x")

  tk.Label(frame_info, text="Mã số").grid(row=0, column=0, padx=5, pady=5, sticky="w")
  entry_maso = tk.Entry(frame_info, width=10)
  entry_maso.grid(row=0, column=1, padx=5, pady=5, sticky="w")

  tk.Label(frame_info, text="Email").grid(row=0, column=2, padx=5, pady=5, sticky="w")
  entry_email = tk.Entry(frame_info, width=30)
  entry_email.grid(row=0, column=3, padx=5, pady=5, sticky="w")

  tk.Label(frame_info, text="Họ lót").grid(row=1, column=0, padx=5, pady=5, sticky="w")
  entry_holot = tk.Entry(frame_info, width=25)
  entry_holot.grid(row=1, column=1, padx=5, pady=5, sticky="w")

  tk.Label(frame_info, text="Tên").grid(row=1, column=2, padx=5, pady=5, sticky="w")
  entry_ten = tk.Entry(frame_info, width=15)
  entry_ten.grid(row=1, column=3, padx=5, pady=5, sticky="w")

  tk.Label(frame_info, text="Phái").grid(row=2, column=0, padx=5, pady=5, sticky="w")
  gender_var = tk.StringVar(value="Nam")
  tk.Radiobutton(frame_info, text="Nam", variable=gender_var, value="Nam").grid(row=2, column=1, padx=5, sticky="w")
  tk.Radiobutton(frame_info, text="Nữ", variable=gender_var, value="Nữ").grid(row=2, column=1, padx=60, sticky="w")

  tk.Label(frame_info, text="Ngày sinh").grid(row=2, column=2, padx=5, pady=5, sticky="w")
  date_entry = DateEntry(frame_info, width=12, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
  date_entry.grid(row=2, column=3, padx=5, pady=5, sticky="w")

  
  #CÁC HÀM XỬ LÝ DỮ LIỆU
  # ---------------- HÀM LOAD DỮ LIỆU VÀO TREEVIEW ----------------
  # HÀM LOAD DỮ LIỆU GIÁO VIÊN
    
  def load_data():
        tree.delete(*tree.get_children())
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT 
            MaGV, HovaTendem, Ten, Phai, NgaySinh, Email 
        FROM GIAOVIEN
        ORDER BY MaGV;
        """

        cursor.execute(query)
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=tuple(row))

        conn.close()

   # ---------------- HÀM LẤY DỮ LIỆU KHI CHỌN DÒNG TRONG TREEVIEW ----------------
  def on_select(event):
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0], 'values')

        entry_maso.delete(0, tk.END)
        entry_maso.insert(0, values[0])

        entry_email.delete(0, tk.END)
        entry_email.insert(0, values[5])

        entry_holot.delete(0, tk.END)
        entry_holot.insert(0, values[1])

        entry_ten.delete(0, tk.END)
        entry_ten.insert(0, values[2])

        # Cập nhật phái (Nam/Nữ)
        gender_var.set(values[3])

        # Cập nhật ngày sinh
        try:
          date_entry.set_date(values[4])
        except:
          date_entry.delete(0, tk.END)
          date_entry.insert(0, values[4])

  # ---------------- HÀM THÊM DỮ LIỆU ----------------
  def add_data():
    maso = entry_maso.get()
    holot = entry_holot.get()
    ten = entry_ten.get()
    phai = gender_var.get()
    ngaysinh = date_entry.get_date() 
    email = entry_email.get()

    # Kiểm tra dữ liệu
    if not maso or not holot or not ten or not email:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
        return

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Thêm dữ liệu vào bảng GiaoVien
            cursor.execute("""
                INSERT INTO GiaoVien(MaGV, HovaTenDem, Ten, Phai, NgaySinh, Email)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (maso, holot, ten, phai, ngaysinh, email))

            conn.commit()
            conn.close()

            # Reload dữ liệu
            load_data()

            # Xóa form
            cancel_action()

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
 
    # ---------------- HÀM LƯU DỮ LIỆU ---------------
  def save_data():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chọn dòng", "Hãy chọn một dòng để lưu/sửa!")
        return

    # Lấy dữ liệu cũ từ Treeview
    old_values = tree.item(selected[0], 'values')

    # Lấy dữ liệu mới từ entry, nếu rỗng thì giữ giá trị cũ
    maso = entry_maso.get() if entry_maso.get() else old_values[0]
    holot = entry_holot.get() if entry_holot.get() else old_values[1]
    ten = entry_ten.get() if entry_ten.get() else old_values[2]
    phai = gender_var.get() if gender_var.get() else old_values[3]
    ngaysinh = date_entry.get() if date_entry.get() else old_values[4]
    email = entry_email.get() if entry_email.get() else old_values[5]

    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Cập nhật dữ liệu trong database
        cursor.execute("""
            UPDATE GIAOVIEN
            SET HovaTendem = ?, Ten = ?, Phai = ?, NgaySinh = ?, Email = ?
            WHERE MaGV = ?
        """, (holot, ten, phai, ngaysinh, email, maso))
        conn.commit()
        conn.close()

        # Cập nhật luôn Treeview
        tree.item(selected[0], values=(maso, holot, ten, phai, ngaysinh, email))

        messagebox.showinfo("Thành công", "Cập nhật dữ liệu thành công!")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

    # ---------------- HÀM SỬA DỮ LIỆU ----------------
  def edit_data():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chọn dòng", "Hãy chọn một dòng để sửa!")
        return

    # Lấy dữ liệu dòng đang chọn trong Treeview
    values = tree.item(selected[0], 'values')

    # Điền dữ liệu vào các Entry để sửa
    entry_maso.delete(0, tk.END)
    entry_maso.insert(0, str(values[0]))

    entry_holot.delete(0, tk.END)
    entry_holot.insert(0, str(values[1]))

    entry_ten.delete(0, tk.END)
    entry_ten.insert(0, str(values[2]))

    # Cập nhật phái (Nam/Nữ)
    gender_var.set(values[3])

    # Cập nhật ngày sinh
    date_entry.set_date(values[4])

    entry_email.delete(0, tk.END)
    entry_email.insert(0, str(values[5]))

    # Focus vào Entry đầu tiên
    entry_maso.focus()


   # ---------------- HÀM HỦY THÔNG TIN TRÊN CÁC ENTRY VÀ BỎ CHỌN DÒNG ----------------  
  from datetime import date
  def cancel_action():
    tree.selection_remove(tree.selection())  # bỏ chọn dòng hiện tại
    entry_maso.delete(0, tk.END)
    entry_holot.delete(0, tk.END)
    entry_ten.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    gender_var.set("Nam")        # bỏ chọn Nam/Nữ
    date_entry.set_date(date.today())   # xoá ngày, reset về ngày hiện tại
    
    
  # ---------------- HÀM XÓA ----------------
  def delete_data():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chọn dòng", "Hãy chọn một dòng để xóa!")
        return

    # Lấy mã giáo viên của dòng được chọn (giả sử cột đầu tiên là MaGV)
    magv = tree.item(selected[0])['values'][0]

    # Xác nhận xóa
    if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa giáo viên {magv}?"):
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Xóa dữ liệu trong database
        cursor.execute("DELETE FROM GIAOVIEN WHERE MaGV = ?", (magv,))
        conn.commit()
        conn.close()

        # Xóa luôn dòng trên Treeview
        for sel in selected:
            tree.delete(sel)

        messagebox.showinfo("Thành công", f"Đã xóa giáo viên {magv} thành công!")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# ---------------- HÀM THOÁT ----------------
  def thoat_action():
        thongtingiaovien.destroy()  # đóng cửa sổ hiện tại
        form_trangchu.main()
  # Frame nút chức năng
  frm_btn = tk.Frame(thongtingiaovien)
  frm_btn.pack(pady=10)

  tk.Button(frm_btn, text="Thêm", width=12, command=add_data).grid(row=0, column=0, padx=5)
  tk.Button(frm_btn, text="Lưu", width=12, command=save_data ).grid(row=0, column=1, padx=5)
  tk.Button(frm_btn, text="Sửa", width=12, command=edit_data).grid(row=0, column=2, padx=5)
  tk.Button(frm_btn, text="Hủy", width=12, command=cancel_action).grid(row=0, column=3, padx=5)
  tk.Button(frm_btn, text="Xóa", width=12, command=delete_data).grid(row=0, column=4, padx=5)
  tk.Button(frm_btn, text="Thoát", width=12, command=thoat_action).grid(row=0, column=5, padx=5) 

  # Bảng danh sách giáo viên
  lbl_ds = tk.Label(thongtingiaovien, text="Danh sách giáo viên", font=("Arial", 10))
  lbl_ds.pack(pady=5, anchor="w", padx=10)

  columns = ("maso", "holot", "ten", "phai", "ngaysinh", "email")
  tree = ttk.Treeview(thongtingiaovien, columns=columns, show="headings", height=10)

  for col in columns:
    tree.heading(col, text=col.capitalize())

  tree.column("maso", width=60, anchor="center")
  tree.column("holot", width=150)
  tree.column("ten", width=100)
  tree.column("phai", width=70, anchor="center")
  tree.column("ngaysinh", width=100, anchor="center")
  tree.column("email", width=200)

  tree.pack(padx=10, pady=5, fill="both")
  load_data()
  tree.bind("<<TreeviewSelect>>", on_select)
  thongtingiaovien.mainloop()


if __name__ == "__main__":
  main()