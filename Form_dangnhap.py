import tkinter as tk
from tkinter import ttk, messagebox
import form_trangchu

# căn giữa cửa sổ
def center_window(win, w=300, h=600):
  ws = win.winfo_screenwidth()
  hs = win.winfo_screenheight()
  x = (ws // 2) - (w // 2)
  y = (hs // 2) - (h // 2)
  win.geometry(f'{w}x{h}+{x}+{y}')

def main():
  dangnhap = tk.Tk()
  dangnhap.title("Đăng nhập hệ thống")
  center_window(dangnhap, 300, 200)
  dangnhap.resizable(False, False)

  # ======= Giao diện đăng nhập =======
  lbl_title = tk.Label(dangnhap, text="Đăng nhập", font=("Arial", 14, "bold"))
  lbl_title.pack(pady=10)

  frm_input = tk.Frame(dangnhap)
  frm_input.pack(pady=5)

  # Ô nhập tài khoản
  tk.Label(frm_input, text="Tài khoản:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
  txt_user = tk.Entry(frm_input, width=25)
  txt_user.grid(row=0, column=1, padx=5, pady=5)

  # Ô nhập mật khẩu
  tk.Label(frm_input, text="Mật khẩu:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
  txt_pass = tk.Entry(frm_input, width=25, show="*")
  txt_pass.grid(row=1, column=1, padx=5, pady=5)
  # Hàm xử lý sự kiện đăng nhập
  def login_action():
        username = txt_user.get()
        password = txt_pass.get()
        # Kiểm tra tài khoản và mật khẩu (ví dụ đơn giản)
        if username == "admin" and password == "123":
            messagebox.showinfo("Thông báo", "Đăng nhập thành công!")
            dangnhap.destroy()  # Đóng cửa sổ đăng nhập
            form_trangchu.main()  # Mở form trang chủ
        else:
            messagebox.showerror("Lỗi", "Tài khoản hoặc mật khẩu không đúng!")
  # Nút đăng nhập
  btn_login = tk.Button(dangnhap, text="Đăng nhập", width=12, command = login_action)
  btn_login.pack(pady=10)
  
  dangnhap.mainloop()

if __name__ == "__main__":
    main()
