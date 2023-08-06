#!C:\Users\bbara\.conda\envs\muse-lsl\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'uvicmuse==2.0.0','console_scripts','uvicmuse'
__requires__ = 'uvicmuse==2.0.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('uvicmuse==2.0.0', 'console_scripts', 'uvicmuse')()
    )
