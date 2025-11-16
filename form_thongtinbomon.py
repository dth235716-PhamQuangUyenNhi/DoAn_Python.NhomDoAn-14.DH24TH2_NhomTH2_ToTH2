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
  thongtinbomon = tk.Tk()
  thongtinbomon.title("Đăng nhập hệ thống")
  center_window(thongtinbomon, 300, 200)
  thongtinbomon.resizable(False, False)
  # Giao diện đăng nhập 
  lbl_title = tk.Label(thongtinbomon, text="Thông tin bộ môn", font=("Arial", 14, "bold"))
  lbl_title.pack(pady=10)

  frm_input = tk.Frame(thongtinbomon)
  frm_input.pack(pady=5)
  # Các ô nhập thông tin bộ môn
  lbl_mato = tk.Label(frm_input, text="Mã tổ:")
  lbl_mato.grid(row=0, column=0, sticky="e", padx=5, pady=5)
  ent_mato = tk.Entry(frm_input, width=30)
  ent_mato.grid(row=0, column=1, pady=5)

  lbl_tento = tk.Label(frm_input, text="Tên tổ:")
  lbl_tento.grid(row=1, column=0, sticky="e", padx=5, pady=5)
  ent_tento = tk.Entry(frm_input, width=30)
  ent_tento.grid(row=1, column=1, pady=5)

  # Hàm thoát về form_trangchu
  def thoat_action():
        thongtinbomon.destroy()  # đóng cửa sổ hiện tại
        form_trangchu.main()


  # Các nút chức năng 
  frm_btn = tk.Frame(thongtinbomon)
  frm_btn.pack(pady=10)

  btn_save = tk.Button(frm_btn, text="Lưu", width=10, )
  btn_save.grid(row=0, column=0, padx=5)

  # Nút thoát
  btn_thoat = tk.Button(frm_btn, text="Thoát", width=10, command=thoat_action)
  btn_thoat.grid(row=0, column=1, padx=5)
  
  thongtinbomon.mainloop()

if __name__ == "__main__":
  main()