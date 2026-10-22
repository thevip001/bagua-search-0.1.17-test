from pathlib import Path

src = Path('source/八卦搜索.user.js')
out = Path('八卦搜索.user.js')
text = src.read_text(encoding='utf-8')
text = text.replace('@version      0.1.16', '@version      0.1.17')
marker = '// 0.1.17 test build generated from 0.1.16.'
if marker not in text:
    text = marker + '\n' + text
out.write_text(text, encoding='utf-8')
