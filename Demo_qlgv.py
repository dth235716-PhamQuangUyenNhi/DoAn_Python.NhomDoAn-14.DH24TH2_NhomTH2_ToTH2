import tkinter as tk
def center_window(win, w=800, h=600):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

  # Cửa sổ chính
root = tk.Tk()
root.title("Quản lý giáo viên phổ thông")
center_window(root,800,600)
root.resizable(False, False)

    # Tiêu đề  
lbl_title = tk.Label(root, text="Quản lý giáo viên phổ thông", font=("Arial",18, "bold"))
lbl_title.pack(pady=10)

  # Frame nhập thông tin
frame_info = tk.Frame(root)
frame_info.pack(pady=5, padx=10, fill="x")

tk.Label(frame_info,  text="Mã số").grid(row=0,  column=0,  padx=5,  pady=5, sticky="w")
entry_maso = tk.Entry(frame_info, width=10)
entry_maso.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info,  text="Email").grid(row=0,  column=2,  padx=5,  pady=5, sticky="w")
entry_email = tk.Entry(frame_info, width=30)
entry_email.grid(row=0, column=3, padx=5, pady=5, sticky="w")

tk.Label(frame_info,  text="Họ lót").grid(row=1,  column=0,  padx=5,  pady=5, sticky="w")
entry_holot = tk.Entry(frame_info, width=25)    
entry_holot.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info,  text="Tên").grid(row=1,  column=2,  padx=5,  pady=5, sticky="w")
entry_ten = tk.Entry(frame_info, width=15)  
entry_ten.grid(row=1, column=3, padx=5, pady=5, sticky="w")

tk.Label(frame_info,  text="Phái").grid(row=2,  column=0,  padx=5,  pady=5, sticky="w")
gender_var = tk.StringVar(value="Nam")
tk.Radiobutton(frame_info, text="Nam", variable=gender_var, value="Nam").grid(row=2, column=1, padx=5, sticky="w")
tk.Radiobutton(frame_info, text="Nữ", variable=gender_var, value="Nữ").grid(row=2, column=1, padx=60, sticky="w")  






                

<<<<<<< HEAD
root.mainloop()
=======
root.mainloop()
>>>>>>> 72b056b1981dea40956e5d080f1abf9ae7ecad94
