import re
import sys

from difflib import SequenceMatcher
from subprocess import check_output


(*files, revision), pattern = sys.argv[1:-1], bytes(sys.argv[-1], 'utf8')

for file in files:
    try:
        index_version = check_output(['git', 'show', f'{revision}:{file}'])
    except:
        index_version = ''
    with open(file, 'rb+') as f:
        current = bytearray(f.read())
        matcher = SequenceMatcher(a=index_version, b=current)
        for tag, i1, i2, j1, j2 in reversed(matcher.get_opcodes()):
            if tag in {'insert', 'replace'}:
                for m in reversed([*re.finditer(pattern, current[j1:j2])]):
                    del current[j1 + m.start():j1 + m.end()]
        f.seek(0)
        f.write(current)
        f.truncate()
