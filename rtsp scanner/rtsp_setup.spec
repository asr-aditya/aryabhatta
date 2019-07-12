# -*- mode: python -*-

block_cipher = None


a = Analysis(['rtsp_setup.py'],
             pathex=['C:\\Users\\Aditya Singh Rathore\\Videos\\setup\\rtsp scanner'],
             binaries=[],
             datas=[('C:\\Users\\Aditya Singh Rathore\\AppData\\Local\\Programs\\Python\\Python37-32\\Lib\\site-packages\\cv2\\opencv_ffmpeg410.dll', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='rtsp_setup',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
