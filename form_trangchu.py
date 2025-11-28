import tkinter as tk
from tkinter import messagebox
import form_thongtingiaovien
import form_timkiem
import form_thongtinbomon
import form_phancong   
import pyodbc


# ------------------------- KẾT NỐI SQL SERVER -------------------------
def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=.\\SQLEXPRESS;"
        "DATABASE=QLGVTP;"
        "Trusted_Connection=yes;"
    )

#CĂN GIỮA CỬA SỔ 
def center_window(win, w=400, h=600):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

# ---------------------- HÀM KIỂM TRA LOGIN -----------------------
def check_login(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT TaiKhoan, Role, MaGV
    FROM Users
    WHERE TaiKhoan = ? 
      AND MatKhau COLLATE Latin1_General_CS_AS = ?
      AND TrangThaiHH = N'Hoạt động'
    """, (username, password))

    row = cur.fetchone()
    conn.close()
    return row  # None nếu sai, hoặc (TaiKhoan, Role, MaGV)

# --------------------- HÀM TẠO TÀI KHOẢN ---------------------
def add_account(username, password):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Kiểm tra trùng user
        cur.execute("SELECT TaiKhoan FROM Users WHERE TaiKhoan = ?", (username,))
        if cur.fetchone():
            conn.close()
            return False, "Tài khoản đã tồn tại!"

        # Thêm tài khoản
        cur.execute("""
            INSERT INTO Users (TaiKhoan, MatKhau, Role, TrangThaiHH)
            VALUES (?, ?, 'User', N'Hoạt động')
        """, (username, password))

        conn.commit()
        conn.close()
        return True, "Tạo tài khoản thành công!"

    except Exception as e:
        return False, f"Lỗi DB: {e}"


# -------------------------- FORM ĐĂNG NHẬP --------------------------
class LoginForm:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Đăng nhập hệ thống")
        center_window(self.win, 300, 230)

        tk.Label(self.win, text="Đăng nhập", font=("Times New Roman", 14, "bold")).pack(pady=10)

        frm = tk.Frame(self.win)
        frm.pack()

        tk.Label(frm, text="Tài khoản:").grid(row=0, column=0)
        self.txt_user = tk.Entry(frm, width=25)
        self.txt_user.grid(row=0, column=1)

        tk.Label(frm, text="Mật khẩu:").grid(row=1, column=0)
        self.show_pass = False                                  # trạng thái để bật/tắt mật khẩu
        self.txt_pass = tk.Entry(frm, width=25, show="*")
        self.txt_pass.grid(row=1, column=1)

        # Nút hiện/ẩn mật khẩu
        def Anpass():
            if self.show_pass:
                self.txt_pass.config(show="*")
                btn_toggle_pass.config(text="👁")
                self.show_pass = False
            else:
                self.txt_pass.config(show="")
                btn_toggle_pass.config(text="👁")
                self.show_pass = True

        btn_toggle_pass = tk.Button(frm, text="👁", width=2, command=Anpass)
        btn_toggle_pass.grid(row=1, column=2, padx=5)

        tk.Button(self.win, text="Đăng nhập", width=12, command=self.login).pack(pady=10)

        # Label "Tạo tài khoản" (gạch chân, trông như link)
        lbl_create = tk.Label(self.win, text="Tạo tài khoản",
                    fg="blue",cursor="hand2",font=("Times New Roman", 10, "underline"))
        lbl_create.pack(pady=10)
        # bind tới method của lớp (method phải nhận event)
        lbl_create.bind("<Button-1>", self.open_create_account)

        self.win.mainloop()


    def open_create_account(self, event):
        CreateAccountForm(self.win)

    # Xử lý đăng nhập
    def login(self):
        username = self.txt_user.get().strip()
        password = self.txt_pass.get().strip()

        result = check_login(username, password)

        if not result:
            messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!")
            return
        username, role, ma_gv = result

        self.win.destroy()
        HomeForm(role, ma_gv)


# ------------------------ FORM TRANG CHỦ -------------------------
class HomeForm:
    def __init__(self, role, ma_gv):
        self.role = role
        self.ma_gv = ma_gv

        self.trangchu = tk.Tk()
        self.trangchu.title("Chương trình quản lý giáo viên phổ thông")
        center_window(self.trangchu, 600, 350)

        self.Label = tk.Label(self.trangchu, text="Chào mừng đến với Hệ thống quản lý giáo viên trường THPT", fg="Red", font=("Times New Roman", 15, "bold"))
        self.Label.pack(anchor="center", pady=80)

        # Các hàm xử lý của nút
        def xem_dsgv():
            form_thongtingiaovien.main(self.role)

        def tim_kiem_gv():
            form_timkiem.main(self.role)

        def xemtobomon():
            form_thongtinbomon.main(self.role)
            
        def xemphancong():
            form_phancong.main(self.role)

        # MENU BAR (dạng VS Code)
        menubar = tk.Menu(self.trangchu)
        self.trangchu.config(menu=menubar)

        # ten menu Trang chủ
        trangchu_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Trang chủ", menu=trangchu_menu)


        trangchu_menu.add_command(label="Thông tin giáo viên", command=xem_dsgv)
        trangchu_menu.add_command(label="Tổ bộ môn", command=xemtobomon)
        trangchu_menu.add_command(label="Lịch phân công", command=xemphancong)
        trangchu_menu.add_command(label="Tìm kiếm giáo viên", command=tim_kiem_gv)
        trangchu_menu.add_command(label="Thoát", command=self.trangchu.destroy)

        """# Frame chứa 4 nút nằm ngang
        frame_buttons = tk.Frame(self.trangchu)
        frame_buttons.pack(anchor='nw', pady=10, padx=10)

        # ---- Nút trang chủ ----
        tk.Button(frame_buttons, text="Trang chủ", width=12, state="disabled").pack(side="left", padx=5)
        # ---- Nút mở Form con ----
        self.btn_dsgv = tk.Button(frame_buttons, text="Danh sách giáo viên", width=15, command=xem_dsgv)
        self.btn_dsgv.pack(side="left", padx=5)

        self.btn_tkgv = tk.Button(frame_buttons, text="Tìm kiếm giáo viên", width=15, command=tim_kiem_gv)
        self.btn_tkgv.pack(side="left", padx=5)

        self.btn_bomon = tk.Button(frame_buttons, text="Tổ bộ môn", width=15, command=xemtobomon)
        self.btn_bomon.pack(side="left", padx=5)

        self.btn_phancong = tk.Button(frame_buttons, text="Lịch phân công", width=15, command=xemphancong)
        self.btn_phancong.pack(side="left", padx=5)

        
        # ---- NÚT THOÁT ----
        tk.Button(self.trangchu, text="Thoát", width=10, command=self.trangchu.destroy).pack(
            side="bottom", anchor="e", padx=10, pady=10
        )"""

        
        
        self.trangchu.mainloop()
# ------------------------- KẾT THÚC FORM TRANG CHỦ -------------------------

# ----------------------------- MỞ FORM TẠO ACC MỚI ------------------------
class CreateAccountForm:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Tạo tài khoản")
        center_window(self.top, 300, 230)

        tk.Label(self.top, text="Tạo tài khoản mới", font=("Times New Roman", 13, "bold")).pack(pady=10)

        frm = tk.Frame(self.top)
        frm.pack()

        tk.Label(frm, text="Tài khoản:").grid(row=0, column=0)
        self.txt_user = tk.Entry(frm, width=25)
        self.txt_user.grid(row=0, column=1)

        tk.Label(frm, text="Mật khẩu:").grid(row=1, column=0)
        self.txt_pass = tk.Entry(frm, width=25)
        self.txt_pass.grid(row=1, column=1)

        tk.Label(frm, text="Nhập lại MK:").grid(row=2, column=0)
        self.txt_pass2 = tk.Entry(frm, width=25)
        self.txt_pass2.grid(row=2, column=1)

        # ---- Nút Đăng ký & Quay lại ----
        frame_buttons = tk.Frame(self.top)
        frame_buttons.pack(pady=10)

        btn_dk = tk.Button(frame_buttons, text="Đăng ký", width=12, command=self.create)
        btn_dk.pack(side="left", padx=5)

        btn_back = tk.Button(frame_buttons, text="Quay lại", width=12, command=self.top.destroy)
        btn_back.pack(side="left", padx=5)

    # ---- XỬ LÝ TẠO TÀI KHOẢN ----
    def create(self):
        user = self.txt_user.get().strip()
        pw1 = self.txt_pass.get().strip()
        pw2 = self.txt_pass2.get().strip()

        if pw1 != pw2:
            messagebox.showerror("Lỗi", "Mật khẩu nhập lại không khớp!")
            return
        
        if len(user) == 0 or len(pw1) == 0:
            messagebox.showerror("Lỗi", "Không được để trống!")
            return

        success, msg = add_account(user, pw1)

        if not success:
            messagebox.showerror("Lỗi", msg)
            return

        messagebox.showinfo("Thành công", "Tạo tài khoản thành công!")
        self.top.destroy()

if __name__ == "__main__":
    LoginForm()
