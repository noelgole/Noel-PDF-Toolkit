import os
import tkinter as tk
from tkinter import ttk
import subprocess


class NoelsPDFToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("Noel's PDF Toolkit")
        self.root.configure(bg="#121212")
        self.center_window(600, 400)

        tk.Label(root, text="Noel's PDF Toolkit", fg="#f0c040", bg="#121212",
                 font=("Helvetica", 16, "bold")).pack(pady=20)

        # Buttons for each tool
        self.add_tool_button("Merge PDFs", "pdf_merge_app.py")
        self.add_tool_button("Merge PDFs in Folder", "merge_folder")
        self.add_tool_button("Reorder Pages", "pdf_reorder.py")
        self.add_tool_button("Shrink PDF", "pdf_shrink.py")
        self.add_tool_button("Delete Pages", "pdf_delete_pages.py")
        self.add_tool_button("Add Page Numbers", "pdf_add_page_numbers.py")

        # Exit Button
        exit_btn = tk.Button(root, text="Exit", command=self.show_thank_you_then_exit,
                             bg="#333333", fg="white", activebackground="#5c0000", activeforeground="white",
                             font=("Arial", 10), width=26, height=1)
        exit_btn.pack(pady=10)

    def show_thank_you_then_exit(self):
        try:
            thank_you_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "thank_you.png")
            if not os.path.exists(thank_you_path):
                raise FileNotFoundError("thank_you.png not found")

            splash = tk.Toplevel()
            splash.overrideredirect(True)
            splash.configure(bg="black")

            img = Image.open(thank_you_path)
            img = img.resize((600, 400), Image.Resampling.LANCZOS)
            self.thank_img = ImageTk.PhotoImage(img)

            label = tk.Label(splash, image=self.thank_img, bg="black")
            label.pack()

            # Center splash
            splash.update_idletasks()
            w = splash.winfo_width()
            h = splash.winfo_height()
            x = (splash.winfo_screenwidth() - w) // 2
            y = (splash.winfo_screenheight() - h) // 2
            splash.geometry(f"+{x}+{y}")

            # Close after 1 second and exit app
            splash.after(1000, lambda: (splash.destroy(), self.root.destroy()))
        except Exception as e:
            print("Exit screen error:", e)
            self.root.destroy()

    def center_window(self, w, h):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.minsize(w, h)

    def add_tool_button(self, label, script):
        btn = tk.Button(self.root, text=label, width=26, height=1,
                        bg="#333333", fg="white", activeforeground="white",
                        relief="flat", bd=0, highlightthickness=0,
                        font=("Arial", 10), command=lambda: self.launch_script(script))
        btn.pack(pady=5)

        # Round corners & hover effect
        def on_enter(e):
            btn.config(bg="#880000")

        def on_leave(e):
            btn.config(bg="#333333")

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.pack(pady=5)

    def merge_pdfs_in_folder(self):
        from tkinter import filedialog, messagebox
        from PyPDF2 import PdfMerger

        folder = filedialog.askdirectory(title="Select Folder Containing PDFs")
        if not folder:
            return

        pdf_files = sorted([f for f in os.listdir(folder) if f.lower().endswith(".pdf")])
        if not pdf_files:
            messagebox.showwarning("No PDFs Found", "No PDF files were found in the selected folder.")
            return

        merger = PdfMerger()
        for pdf in pdf_files:
            merger.append(os.path.join(folder, pdf))

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", title="Save Merged PDF")
        if not save_path:
            return

        merger.write(save_path)
        merger.close()

        messagebox.showinfo("Success", f"Merged PDF saved to:\n{save_path}")

    def launch_script(self, script_name):
        if script_name == "merge_folder":
            self.merge_pdfs_in_folder()
            return
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
        try:
            subprocess.Popen(["python", script_path])
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to launch {script_name}\n{e}")

class MergeWindow:
    def __init__(self, count):
        self.top = tk.Toplevel()
        self.top.title("Merge PDFs")
        self.top.configure(bg="#121212")
        self.center_window()

        self.file_paths = [None] * count
        self.labels = []

        tk.Label(self.top, text="Select PDFs to Merge", font=("Helvetica", 14, "bold"),
                 fg="#f0c040", bg="#121212").pack(pady=10)

        frame = tk.Frame(self.top, bg="#121212")
        frame.pack()

        for i in range(count):
            row = tk.Frame(frame, bg="#121212")
            row.grid(row=i, column=0, pady=5, padx=5)

            label = tk.Label(row, text="[Not selected]", bg="#121212", fg="white", width=40, anchor="w")
            label.grid(row=0, column=0, padx=3)
            self.labels.append(label)

            browse_btn = tk.Button(row, text="Browse", command=lambda idx=i: self.browse_file(idx),
                                   bg="#333333", fg="white", activebackground="#444444", activeforeground="white")
            browse_btn.grid(row=0, column=1, padx=3)

            remove_btn = tk.Button(row, text="Remove", command=lambda idx=i: self.remove_file(idx),
                                   bg="#333333", fg="white", activebackground="#444444", activeforeground="white")
            remove_btn.grid(row=0, column=2, padx=3)

        merge_btn = tk.Button(self.top, text="Merge PDF", command=self.merge_pdfs,
                              bg="#5c0000", fg="white", activebackground="#880000", activeforeground="white")
        merge_btn.pack(pady=20)

        self.status = tk.Label(self.top, text="", bg="#121212", fg="#ccc", font=("Arial", 9))
        self.status.pack()

        # Home button with icon only
        try:
            image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "home.png")
            if not os.path.exists(image_path):
                raise FileNotFoundError("home.png not found at: " + image_path)

            home_icon = Image.open(image_path)
            home_icon = home_icon.resize((30, 30), Image.Resampling.LANCZOS)
            self.home_img = ImageTk.PhotoImage(home_icon)

            home_btn = tk.Button(self.top, image=self.home_img, command=self.go_home,
                                 bg="#FFD700", borderwidth=0, activebackground="#FFD700")
            home_btn.pack(pady=10)
        except Exception as e:
            print("Home icon error:", e)
        except Exception as e:
            print("Home icon error:", e)

        self.top.mainloop()

    def center_window(self):
        self.top.update_idletasks()
        w, h = 500, 550
        x = (self.top.winfo_screenwidth() - w) // 2
        y = (self.top.winfo_screenheight() - h) // 2
        self.top.geometry(f"{w}x{h}+{x}+{y}")

    def browse_file(self, index):
        path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if path:
            self.file_paths[index] = path
            self.labels[index].config(text=os.path.basename(path))

    def remove_file(self, index):
        self.file_paths[index] = None
        self.labels[index].config(text="[Not selected]")

    def merge_pdfs(self):
        valid_files = [f for f in self.file_paths if f]
        if not valid_files:
            messagebox.showwarning("No PDFs", "Please select at least one file.")
            return

        merger = PdfMerger()
        for pdf in valid_files:
            merger.append(pdf)

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", title="Save Merged PDF")
        if not save_path:
            return

        merger.write(save_path)
        merger.close()

        size_mb = os.path.getsize(save_path) / (1024 * 1024)
        self.status.config(text=f"Saved to: {save_path} ({size_mb:.2f} MB)")
        messagebox.showinfo("Success", f"Merged PDF saved to:\n{save_path}\nSize: {size_mb:.2f} MB")

    def go_home(self):
        self.top.destroy()


class MergePDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Noel's PDF Merger")
        self.root.configure(bg="#121212")
        self.center_window(400, 200)

        tk.Label(root, text="Select number of PDFs to merge:", fg="white", bg="#121212",
                 font=("Arial", 12)).pack(pady=20)

        self.num_var = tk.StringVar()
        self.num_dropdown = ttk.Combobox(root, textvariable=self.num_var,
                                         values=[str(i) for i in range(2, 11)],
                                         state="readonly", width=5)
        self.num_dropdown.pack(pady=5)

        next_btn = tk.Button(root, text="Next", command=self.launch_merge_window,
                             bg="#333333", fg="white", activebackground="#5c0000", activeforeground="white")
        next_btn.pack(pady=20)

    def center_window(self, w, h):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def launch_merge_window(self):
        try:
            count = int(self.num_var.get())
            self.root.withdraw()
            MergeWindow(count)
        except ValueError:
            messagebox.showerror("Invalid Selection", "Please select a valid number.")


if __name__ == "__main__":
    main_root = tk.Tk()
    try:
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.ico")
        main_root.iconbitmap(icon_path)
    except Exception as e:
        print("App icon error:", e)
    app = MergePDFApp(main_root)
    main_root.mainloop()
class PDFReorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Noel's PDF Reorder Tool")
        self.set_geometry(500, 550)
        self.root.configure(bg="#121212")

        # Set custom .ico icon
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.ico")
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print("App icon error:", e)

        self.file_path = None
        self.style = ttk.Style()
        self.set_dark_theme()

        tk.Label(root, text="Reorder PDF Pages", font=("Helvetica", 18, "bold"), fg="#f0c040", bg="#121212").pack(pady=20)

        ttk.Button(root, text="Select PDF File", command=self.load_pdf).pack(pady=10)

        self.info_label = tk.Label(root, text="", bg="#121212", fg="white", font=("Arial", 10))
        self.info_label.pack()

        ttk.Button(root, text="Enter Page Order & Save", command=self.reorder_pdf).pack(pady=10)

        # Home and Close buttons
        btn_frame = tk.Frame(root, bg="#121212")
        btn_frame.pack(pady=20)

        try:
            home_icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "home.png")
            if not os.path.exists(home_icon_path):
                raise FileNotFoundError("home.png not found")
            home_icon = Image.open(home_icon_path)
            home_icon = home_icon.resize((30, 30), Image.Resampling.LANCZOS)
            self.home_img = ImageTk.PhotoImage(home_icon)
            home_btn = tk.Button(btn_frame, image=self.home_img, command=self.go_home,
                                 bg="#FFD700", borderwidth=0, activebackground="#FFD700")
            home_btn.pack(side="left", padx=10)
        except Exception as e:
            print("Home icon error:", e)


        self.status = tk.Label(root, text="", bg="#121212", fg="#ccc", font=("Arial", 9))
        self.status.pack(side="bottom", fill="x", pady=10)

    def set_geometry(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def set_dark_theme(self):
        self.style.theme_use("default")
        self.style.configure("TButton", background="#333", foreground="#f0f0f0", padding=6, font=("Arial", 10))
        self.style.map("TButton", background=[("active", "#5c0000")])

    def load_pdf(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.file_path:
            try:
                doc = fitz.open(self.file_path)
                self.total_pages = len(doc)
                self.info_label.config(text=f"Loaded: {os.path.basename(self.file_path)} ({self.total_pages} pages)")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load PDF: {str(e)}")

    def reorder_pdf(self):
        if not self.file_path:
            messagebox.showwarning("No File", "Please select a PDF file first.")
            return
        doc = fitz.open(self.file_path)
        order_input = simpledialog.askstring("New Page Order",
                                             f"Enter new order (1–{len(doc)}), e.g., 3,1,2 or 1-3,5:")
        if not order_input:
            return
        try:
            new_order = []
            for part in order_input.split(','):
                part = part.strip()
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    new_order.extend(range(start - 1, end))
                else:
                    new_order.append(int(part) - 1)

            new_doc = fitz.open()
            for i in new_order:
                new_doc.insert_pdf(doc, from_page=i, to_page=i)

            save_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                     filetypes=[("PDF Files", "*.pdf")],
                                                     title="Save Reordered PDF")
            if save_path:
                new_doc.save(save_path)
                self.status.config(text=f"Reordered PDF saved to: {save_path}")
                messagebox.showinfo("Success", f"Saved to:\n{save_path}")
            new_doc.close()
            doc.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_home(self):
        self.root.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    app = PDFReorderApp(root)
    root.mainloop()
class PDFDeletePagesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Noel's PDF Delete Tool")
        self.set_geometry(500, 550)
        self.root.configure(bg="#121212")

        # Set icon
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.ico")
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print("App icon error:", e)

        self.style = ttk.Style()
        self.set_dark_theme()

        tk.Label(root, text="Delete Pages from PDF", font=("Helvetica", 18, "bold"),
                 fg="#f0c040", bg="#121212").pack(pady=20)

        ttk.Button(root, text="Select PDF File", command=self.select_pdf).pack(pady=10)

        self.info_label = tk.Label(root, text="", bg="#121212", fg="white", font=("Arial", 10))
        self.info_label.pack()

        ttk.Button(root, text="Enter Pages to Delete", command=self.delete_pages).pack(pady=10)

        # Home & Close buttons
        btn_frame = tk.Frame(root, bg="#121212")
        btn_frame.pack(pady=20)

        try:
            home_icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "home.png")
            if os.path.exists(home_icon_path):
                home_icon = Image.open(home_icon_path)
                home_icon = home_icon.resize((30, 30), Image.Resampling.LANCZOS)
                self.home_img = ImageTk.PhotoImage(home_icon)
                home_btn = tk.Button(btn_frame, image=self.home_img, command=self.go_home,
                                     bg="#FFD700", borderwidth=0, activebackground="#FFD700")
                home_btn.pack(side="left", padx=10)
        except Exception as e:
            print("Home icon error:", e)



        self.status = tk.Label(root, text="", bg="#121212", fg="#ccc", font=("Arial", 9))
        self.status.pack(side="bottom", fill="x", pady=10)

        self.file_path = None

    def set_geometry(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def set_dark_theme(self):
        self.style.theme_use("default")
        self.style.configure("TButton", background="#333", foreground="#f0f0f0",
                             padding=6, font=("Arial", 10))
        self.style.map("TButton", background=[("active", "#5c0000")])

    def select_pdf(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.file_path:
            try:
                reader = PdfReader(self.file_path)
                total = len(reader.pages)
                self.info_label.config(text=f"Loaded: {os.path.basename(self.file_path)} ({total} pages)")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read PDF: {e}")

    def parse_page_range(self, input_str, total_pages):
        pages_to_delete = set()
        try:
            parts = input_str.split(",")
            for part in parts:
                part = part.strip()
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    pages_to_delete.update(range(start - 1, end))
                else:
                    pages_to_delete.add(int(part) - 1)
            return sorted(p for p in pages_to_delete if 0 <= p < total_pages)
        except Exception:
            return None

    def delete_pages(self):
        if not self.file_path:
            messagebox.showwarning("No File", "Please select a PDF file first.")
            return

        try:
            reader = PdfReader(self.file_path)
            total_pages = len(reader.pages)

            input_str = simpledialog.askstring("Delete Pages",
                f"Enter page numbers to delete (1–{total_pages}), e.g., 2,4-6:")
            if not input_str:
                return

            pages_to_delete = self.parse_page_range(input_str, total_pages)
            if pages_to_delete is None:
                messagebox.showerror("Invalid Input", "Invalid page range format.")
                return

            writer = PdfWriter()
            for i in range(total_pages):
                if i not in pages_to_delete:
                    writer.add_page(reader.pages[i])

            save_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                     title="Save PDF After Deletion",
                                                     filetypes=[("PDF Files", "*.pdf")])
            if not save_path:
                return

            with open(save_path, "wb") as f:
                writer.write(f)

            self.status.config(text=f"Saved to: {save_path}")
            messagebox.showinfo("Success", f"Saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Page deletion failed:\n{str(e)}")

    def go_home(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFDeletePagesApp(root)
    root.mainloop()
class PDFAddPageNumbersApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Noel's PDF Page Number Tool")
        self.set_geometry(500, 550)
        self.root.configure(bg="#121212")

        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.ico")
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print("App icon error:", e)

        self.style = ttk.Style()
        self.set_dark_theme()

        tk.Label(root, text="Add Page Numbers", font=("Helvetica", 18, "bold"),
                 fg="#f0c040", bg="#121212").pack(pady=20)

        ttk.Button(root, text="Select PDF File", command=self.select_pdf).pack(pady=10)

        tk.Label(root, text="Page Number Position:", bg="#121212", fg="white", font=("Arial", 10)).pack()

        self.position_var = tk.StringVar(value="bottom-center")
        ttk.Combobox(root, textvariable=self.position_var,
                     values=["bottom-left", "bottom-center", "bottom-right"],
                     state="readonly", width=20).pack(pady=5)

        ttk.Button(root, text="Add Page Numbers & Save", command=self.add_page_numbers).pack(pady=15)

        # Home & Close buttons
        btn_frame = tk.Frame(root, bg="#121212")
        btn_frame.pack(pady=20)

        try:
            home_icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "home.png")
            if os.path.exists(home_icon_path):
                home_icon = Image.open(home_icon_path)
                home_icon = home_icon.resize((30, 30), Image.Resampling.LANCZOS)
                self.home_img = ImageTk.PhotoImage(home_icon)
                home_btn = tk.Button(btn_frame, image=self.home_img, command=self.go_home,
                                     bg="#FFD700", borderwidth=0, activebackground="#FFD700")
                home_btn.pack(side="left", padx=10)
        except Exception as e:
            print("Home icon error:", e)



        self.status = tk.Label(root, text="", bg="#121212", fg="#ccc", font=("Arial", 9))
        self.status.pack(side="bottom", fill="x", pady=10)

        self.pdf_path = None

    def set_geometry(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def set_dark_theme(self):
        self.style.theme_use("default")
        self.style.configure("TButton", background="#333", foreground="#f0f0f0",
                             padding=6, font=("Arial", 10))
        self.style.map("TButton", background=[("active", "#5c0000")])

    def select_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_path:
            self.status.config(text=f"Selected: {os.path.basename(self.pdf_path)}")

    def create_numbered_overlay(self, page_num, total_pages, position, width, height):
        from io import BytesIO
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=(width, height))
        text = f"{page_num} / {total_pages}"
        x = {
            "bottom-left": inch * 0.5,
            "bottom-center": width / 2,
            "bottom-right": width - inch * 0.5
        }.get(position, width / 2)

        align = {
            "bottom-left": "left",
            "bottom-center": "center",
            "bottom-right": "right"
        }.get(position, "center")

        if align == "center":
            c.drawCentredString(x, 0.5 * inch, text)
        elif align == "left":
            c.drawString(x, 0.5 * inch, text)
        else:
            c.drawRightString(x, 0.5 * inch, text)

        c.showPage()
        c.save()
        buffer.seek(0)
        return PdfReader(buffer).pages[0]

    def add_page_numbers(self):
        if not self.pdf_path:
            messagebox.showwarning("No PDF", "Please select a PDF file.")
            return

        try:
            reader = PdfReader(self.pdf_path)
            writer = PdfWriter()
            total_pages = len(reader.pages)
            pos = self.position_var.get()

            for i, page in enumerate(reader.pages):
                width = float(page.mediabox.width)
                height = float(page.mediabox.height)
                overlay = self.create_numbered_overlay(i + 1, total_pages, pos, width, height)
                page.merge_page(overlay)
                writer.add_page(page)

            save_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                     title="Save Numbered PDF",
                                                     filetypes=[("PDF Files", "*.pdf")])
            if not save_path:
                return

            with open(save_path, "wb") as f:
                writer.write(f)

            self.status.config(text=f"Saved to: {save_path}")
            messagebox.showinfo("Success", f"Page numbers added and saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add page numbers:\n{str(e)}")

    def go_home(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFAddPageNumbersApp(root)
    root.mainloop()
class PDFShrinkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Noel's PDF Shrink Tool")
        self.set_geometry(500, 600)
        self.root.configure(bg="#121212")

        # Set icon
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.ico")
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print("App icon error:", e)

        self.style = ttk.Style()
        self.set_dark_theme()

        tk.Label(root, text="Shrink PDF", font=("Helvetica", 18, "bold"),
                 fg="#f0c040", bg="#121212").pack(pady=20)

        ttk.Button(root, text="Select PDF File", command=self.select_pdf).pack(pady=10)

        self.size_frame = tk.Frame(root, bg="#121212")
        self.size_frame.pack(pady=10)

        tk.Label(self.size_frame, text="Target Size:", fg="white", bg="#121212").grid(row=0, column=0, padx=5)
        self.size_var = tk.StringVar()
        self.size_entry = ttk.Entry(self.size_frame, textvariable=self.size_var, width=10)
        self.size_entry.grid(row=0, column=1)

        self.unit_var = tk.StringVar(value="MB")
        self.unit_dropdown = ttk.Combobox(self.size_frame, textvariable=self.unit_var,
                                          values=["MB", "KB"], width=5, state="readonly")
        self.unit_dropdown.grid(row=0, column=2, padx=5)

        # Compression quality (user-friendly)
        tk.Label(root, text="Compression Quality:", fg="white", bg="#121212", font=("Arial", 10)).pack()
        self.quality_map = {"Poor": "/screen", "Medium": "/ebook", "Best": "/prepress"}
        self.quality_label_var = tk.StringVar(value="Medium")
        ttk.Combobox(root, textvariable=self.quality_label_var,
                     values=list(self.quality_map.keys()), width=20, state="readonly").pack(pady=5)

        ttk.Button(root, text="Shrink & Save", command=self.shrink_pdf).pack(pady=10)

        # Home & Close buttons
        btn_frame = tk.Frame(root, bg="#121212")
        btn_frame.pack(pady=20)

        try:
            home_icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "home.png")
            if os.path.exists(home_icon_path):
                home_icon = Image.open(home_icon_path)
                home_icon = home_icon.resize((30, 30), Image.Resampling.LANCZOS)
                self.home_img = ImageTk.PhotoImage(home_icon)
                home_btn = tk.Button(btn_frame, image=self.home_img, command=self.go_home,
                                     bg="#FFD700", borderwidth=0, activebackground="#FFD700")
                home_btn.pack(side="left", padx=10)
        except Exception as e:
            print("Home icon error:", e)



        self.status = tk.Label(root, text="", bg="#121212", fg="#ccc", font=("Arial", 9))
        self.status.pack(side="bottom", fill="x", pady=10)

        self.input_path = None

    def set_geometry(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def set_dark_theme(self):
        self.style.theme_use("default")
        self.style.configure("TButton", background="#333", foreground="#f0f0f0",
                             padding=6, font=("Arial", 10))
        self.style.map("TButton", background=[("active", "#5c0000")])

    def select_pdf(self):
        self.input_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.input_path:
            self.status.config(text=f"Selected: {os.path.basename(self.input_path)}")

    def ghostscript_available(self):
        try:
            subprocess.run(["gs", "--version"], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, check=True)
            return True
        except Exception:
            return False

    def shrink_pdf(self):
        if not self.input_path:
            messagebox.showwarning("No PDF", "Please select a PDF file first.")
            return

        if not self.ghostscript_available():
            messagebox.showerror("Ghostscript Missing", "Ghostscript is not installed or not found in PATH.")
            return

        size_input = self.size_var.get().strip()
        if not size_input.isdigit():
            messagebox.showerror("Invalid Input", "Please enter a numeric target size.")
            return

        unit = self.unit_var.get()
        target_size = int(size_input)
        target_bytes = target_size * (1024 if unit == "KB" else 1024 * 1024)

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", title="Save Compressed PDF",
                                                   filetypes=[("PDF Files", "*.pdf")])
        if not output_path:
            return

        # Map quality label to Ghostscript setting
        quality_label = self.quality_label_var.get()
        gs_quality = self.quality_map.get(quality_label, "/ebook")

        # Ghostscript command
        gs_cmd = [
            "gs",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={gs_quality}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={output_path}",
            self.input_path
        ]

        try:
            subprocess.run(gs_cmd, check=True)
            final_size = os.path.getsize(output_path)
            size_in_unit = final_size / (1024 if unit == "KB" else 1024 * 1024)
            self.status.config(text=f"Saved to: {output_path} ({size_in_unit:.2f} {unit})")
            messagebox.showinfo("Success", f"Compressed and saved to:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Compression failed:\n{str(e)}")

    def go_home(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFShrinkApp(root)
    root.mainloop()


if __name__ == "__main__":
    import time
    from PIL import Image, ImageTk

    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.configure(bg="#121212")
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    width, height = 600, 400
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    splash.geometry(f"{width}x{height}+{x}+{y}")

    try:
        splash_img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
        splash_img = Image.open(splash_img_path).resize((600, 400), Image.Resampling.LANCZOS)
        splash_photo = ImageTk.PhotoImage(splash_img)
        splash_label = tk.Label(splash, image=splash_photo, bg="#121212")
        splash_label.pack()
    except Exception as e:
        splash_label = tk.Label(splash, text="Noel's PDF Toolkit", font=("Helvetica", 16), fg="white", bg="#121212")
        splash_label.pack(pady=50)

    splash.update()
    time.sleep(1)
    splash.destroy()

    root = tk.Tk()
    try:
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.ico")
        root.iconbitmap(icon_path)
    except Exception as e:
        print("App icon error:", e)
    app = NoelsPDFToolkit(root)
    root.mainloop()
