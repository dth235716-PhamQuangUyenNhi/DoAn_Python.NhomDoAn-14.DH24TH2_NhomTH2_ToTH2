import tkinter as tk
from tkinter import ttk, messagebox

# căn giữa cửa sổ
def center_window(win, w=300, h=600):
  ws = win.winfo_screenwidth()
  hs = win.winfo_screenheight()
  x = (ws // 2) - (w // 2)
  y = (hs // 2) - (h // 2)
  win.geometry(f'{w}x{h}+{x}+{y}')

def main():
  trangchu = tk.Tk()
  trangchu.title("Đăng nhập hệ thống")
  center_window(trangchu, 600, 300)
  trangchu.resizable(False, False)

  trangchu.mainloop()

if __name__ == "__main__":
    main()