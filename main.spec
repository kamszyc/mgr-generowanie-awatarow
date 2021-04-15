# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['D:\\magisterka\\kody\\mgr-generowanie-avatarow'],
             binaries=[],
             datas=[],
             hiddenimports=['models.test_model', 'models.cut_model', 'models.cycle_gan_model', 'models.pix2pix_model', 'models.attention_gan_model',
              'data.aligned_dataset', 'data.single_dataset', 'data.single_image_rembg_dataset', 'data.unaligned_dataset'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += Tree('./checkpoints', prefix='checkpoints')
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
