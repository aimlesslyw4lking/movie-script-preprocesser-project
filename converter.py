import os

# Укажите путь к папке, где лежат ваши файлы .conllu
input_folder = "input_conllu"
# Укажите папку, куда сохранить готовые файлы для AntConc
output_folder = "output_antconc"

# Создаем папку для результата, если ее нет
os.makedirs(output_folder, exist_ok=True)

# Проверяем все файлы в папке
for filename in os.listdir(input_folder):
    if filename.endswith(".conllu"):
        input_path = os.path.join(input_folder, filename)
        
        # Берем имя файла без расширения в качестве маркера подкорпуса (например, "крош")
        subcorpus = os.path.splitext(filename)[0]
        
        antconc_tokens = []
        
        with open(input_path, "r", encoding="utf-8") as f:
            for line in f:
                # Пропускаем технические комментарии UDPipe и пустые строки
                if line.startswith("#") or not line.strip():
                    continue
                
                columns = line.split("\t")
                
                # Проверяем, что в строке достаточно колонок (в CoNLL-U их должно быть 10)
                if len(columns) < 10:
                    continue
                
                word = columns[1]       # 2-я колонка: Слово (FORM)
                lemma = columns[2]      # 3-я колонка: Лемма (LEMMA)
                pos = columns[3]        # 4-я колонка: Часть речи (UPOS)
                deprel = columns[7]     # 8-я колонка: Синтаксическая роль (DEPREL)
                
                # Пропускаем знаки препинания, если они не нужны как слова с ролями
                if pos == "PUNCT":
                    continue
                
                # Собираем токен в формате: слово#лемма#чр#роль#подкорпус
                # Пример: мыла#мыть#VERB#root#крош
                token = f"{word}#{lemma}#{pos}#{deprel}#{subcorpus}"
                antconc_tokens.append(token)
        
        # Сохраняем результат в линейную строку через пробел
        output_filename = f"{subcorpus}_ready.txt"
        output_path = os.path.join(output_folder, output_filename)
        
        with open(output_path, "w", encoding="utf-8") as f_out:
            f_out.write(" ".join(antconc_tokens))
            
        print(f"Успешно обработан файл: {filename} -> {output_filename}")

print("\nВсе файлы готовы для загрузки в AntConc!")