# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['pyqt_main.py'],
    pathex=[],
    binaries=[],
    datas=[('edid_main.py', '.'), ('monitor_info.py', '.'), ('product_name.py', '.'), ('fonts/embedded_fonts.py', 'fonts')],
    hiddenimports=['PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('O', None, 'OPTION'), ('O', None, 'OPTION')],
    name='EDID Reader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon=['C:\\Users\\px1903\\Desktop\\自製工具\\EDID_read_raw\\icon\\moni.ico'],
)
