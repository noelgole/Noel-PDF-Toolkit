# Noel's PDF Toolkit

A unified desktop utility for managing and editing PDF files

---

Table of Contents
1. Overview
2. Features
3. Installation
4. Usage
5. Building from Source
6. Troubleshooting
7. License

---

Overview
Noel's PDF Toolkit is a dark-themed, Windows desktop application that bundles multiple PDF utilities into a single executable. It provides a clean GUI for common PDF tasks:

- Merging multiple PDFs into one
- Merging all PDFs in a folder
- Reordering pages within a PDF
- Compressing (shrinking) PDFs using Ghostscript
- Deleting specific pages from a PDF
- Adding standalone page numbers to a PDF

Powered by Python, Tkinter, PyPDF2, ReportLab, and Ghostscript, this toolkit requires no manual scripting once installed. Simply run the .exe and select the desired tool.

---

Features

1. Merge PDFs
   - Select individual PDF files in any order and merge them into a single document.

2. Merge PDFs in Folder
   - Point to a folder and automatically merge all .pdf files inside.

3. Reorder Pages
   - Rearrange pages of a selected PDF by specifying new page orders.

4. Shrink PDF
   - Compress PDFs with selectable quality levels (Poor, Medium, Best) via Ghostscript settings (/screen, /ebook, /prepress).

5. Delete Pages
   - Remove unwanted pages by entering a comma-separated list or ranges (e.g., 1,3-5).

6. Add Page Numbers
   - Insert standalone numbers (1, 2, 3, …) at bottom-left, bottom-center, or bottom-right.

---

Installation

1. Download the latest noels_pdf_toolkit.exe from the project release.
2. Install Ghostscript (required for PDF compression):
   - Download from https://www.ghostscript.com/download/gsdnld.html and run the installer.
   - Ensure gswin64c.exe (or gs) is added to your system PATH.
3. (Optional) Bootstrap script
   - Run setup.bat as Administrator to install Python 3.10, Chocolatey, Ghostscript, and required Python packages.

---

Usage

1. Launch the Toolkit
   - Double-click noels_pdf_toolkit.exe. A splash screen will appear for 1 second, then the main window opens.

2. Select a Tool
   - Click any of the buttons:
     - Merge PDFs: choose individual files.
     - Merge PDFs in Folder: choose a directory.
     - Reorder Pages: select a file, enter page order.
     - Shrink PDF: select a file, choose size & quality.
     - Delete Pages: select a file, enter pages to remove.
     - Add Page Numbers: select a file, choose position, save.

3. Perform the Action
   - Follow on-screen dialogs to choose files and save the result.

4. Exit
   - Click Exit. A thank_you.png splash displays for 1 second before closing.

---

Building from Source

If you wish to modify or rebuild the toolkit:

1. Prerequisites
   - Python 3.10+ (https://www.python.org/downloads/)
   - Ghostscript (https://www.ghostscript.com/)
   - pip packages:
     pip install PyPDF2 reportlab pillow pyinstaller

2. Clone or copy the repo into a folder.

3. Run PyInstaller (in the project root):
   pyinstaller --noconfirm --onefile --windowed --icon=logo.ico --add-data "logo.ico;." --add-data "logo.png;." --add-data "home.png;." --add-data "thank_you.png;." --hidden-import fitz --hidden-import reportlab.pdfgen --hidden-import pdf_merge_app --hidden-import pdf_reorder --hidden-import pdf_shrink --hidden-import pdf_delete_pages --hidden-import pdf_add_page_numbers noels_pdf_toolkit.py

4. The standalone noels_pdf_toolkit.exe will appear in the dist/ folder.

---

Troubleshooting

- Ghostscript Missing:
  - Ensure Ghostscript is installed and gswin64c.exe is on your PATH.
  - Test by running gswin64c --version in a new terminal.

- Tools Not Launching:
  - Verify you have the latest .exe with all hidden imports.
  - Run from a command prompt to see any error messages.

- UI Doesn’t Appear:
  - Make sure you haven’t renamed any .py modules after building.
  - Check noels_pdf_toolkit.spec for missing data entries.

---

License

This project is open-source under the MIT License. Feel free to modify and distribute as needed.
