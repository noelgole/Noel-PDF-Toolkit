# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['noels_pdf_toolkit.py'],
    pathex=[],
    binaries=[],
    datas=[('logo.ico', '.'), ('logo.png', '.'), ('home.png', '.'), ('thank_you.png', '.')],
    hiddenimports=['fitz', 'reportlab.pdfgen', 'pdf_merge_app', 'pdf_reorder', 'pdf_shrink', 'pdf_delete_pages', 'pdf_add_page_numbers'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='noels_pdf_toolkit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['logo.ico'],
)
