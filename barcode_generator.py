import os
import tempfile
from subprocess import Popen
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import barcode
from barcode.writer import ImageWriter

tmp_path = 'BarcodeGenerator.png'


def generate_barcode(event):
    global tmp_path
    delete_temp_image()
    barcode_txt = ent_barcode_txt.get()
    code_type = ent_code_type.get()
    if len(barcode_txt) is 0:
        notify('Nothing to do')
        return
    print(f'Code type: {code_type}')
    print(f'Text to generate: {barcode_txt}')
    b_class = barcode.get_barcode_class(code_type)
    iw = ImageWriter()
    iw.set_options({'dpi': 140})
    try:
        bar = b_class(str(barcode_txt), writer=iw)
        notify('Format success')
    except (barcode.errors.WrongCountryCodeError,
            barcode.errors.BarcodeError,
            barcode.errors.BarcodeNotFoundError,
            barcode.errors.IllegalCharacterError,
            barcode.errors.NumberOfDigitsError,
            ValueError) as e:
        return notify(str(e))
    path = os.path.join(tempfile.gettempdir(), barcode_txt)
    tmp_path = bar.save(path, text=barcode_txt)
    print(f'temporary image: {tmp_path}')


def delete_temp_image():
    global tmp_path
    if tmp_path == 'BarcodeGenerator.png':
        return
    os.remove(tmp_path)
    tmp_path = 'BarcodeGenerator.png'


def preview_image():
    tmp_img = PhotoImage(file=tmp_path)
    pnl_image.config(image=tmp_img)
    pnl_image.image = tmp_img
    pnl_image.after(200, preview_image)


def open_image(event=None):
    os_name = os.name
    if os_name == 'nt':
        try:
            Popen(['mspaint', tmp_path])
        except (FileNotFoundError, NameError):
            notify('MS Paint not found')
    elif os_name == 'posix':
        # for Ubuntu maybe others
        try:
            Popen(['shotwell', tmp_path])
        except (FileNotFoundError, NameError):
            notify('Shotwell not found')


def save_image(event=None):
    file = filedialog.asksaveasfile(
        mode="wb", title="Save Image", defaultextension=".png",
        initialfile=tmp_path.split(os.sep)[-1],
        filetypes=(("png files", "*.png"), ("all files", "*.*")))
    if file:
        try:
            image = open(tmp_path, 'rb').read()
            file.write(image)
            file.close()
            notify('Image saved')
        except AttributeError as e:
            notify(str(e))


def notify(string='Press Enter to generate barcode'):
    lbl_notify.config(text=string)


master = Tk()

lbl_barcode_txt = Label(master, text='Text to Generate')
lbl_barcode_txt.place(x=100, y=10)

ent_barcode_txt = Entry(master)
ent_barcode_txt.bind('<Return>', generate_barcode)
ent_barcode_txt.place(x=80, y=40)
ent_barcode_txt.focus()

lbl_code_type = Label(master, text='Format')
lbl_code_type.place(x=360, y=10)

ent_code_type = ttk.Combobox(master, values=barcode.PROVIDED_BARCODES)
ent_code_type.config(width=12)
ent_code_type.place(x=330, y=40)
ent_code_type.current(0)

lbl_preview = Label(master, text='Preview')
lbl_preview.place(x=240, y=180)

img = PhotoImage(file=tmp_path)
pnl_image = Label(master, image=img)
pnl_image.place(x=220, y=130)

lbl_notify = Label(master, text='None')
lbl_notify.place(x=5, y=290)

btn_open = Button(master, text='Open', command=open_image)
btn_open.bind('<Return>', open_image)
btn_open.config(width=10)
btn_open.place(x=60, y=120)

btn_save = Button(master, text='Save', command=save_image)
btn_save.bind('<Return>', save_image)
btn_save.config(width=10)
btn_save.place(x=60, y=190)

master.iconbitmap(r'icon.ico')
master.wm_title("BarcodeGenerator")
master.geometry("540x320")
preview_image()
notify()
master.mainloop()
delete_temp_image()
