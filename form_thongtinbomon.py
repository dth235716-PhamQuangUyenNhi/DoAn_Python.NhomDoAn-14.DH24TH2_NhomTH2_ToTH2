import tkinter as tk
from tkinter import ttk, messagebox
import form_trangchu

# căn giữa cửa sổ
def center_window(win, w=700, h=400):
  ws = win.winfo_screenwidth()
  hs = win.winfo_screenheight()
  x = (ws // 2) - (w // 2)
  y = (hs // 2) - (h // 2)
  win.geometry(f'{w}x{h}+{x}+{y}')

def main():
  thongtinbomon = tk.Tk()
  thongtinbomon.title("Đăng nhập hệ thống")
  center_window(thongtinbomon, 700, 400)
  thongtinbomon.resizable(False, False)
  # Giao diện đăng nhập 
  lbl_title = tk.Label(thongtinbomon, text="Thông tin bộ môn", font=("Arial", 14, "bold"))
  lbl_title.pack(pady=10)

  # Frame nhập thông tin
  frame_info = tk.Frame(thongtinbomon)
  frame_info.pack(pady=5, padx=10, fill="x")

  tk.Label(frame_info, text="Mã tổ:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
  entry_maso = tk.Entry(frame_info, width=10)
  entry_maso.grid(row=0, column=1, padx=5, pady=5, sticky="w")

  tk.Label(frame_info, text="Tên tổ trưởng:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
  entry_email = tk.Entry(frame_info, width=30)
  entry_email.grid(row=0, column=3, padx=5, pady=5, sticky="w")

  tk.Label(frame_info, text="Tên tổ: ").grid(row=1, column=0, padx=5, pady=5, sticky="w")
  entry_holot = tk.Entry(frame_info, width=25)
  entry_holot.grid(row=1, column=1, padx=5, pady=5, sticky="w")

 
  # Hàm thoát về form_trangchu
  def thoat_action():
        thongtinbomon.destroy()  # đóng cửa sổ hiện tại
        form_trangchu.main()


  # Các nút chức năng 
  frm_btn = tk.Frame(thongtinbomon)
  frm_btn.pack(pady=10)
  # Frame nút


  tk.Button(frm_btn, text="Thêm", width=12).grid(row=0, column=0, padx=5)
  tk.Button(frm_btn, text="Lưu", width=12).grid(row=0, column=1, padx=5)
  tk.Button(frm_btn, text="Sửa", width=12).grid(row=0, column=2, padx=5)
  tk.Button(frm_btn, text="Hủy", width=12).grid(row=0, column=3, padx=5)
  tk.Button(frm_btn, text="Xóa", width=12).grid(row=0, column=4, padx=5)
  tk.Button(frm_btn, text="Thoát", width=12, command=thongtinbomon.quit).grid(row=0, column=5, padx=5) 

  """btn_save = tk.Button(frm_btn, text="Lưu", width=10, )
  btn_save.grid(row=0, column=0, padx=5)

  # Nút thoát
  btn_thoat = tk.Button(frm_btn, text="Thoát", width=10, command=thoat_action)
  btn_thoat.grid(row=0, column=1, padx=5)"""

  # Bảng danh sách giáo viên
  lbl_ds = tk.Label(thongtinbomon, text="Danh sách giáo viên", font=("Arial", 10))
  lbl_ds.pack(pady=5, anchor="w", padx=10)

  columns = ("mato", "tento", "tentotruong")
  tree = ttk.Treeview(thongtinbomon, columns=columns, show="headings", height=8)

  for col in columns:
    tree.heading(col, text=col.capitalize())

  tree.column("mato", width=30, anchor="center")
  tree.column("tento", width=50)
  tree.column("tentotruong", width=100)


  tree.pack(padx=10, pady=5, fill="both")
  
  thongtinbomon.mainloop()

if __name__ == "__main__":
  main()