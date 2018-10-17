import re
import sys

from difflib import SequenceMatcher
from subprocess import check_output


_, file, pattern = sys.argv
index_version = check_output(['git', 'show', f':{file}'])
with open(file, 'rb+') as f:
    current = bytearray(f.read())
    m = SequenceMatcher(a=index_version, b=current)
    for tag, i1, i2, j1, j2 in reversed(m.get_opcodes()):
        if tag in {'insert', 'replace'}:
            for m in re.finditer(bytes(pattern, 'utf8'), current[j1:j2]):
                del current[j1 + m.start():j1 + m.end()]
    f.seek(0)
    f.write(current)
    f.truncate()
