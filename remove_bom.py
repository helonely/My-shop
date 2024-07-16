with open('catalog.json', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Удаление BOM, если оно присутствует
if content.startswith(u'\ufeff'):
    content = content[1:]

with open('catalog.json', 'w', encoding='utf-8') as f:
    f.write(content)
