import tkinter as tk
from tkinter import ttk, messagebox
import DEMO_CT_QLGVPT

# căn giữa cửa sổ
def center_window(win, w=300, h=600):
  ws = win.winfo_screenwidth()
  hs = win.winfo_screenheight()
  x = (ws // 2) - (w // 2)
  y = (hs // 2) - (h // 2)
  win.geometry(f'{w}x{h}+{x}+{y}')


def main():
  trangchu = tk.Tk()
  trangchu.title("Chương trình quản lý giáo viên phổ thông")
  center_window(trangchu, 600, 300)
  trangchu.resizable(False, False)

  # Frame chứa 2 nút nằm ngang
  frame_buttons = tk.Frame(trangchu)
  frame_buttons.pack(anchor='nw', pady=10, padx=10)



  # Nút 1: "Trang Chủ", disabled
  btn_trangchu = tk.Button(frame_buttons, text="Trang Chủ", state="disabled", width=15)
  btn_trangchu.pack(side="left", padx=5)

  def xem_thong_tin_giaovien():
    DEMO_CT_QLGVPT.main()  # Mở form trang chủ

  # Nút 2: "Xem thông tin giáo viên"
  btn_giaovien = tk.Button(frame_buttons, text="Xem thông tin giáo viên", width=20, command=xem_thong_tin_giaovien)
  btn_giaovien.pack(side="left", padx=5)



  trangchu.mainloop()

if __name__ == "__main__":
    main()