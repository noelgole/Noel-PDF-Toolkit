import os
import io
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image, ImageTk

class PDFAddPageNumbersApp:
    def __init__(self, root):
        """
        root: a tk.Tk() or tk.Toplevel() onto which the UI will be built
        """
        self.root = root
        self.root.title("Noel's PDF Page Numbering")
        self._center_window(500, 600)
        self.root.configure(bg="#121212")

        # set icon if available
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "logo.ico")
            self.root.iconbitmap(icon_path)
        except:
            pass

        # Style buttons
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TButton",
                        background="#333", foreground="#f0f0f0",
                        padding=6, font=("Arial", 10))
        style.map("TButton", background=[("active", "#5c0000")])

        # Header
        tk.Label(self.root,
                 text="Add Page Numbers",
                 font=("Helvetica", 18, "bold"),
                 fg="#f0c040", bg="#121212")\
          .pack(pady=20)

        # Select PDF button
        ttk.Button(self.root,
                   text="Select PDF",
                   command=self._select_pdf)\
           .pack(pady=10)

        # Position dropdown
        self.position_var = tk.StringVar(value="bottom-center")
        ttk.Label(self.root,
                  text="Position:",
                  background="#121212",
                  foreground="white")\
           .pack(pady=(10,0))
        ttk.Combobox(self.root,
                     textvariable=self.position_var,
                     values=["bottom-left", "bottom-center", "bottom-right"],
                     state="readonly",
                     width=15)\
           .pack(pady=5)

        # Add & Save button
        ttk.Button(self.root,
                   text="Add & Save",
                   command=self.add_page_numbers)\
           .pack(pady=10)

        # Home/Exit icon
        try:
            img = Image.open(os.path.join(os.path.dirname(__file__), "home.png"))
            img = img.resize((30, 30), Image.Resampling.LANCZOS)
            self.home_photo = ImageTk.PhotoImage(img)
            tk.Button(self.root,
                      image=self.home_photo,
                      command=self.root.destroy,
                      bg="#FFD700",
                      borderwidth=0)\
              .pack(pady=10)
        except:
            pass

        # Status bar
        self.status = tk.Label(self.root,
                               text="",
                               fg="#ccc",
                               bg="#121212")
        self.status.pack(side="bottom", fill="x", pady=10)

        # Internal state
        self.pdf_path = None

    def _center_window(self, width, height):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _select_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF Files","*.pdf")])
        if path:
            self.pdf_path = path
            self.status.config(text=os.path.basename(path))

    def _create_overlay(self, page_num, position, w, h):
        """
        Create a single-page PDF overlay with just the page number.
        position: 'bottom-left' | 'bottom-center' | 'bottom-right'
        w, h: dimensions of the page in points
        """
        buf = BytesIO()
        c = canvas.Canvas(buf, pagesize=(w, h))

        text = str(page_num)
        font_name = "Helvetica"
        font_size = 12
        c.setFont(font_name, font_size)
        text_width = c.stringWidth(text, font_name, font_size)

        margin = 0.75 * inch  # 0.75" above bottom and from sides

        pos = position.replace("_", "-").lower()
        if pos == "bottom-left":
            x = margin
        elif pos == "bottom-right":
            x = w - margin - text_width
        else:  # bottom-center
            x = (w - text_width) / 2

        y = margin

        c.drawString(x, y, text)
        c.save()
        buf.seek(0)

        return PdfReader(buf).pages[0]

    def add_page_numbers(self):
        if not self.pdf_path:
            messagebox.showwarning("No PDF", "Please select a PDF first.")
            return

        try:
            reader = PdfReader(self.pdf_path)
            writer = PdfWriter()
            pos = self.position_var.get()

            for idx, page in enumerate(reader.pages, start=1):
                w = float(page.mediabox.width)
                h = float(page.mediabox.height)
                overlay = self._create_overlay(idx, pos, w, h)
                page.merge_page(overlay)
                writer.add_page(page)

            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                title="Save Numbered PDF",
                filetypes=[("PDF Files","*.pdf")]
            )
            if not save_path:
                return

            with open(save_path, "wb") as f:
                writer.write(f)

            self.status.config(text=os.path.basename(save_path))
            messagebox.showinfo("Success",
                                f"Page numbers added and saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add page numbers:\n{e}")

if __name__ == "__main__":
    # Standalone mode (if you ever run this file directly)
    root = tk.Tk()
    app = PDFAddPageNumbersApp(root)
    root.mainloop()
