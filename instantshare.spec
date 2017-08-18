# -*- mode: python -*-

block_cipher = None

hidden_imports = ['cli.audio', 
                  'cli.file', 
                  'cli.gui', 
                  'cli.screen', 
                  'cli.text', 
                  'cli.video',
                  'screenshot.snippingtool',
                  'screenshot.windows_tk',
                  'screenshot.gnome_screenshot',
                  'storage.dropbox',
                  'storage.googledrive',
                  'storage.imgur',
                  'storage.owncloud',
                  'storage.pastebin',
                  'storage.sftp',
                  'storage.twitter_intent']

added_files = [('src/res', 'res')]

a = Analysis(['src\\instantshare'],
             pathex=['C:\\Developer\\instantshare'],
             binaries=[],
             datas=added_files,
             hiddenimports=hidden_imports,
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
          exclude_binaries=True,
          name='instantshare',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='instantshare')
