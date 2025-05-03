import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

class PDFShrinkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Noel's PDF Shrink Tool")
        self.set_geometry(500, 600)
        self.root.configure(bg="#121212")
        # App icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "logo.ico")
            self.root.iconbitmap(icon_path)
        except:
            pass

        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("TButton", background="#333", foreground="#f0f0f0",
                             padding=6, font=("Arial", 10))
        self.style.map("TButton", background=[("active", "#5c0000")])

        tk.Label(root, text="Shrink PDF", font=("Helvetica", 18, "bold"),
                 fg="#f0c040", bg="#121212").pack(pady=20)

        ttk.Button(root, text="Select PDF File", command=self.select_pdf).pack(pady=10)
        frame = tk.Frame(root, bg="#121212"); frame.pack(pady=10)
        tk.Label(frame, text="Target Size:", fg="white", bg="#121212").grid(row=0, column=0)
        self.size_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.size_var, width=8).grid(row=0, column=1, padx=5)
        self.unit_var = tk.StringVar(value="MB")
        ttk.Combobox(frame, textvariable=self.unit_var, values=["MB","KB"],
                     state="readonly", width=5).grid(row=0, column=2)

        tk.Label(root, text="Compression Quality:", fg="white", bg="#121212").pack()
        self.quality_map = {"Poor":"/screen","Medium":"/ebook","Best":"/prepress"}
        self.quality_var = tk.StringVar(value="Medium")
        ttk.Combobox(root, textvariable=self.quality_var,
                     values=list(self.quality_map), state="readonly").pack(pady=5)

        ttk.Button(root, text="Shrink & Save", command=self.shrink_pdf).pack(pady=10)

        btn_frame = tk.Frame(root, bg="#121212"); btn_frame.pack(pady=20)
        try:
            home_img = Image.open(os.path.join(os.path.dirname(__file__),"home.png"))
            home_img = home_img.resize((30,30), Image.Resampling.LANCZOS)
            self.home_photo = ImageTk.PhotoImage(home_img)
            tk.Button(btn_frame, image=self.home_photo, command=root.destroy,
                      bg="#FFD700", borderwidth=0).pack(side="left", padx=10)
        except:
            pass

        self.status = tk.Label(root, text="", fg="#ccc", bg="#121212")
        self.status.pack(side="bottom", fill="x", pady=10)
        self.input_path = None

    def set_geometry(self, w, h):
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x, y = (sw-w)//2, (sh-h)//2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def select_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF Files","*.pdf")])
        if path:
            self.input_path = path
            self.status.config(text=os.path.basename(path))

    def shrink_pdf(self):
        if not self.input_path:
            messagebox.showwarning("No PDF","Please select a PDF first.")
            return

        # find Ghostscript
        gs = next((shutil.which(x) for x in ("gs","gswin64c","gswin32c") if shutil.which(x)), None)
        if not gs:
            messagebox.showerror("Ghostscript Missing",
                "Ghostscript not found—install it and add its bin folder to your PATH.")
            return

        size = self.size_var.get().strip()
        if not size.isdigit():
            messagebox.showerror("Invalid Size","Enter a numeric target size.")
            return

        unit = self.unit_var.get()
        quality = self.quality_map.get(self.quality_var.get(), "/ebook")
        out_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                filetypes=[("PDF Files","*.pdf")])
        if not out_path:
            return

        cmd = [
            gs,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={quality}",
            "-dNOPAUSE","-dBATCH","-dQUIET",
            f"-sOutputFile={out_path}",
            self.input_path
        ]
        try:
            subprocess.run(cmd, check=True)
            final = os.path.getsize(out_path)
            val = final/(1024 if unit=="KB" else 1024*1024)
            self.status.config(text=f"Saved: {os.path.basename(out_path)} ({val:.2f} {unit})")
            messagebox.showinfo("Success","PDF compressed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Compression failed:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFShrinkApp(root)
    root.mainloop()
