# def open_pdf():
#     file = filedialog.askopenfilename(title="Select a PDF", filetype=(  # type: ignore
#         ("PDF    Files", "*.pdf"), ("All Files", "*.*")))
#     if file:
#         # Open the PDF File
#         pdf_file = PyPDF2.PdfReader(file)
#         # Select a Page to read
#         page = pdf_file.pages[0]
#         # Get the content of the Page
#         content = page.extract_text()
#         # Add the content to TextBox
#         text.insert(1.0, content)


import fitz
from tkinter import *
from PIL import Image, ImageTk

file_name = input("Enter path to file: ")
doc = fitz.open(file_name)

zoom = 1
mat = fitz.Matrix(zoom, zoom)

num_pages = 0

for p in doc:
    num_pages += 1

root = Tk()
root.geometry('750x700')

# add scroll bar
scrollbar = Scrollbar(root)
scrollbar.pack(side = RIGHT, fill = Y)

# add canvas
canvas = Canvas(root, yscrollcommand = scrollbar.set)
canvas.pack(side = LEFT, fill = BOTH, expand = 1)

entry = Entry(root)
label = Label(root, text="Enter page number to display:")

def pdf_to_img(page_num):
    page = doc.load_page(page_num)
    pix = page.get_pixmap(matrix=mat)
    return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

def show_image():
    try:
        page_num = int(entry.get()) - 1
        assert page_num >= 0 and page_num < num_pages
        im = pdf_to_img(page_num)
        img_tk = ImageTk.PhotoImage(im)
        frame = Frame(canvas)
        panel = Label(frame, image=img_tk)
        panel.pack(side="bottom", fill="both", expand="yes")
        frame.image = img_tk
        canvas.create_window(0, 0, anchor='nw', window=frame)
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    except:
        pass



button = Button(root, text="Show Page", command=show_image)

label.pack(side=TOP, fill=None)
entry.pack(side=TOP, fill=BOTH)
button.pack(side=TOP, fill=None)

entry.insert(0, '1')
show_image()

scrollbar.config(command = canvas.yview)
root.mainloop()

doc.close()