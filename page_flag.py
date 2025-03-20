from PIL import Image, ImageDraw, ImageFont

# Увеличиваем размер изображения
image = Image.new('RGB', (1100, 1300), color=(255, 255, 255))
draw = ImageDraw.Draw(image)

# Загружаем шрифты
try:
    title_font = ImageFont.truetype("arial.ttf", 24)  # Шрифт для заголовков
    text_font = ImageFont.truetype("arial.ttf", 18)   # Шрифт для основного текста
    table_font = ImageFont.truetype("arial.ttf", 16)  # Шрифт для таблицы
except IOError:
    title_font = ImageFont.load_default()  # Используем шрифт по умолчанию, если Arial недоступен
    text_font = ImageFont.load_default()
    table_font = ImageFont.load_default()

# Параметры текста
title_color = (0, 0, 0)  # Черный цвет для заголовков
text_color = (50, 50, 50)  # Темно-серый цвет для текста
y_text = 30

# Добавляем заголовок "Цены на печать" по центру
title_text = "Цены на печать"
bbox = draw.textbbox((0, 0), title_text, font=title_font)
text_width = bbox[2] - bbox[0]
text_x = (image.width - text_width) // 2  # Центрируем заголовок
draw.text((text_x, y_text), title_text, font=title_font, fill=title_color)
y_text += 50  # Увеличиваем отступ после заголовка

# Добавляем текст
text = [
    "Флаги нестандартных размеров на синтетических тканях.",
    "Цены указаны на полиэфирный шелк.",
    "Печать на ткани атлас, габардин: +50 рублей за м.кв.",
    "Печать на ткани шармус, сатен, шифон, полиоксофд, мокрый шелк: +100 рублей за м.кв.",
    "Постпечатная обработка входит в стоимость:",
    "· Крепления (карман, стропа, петли, усиление по перу)",
    "· Установка люверсов",
    "· Обшив",
    "· Горячий рез"
]

# Вычисляем максимальную ширину текста для центрирования
max_text_width = max(draw.textbbox((0, 0), line, font=text_font)[2] - draw.textbbox((0, 0), line, font=text_font)[0] for line in text)
text_x = (image.width - max_text_width) // 2  # Центрируем текст

for line in text:
    draw.text((text_x, y_text), line, font=text_font, fill=text_color)
    y_text += 30  # Увеличиваем отступ между строками

# Добавляем таблицу
table = [
    ["Тираж кв. м", "До 5", "6-10", "11-20", "21-50", "51-100", "101-200", "201-300", "300-500"],
    ["Стоимость за кв.м,\nв рублях", "950", "780", "720", "640", "550", "480", "450", "400"]  # Перенос строки
]

# Начальные координаты для таблицы
y_table = y_text + 50  # Отступ после текста

# Параметры таблицы
cell_widths = [160, 90, 90, 90, 90, 90, 90, 90, 90]  # Ширина каждой ячейки
cell_height = 50  # Высота ячейки
header_color = (230, 240, 255)  # Цвет фона заголовка (светло-голубой)

# Вычисляем общую ширину таблицы
table_width = sum(cell_widths)
table_x = (image.width - table_width) // 2  # Центрируем таблицу

# Рисуем заголовок таблицы
x_table = table_x
for i, cell in enumerate(table[0]):
    draw.rectangle(
        [(x_table, y_table),
         (x_table + cell_widths[i], y_table + cell_height)],
        outline=(0, 0, 0), fill=header_color  # Цвет фона для заголовка
    )
    # Используем textbbox для вычисления размера текста
    bbox = draw.textbbox((0, 0), cell, font=table_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    # Центрируем текст в ячейке
    text_x = x_table + (cell_widths[i] - text_width) // 2
    text_y = y_table + (cell_height - text_height) // 2
    draw.text((text_x, text_y), cell, font=table_font, fill=title_color)
    x_table += cell_widths[i]  # Переходим к следующей ячейке

# Рисуем строку с ценами
x_table = table_x  # Сбрасываем координату X
y_table += cell_height  # Переходим на следующую строку
for i, cell in enumerate(table[1]):
    draw.rectangle(
        [(x_table, y_table),
         (x_table + cell_widths[i], y_table + cell_height)],
        outline=(0, 0, 0), fill=(255, 255, 255)  # Белый фон для ячеек с ценами
    )
    # Если это первая ячейка, обрабатываем перенос строки
    if i == 0:
        lines = cell.split("\n")  # Разделяем текст по переносу строки
        total_text_height = sum(draw.textbbox((0, 0), line, font=table_font)[3] - draw.textbbox((0, 0), line, font=table_font)[1] for line in lines) + 5 * (len(lines) - 1)
        start_y = y_table + (cell_height - total_text_height) // 2  # Начальная координата Y для текста
        for j, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=table_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            # Центрируем каждую строку текста
            text_x = x_table + (cell_widths[i] - text_width) // 2
            text_y = start_y
            draw.text((text_x, text_y), line, font=table_font, fill=text_color)
            start_y += text_height + 5  # Отступ между строками
    else:
        # Для остальных ячеек
        bbox = draw.textbbox((0, 0), cell, font=table_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        # Центрируем текст в ячейке
        text_x = x_table + (cell_widths[i] - text_width) // 2
        text_y = y_table + (cell_height - text_height) // 2
        draw.text((text_x, text_y), cell, font=table_font, fill=text_color)
    x_table += cell_widths[i]  # Переходим к следующей ячейке

# Сохраняем изображение
image.save("price_table.png")

# Показываем изображение
image.show()