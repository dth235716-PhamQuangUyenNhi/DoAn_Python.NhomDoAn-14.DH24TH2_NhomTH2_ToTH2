import tkinter as tk
from tkinter import ttk, messagebox
import DEMO_CT_QLGVPT
import form_timkiem
import form_phancong
import form_thongtinbomon

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

  # Frame chứa 4 nút nằm ngang
  frame_buttons = tk.Frame(trangchu)
  frame_buttons.pack(anchor='nw', pady=10, padx=10)



  # Nút 1: "Trang Chủ", disabled
  btn_trangchu = tk.Button(frame_buttons, text="Trang Chủ", state="disabled", width=10)
  btn_trangchu.pack(side="left", padx=5)

  def xem_thong_tin_giaovien():
    DEMO_CT_QLGVPT.main()  # Mở form trang chủ

  # Nút 2: "Xem thông tin giáo viên"
  btn_giaovien = tk.Button(frame_buttons, text="Thông tin giáo viên", width=15, command=xem_thong_tin_giaovien)
  btn_giaovien.pack(side="left", padx=5)


  def tim_giaovien():
    form_timkiem.main()  # Mở form tim kiếm giáo viên

  def Lich_phancong():
    form_phancong.main()  # Mở form phân công

  def Thong_tinbomon():
    form_thongtinbomon.main()  # Mở form thông tin bộ môn

  # Nút 4: "tìm kiếm giáo viên"
  btn_tkgiaovien = tk.Button(frame_buttons, text="Tìm kiếm giáo viên", width=15, command=tim_giaovien)
  btn_tkgiaovien.pack(side="left", padx=5)

   # Nút 4: "lịch phân công"
  btn_phancong = tk.Button(frame_buttons, text="Lịch phân công", width=15, command=Lich_phancong)
  btn_phancong.pack(side="left", padx=5)

  # Nút 4: "thông tin bộ môn"
  btn_thongtinbomon = tk.Button(frame_buttons, text="Thông tin bộ môn", width=15, command=Thong_tinbomon)
  btn_thongtinbomon.pack(side="left", padx=5)

  # Nút thoát
  btn_thoat = tk.Button(trangchu, text="Thoat", width=10, command=quit)
  btn_thoat.pack(side = 'bottom', anchor= "e", padx=10, pady=10)

  trangchu.mainloop()

if __name__ == "__main__":
    main()
  