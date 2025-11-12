import tkinter as tk
from tkinter import ttk, messagebox

try:
  from tkcalendar import DateEntry
except Exception:
  DateEntry = None


def center_window(win, w=700, h=500):
  ws = win.winfo_screenwidth()
  hs = win.winfo_screenheight()
  x = (ws // 2) - (w // 2)
  y = (hs // 2) - (h // 2)
  win.geometry(f'{w}x{h}+{x}+{y}')


def main():
  root = tk.Tk()
  root.title("Quản lý giáo viên phổ thông")
  center_window(root, 700, 500)
  root.resizable(False, False)

  # Tiêu đề
  lbl_title = tk.Label(root, text="Quản lý giáo viên phổ thông", font=("Arial", 18, "bold"))
  lbl_title.pack(pady=10)

  # Frame nhập thông tin
  frame_info = tk.Frame(root)
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

  # Bảng danh sách giáo viên
  lbl_ds = tk.Label(root, text="Danh sách giáo viên", font=("Arial", 10))
  lbl_ds.pack(pady=5, anchor="w", padx=10)

  columns = ("maso", "holot", "ten", "phai", "ngaysinh", "email")
  tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

  for col in columns:
    tree.heading(col, text=col.capitalize())

  tree.column("maso", width=60, anchor="center")
  tree.column("holot", width=150)
  tree.column("ten", width=100)
  tree.column("phai", width=70, anchor="center")
  tree.column("ngaysinh", width=100, anchor="center")
  tree.column("email", width=200)

  tree.pack(padx=10, pady=5, fill="both")

  root.mainloop()


if __name__ == "__main__":
  main()