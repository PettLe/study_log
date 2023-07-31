# -*- mode: python -*-
import os

block_cipher = None

current_dir = os.path.dirname(os.path.curdir)

a = Analysis(['main.py'],
             # pathex=['output_path'],
             pathex=[current_dir],
             binaries=[],
             datas=[
                 ('*.db', 'databases')
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          Tree('C:/Users/Pete/Documents/KOODAUSPROJEKTIT/study_log'),
          name='Kaisan Study Log',
          debug=False,
          strip=False,
          upx=True,
          console=False)