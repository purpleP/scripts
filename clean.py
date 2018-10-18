import re
import sys

from difflib import SequenceMatcher
from subprocess import check_output


file, pattern = sys.argv[1], bytes(sys.argv[2], 'utf8')
index_version = check_output(['git', 'show', f':{file}'])
with open(file, 'rb+') as f:
    current = bytearray(f.read())
    matcher = SequenceMatcher(a=index_version, b=current)
    for tag, i1, i2, j1, j2 in reversed(matcher.get_opcodes()):
        if tag in {'insert', 'replace'}:
            for m in re.finditer(pattern, current[j1:j2]):
                del current[j1 + m.start():j1 + m.end()]
    f.seek(0)
    f.write(current)
    f.truncate()
