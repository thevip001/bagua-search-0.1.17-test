from pathlib import Path

p = Path('八卦搜索.user.js')
text = p.read_text(encoding='utf-8')

text = text.replace('@version      0.1.17', '@version      0.1.18')
text = text.replace('// 0.1.17 test build generated from 0.1.16.', '// 0.1.18 test build generated from 0.1.17.')
text = text.replace('直接拖拽执行内圈功能', '直接拖拽，执行搜索盘内圈功能')

p.write_text(text, encoding='utf-8')
