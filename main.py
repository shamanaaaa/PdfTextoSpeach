import os
import tkinter as tk
from tkinter import filedialog as fd, END
import convert_pdf_to_text
from tkinter import messagebox, INSERT
from natsort import natsorted
import Mp3ToText


def readFile(filename):
    f = open(filename, "r")
    text = f.read()
    return text


def writeFile(filename, text):
    with open(filename, "w") as text_file:
        text_file.write(text)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.current_page = ""
        self.current_pdf = ""
        self.open_file = tk.Button(self)
        self.left = tk.Button(self)
        self.left = tk.Button(self, text="PAGE LEFT", command=self.go_left)
        self.right = tk.Button(self)
        self.right = tk.Button(self, text="PAGE RIGHT", command=self.go_right)
        self.play = tk.Button(self)
        self.play = tk.Button(self, text="PLAY", command=self.play_text)
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.text = tk.Text(width=128, height=60)
        self.master = master
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.open_file["text"] = "OPEN PDF"
        self.open_file["command"] = self.open_pdf
        self.open_file.grid(row=0, column=0)
        self.quit.grid(row=0, column=4)
        self.left.grid(row=0, column=1)
        self.text.grid(row=2, column=0)
        self.right.grid(row=0, column=2)
        self.play.grid(row=0, column=3)

    def open_pdf(self):
        file_types = [('PDF files', '*.pdf')]
        dlg = fd.Open(self, filetypes=file_types)
        pdf_file = dlg.show()
        # extract PDF to txt pages one by one in PDF name directory
        pdf_name = ((pdf_file.split("/")[-1]).split(".")[0])
        try:
            os.mkdir("PDF_FILES/" + pdf_name)
            total_pages = (convert_pdf_to_text.total_pages(pdf_file))
            for page in range(1, total_pages + 1):
                pdf_text = convert_pdf_to_text.convert_pdf_to_txt(pdf_file, page)
                writeFile(f"PDF_FILES/{pdf_name}/{page}.txt", pdf_text)
        except FileExistsError:
            messagebox.showinfo("Warning", "File exists, opening file")
        self.current_pdf = pdf_name
        self.current_page = natsorted(os.listdir(f"PDF_FILES/{pdf_name}/"))[0]
        with open(f"PDF_FILES/{self.current_pdf}/{self.current_page}", 'r') as f:
            self.text.insert(INSERT, f.read())

    def go_right(self, counter=0):
        try:
            file_list = natsorted(os.listdir(f"PDF_FILES/{self.current_pdf}"))
            next_index = file_list.index(self.current_page) + 1 + counter
            if next_index == 0 or next_index == len(file_list):
                return None
            file = file_list[next_index]
            with open(f"PDF_FILES/{self.current_pdf}/{file}", 'r') as f:
                self.text.delete('1.0', END)
                self.text.insert(INSERT, f.read())
                self.current_page = file
        except ValueError:
            messagebox.showinfo("Warning", "Please open PDF file first.")

    def go_left(self):
        self.go_right(counter=-2)

    def play_text(self):
        play_text = readFile(f"PDF_FILES/{self.current_pdf}/{self.current_page}")
        Mp3ToText.mp3_convert(play_text)


root = tk.Tk()
root.geometry("1024x768")
app = Application(master=root)
app.mainloop()
