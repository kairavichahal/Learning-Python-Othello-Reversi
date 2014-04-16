# -*- mode: python -*-
a = Analysis(['othello.py'],
             pathex=['/Users/Kairavi/Documents/Carnegie Mellon University/Coursework/2.3/Fundamentals of Programming/Othello'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='othello',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='othello')
