import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
#from PIL import Image, ImageTk
import form_trangchu


def center_window(win, w=700, h=500):
  ws = win.winfo_screenwidth()
  hs = win.winfo_screenheight()
  x = (ws // 2) - (w // 2)
  y = (hs // 2) - (h // 2)
  win.geometry(f'{w}x{h}+{x}+{y}')


#def upload_image():
#  """Chọn ảnh 4x6"""
#  path = filedialog.askopenfilename(
#    filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
#  )
#  if path:
#   img = Image.open(path)
#   img = img.resize((20, 130))  # Kích thước ảnh trong label
#   photo = ImageTk.PhotoImage(img)
#   image_label.config(image=photo)
#   image_label.image = photo



def main():
  ttgv = tk.Tk()
  ttgv.title("Quản lý giáo viên phổ thông")
  center_window(ttgv, 800, 700)
  ttgv.resizable(False, False)

  # Tiêu đề
  lbl_title = tk.Label(ttgv, text="SƠ YẾU LÍ LỊCH", font=("Arial", 18, "bold"))
  lbl_title.pack(pady=10)

  # Frame chính chứa 2 cột
  frm = tk.Frame(ttgv)
  frm.pack(pady=10)

  # Cột trái: Ảnh
  left = tk.Frame(frm)
  left.grid(row=0, column=0, padx=20)

  tk.Label(left, text="Ảnh màu\n(4 x 6 cm)", font=("Times New Roman", 12)).pack()
  image_label = tk.Label(left, width=20, height=12, bg="white", relief="solid")
  image_label.pack(pady=5)

  #tk.Button(left, text="Tải ảnh lên", command=upload_image).pack(pady=5)

  # Cột phải: Thông tin giáo viên
  right = tk.Frame(frm)
  right.grid(row=0, column=1, sticky="w")

  labels = [
    "1) Họ và tên khai sinh:",
    "Giới tính:",
    "3) Sinh ngày:",
    "5) Quê quán:",
    "6) Dân tộc:",
    "7) Tôn giáo:",
    "8) Số CCCD:",
    "SĐT liên hệ:",
    "9) Email:",
    "11) Chuyên ngành đào tạo:",
    "12) Trang thái công tác:",
    "13) Nơi công tác:"
  ]

   # Hàm thoát về form_trangchu
  def thoat_action():
        ttgv.destroy()  # đóng cửa sổ hiện tại
        form_trangchu.main()

  # Frame chứa nút
  frame_buttons = tk.Frame(ttgv)
  frame_buttons.pack(side=tk.BOTTOM, pady=25)
  # Nút sửa
  btn_tim = tk.Button(frame_buttons, text="Chỉnh sửa", width=10, command = thoat_action)
  btn_tim.pack(side= 'left', padx=10)
  # Nút lưu
  btn_tim = tk.Button(frame_buttons, text="Lưu", width=10, command = thoat_action)
  btn_tim.pack(side= 'left', padx=10)
  # Nút thoát
  btn_thoat = tk.Button(frame_buttons, text="Thoát", width=10, command = thoat_action)
  btn_thoat.pack(side= 'left', padx=10)

  ttgv.mainloop()

if __name__ == "__main__":
    main()
  