import tkinter as tk
from tkinter import ttk, messagebox
import form_trangchu

def center_window(win, w=600, h=400):
  ws = win.winfo_screenwidth()
  hs = win.winfo_screenheight()
  x = (ws // 2) - (w // 2)
  y = (hs // 2) - (h // 2)
  win.geometry(f'{w}x{h}+{x}+{y}')


def main():
  phancong = tk.Tk()
  phancong.title("Quản lý giáo viên phổ thông")
  center_window(phancong, 600, 400)
  phancong.resizable(False, False)

  # Tiêu đề
  lbl_title = tk.Label(phancong, text="Lịch phân công", font=("Arial", 18, "bold"))
  lbl_title.pack(pady=10)

    # MENU BAR (dạng VS Code)
  menubar = tk.Menu(phancong)
  phancong.config(menu=menubar)

    # Menu Năm học
  year_menu = tk.Menu(menubar, tearoff=0)
  menubar.add_cascade(label="Năm học", menu=year_menu)

  # Thêm năm vào MENU sau này chỉnh lại để thêm nhiều năm
  year_menu.add_command(label="2023")
  year_menu.add_command(label="2024")
  year_menu.add_command(label="2025")

  # ----- DANH SÁCH GIÁO VIÊN -----
  # Bảng danh sách giáo viên
  lbl_ds = tk.Label(phancong, text="Danh sách phân công dạy học", font=("Arial", 10))
  lbl_ds.pack(pady=5, anchor="w", padx=10)

  columns = ("Nam", "masogv", "ten", "lop", "bomon", "siso")
  tree = ttk.Treeview(phancong, columns=columns, show="headings", height=10)

  for col in columns:
    tree.heading(col, text=col.capitalize())

  tree.column("Nam", width=60, anchor="center")
  tree.column("masogv", width=60)
  tree.column("ten", width=100)
  tree.column("lop", width=70, anchor="center")
  tree.column("bomon", width=70, anchor="center")
  tree.column("siso", width=60, anchor="center")

  tree.pack(padx=10, pady=5, fill="both")


  # Hàm thoát về form_trangchu
  def thoat_action():
        phancong.destroy()  # đóng cửa sổ hiện tại
        form_trangchu.main()
  # Nút thoát
  btn_thoat = tk.Button(phancong, text="Thoat", width=10, command=thoat_action)
  btn_thoat.pack(side = 'bottom', anchor= "e", padx=10, pady=10)

  phancong.mainloop()

if __name__ == "__main__":
  main()