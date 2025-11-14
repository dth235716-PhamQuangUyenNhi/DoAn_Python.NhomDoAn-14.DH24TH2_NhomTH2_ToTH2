import tkinter as tk
from tkinter import ttk, messagebox
import form_trangchu

# căn giữa cửa sổ
def center_window(win, w=300, h=200):
  ws = win.winfo_screenwidth()
  hs = win.winfo_screenheight()
  x = (ws // 2) - (w // 2)
  y = (hs // 2) - (h // 2)
  win.geometry(f'{w}x{h}+{x}+{y}')

def main():
  timkiem = tk.Tk()
  timkiem.title("Đăng nhập hệ thống")
  center_window(timkiem, 300, 200)
  timkiem.resizable(False, False)

  # ======= Giao diện đăng nhập =======
  lbl_title = tk.Label(timkiem, text="Tìm kiếm giáo viên", font=("Arial", 14, "bold"))
  lbl_title.pack(pady=10)

  frm_input = tk.Frame(timkiem)
  frm_input.pack(pady=5)

  # Ô nhập tài khoản
  tk.Label(frm_input, text="Mã số giáo viên:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
  txt_tkgv = tk.Entry(frm_input, width=25)
  txt_tkgv.grid(row=0, column=1, padx=5, pady=5)

 
  # Hàm xử lý sự kiện đăng nhập
  def login_action():
        username = "admin"
        # Kiểm tra mã số của giáo viên
        if username == "admin": #viết code lại tìm
            form_trangchu.main()  # Mở form ket qua gv
        else:
            messagebox.showerror("Không có giáo viên nào có mã số này!")

 # Hàm thoát về form_trangchu
  def thoat_action():
        timkiem.destroy()  # đóng cửa sổ hiện tại
        form_trangchu.main()

  # Frame chứa nút
  frame_buttons = tk.Frame(timkiem)
  frame_buttons.pack(pady=10)
  # Nút tìm
  btn_tim = tk.Button(frame_buttons, text="Tìm kiếm", width=10, command = login_action)
  btn_tim.pack(side= 'left', padx=10)
  # Nút thoát
  btn_thoat = tk.Button(frame_buttons, text="Thoát", width=10, command = thoat_action)
  btn_thoat.pack(side= 'left', padx=10)
  
  timkiem.mainloop()

if __name__ == "__main__":
    main()
