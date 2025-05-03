import os
import tkinter as tk
from tkinter import ttk
import subprocess
import pdf_merge_app
import pdf_reorder
import pdf_shrink
import pdf_delete_pages
import pdf_add_page_numbers

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

        # map each button target to (module_name, class_name)
        mapping = {
            "pdf_merge_app.py": ("pdf_merge_app", "MergePDFApp"),
            "pdf_reorder.py": ("pdf_reorder", "PDFReorderApp"),
            "pdf_shrink.py": ("pdf_shrink", "PDFShrinkApp"),
            "pdf_delete_pages.py": ("pdf_delete_pages", "PDFDeletePagesApp"),
            "pdf_add_page_numbers.py": ("pdf_add_page_numbers", "PDFAddPageNumbersApp"),
        }

        if script_name not in mapping:
            tk.messagebox.showerror("Error", f"Unknown tool: {script_name}")
            return

        mod_name, class_name = mapping[script_name]
        try:
            module = __import__(mod_name, fromlist=[class_name])
            ToolClass = getattr(module, class_name)
            win = tk.Toplevel(self.root)
            ToolClass(win)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to launch {script_name}:\n{e}")




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
