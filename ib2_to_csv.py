import configparser
import os
import codecs
from sys import platform as _platform
from collections import OrderedDict


def main():
    """Конвертер файлов импорта формата ibank2 в формат CSV"""
    folder_in = 'in/ibank2'
    folder_out = 'out/csv'
    folder_out_dct = folder_out + "/dct"

    config = configparser.ConfigParser()

    if os.path.exists("config.ini"):
        config.read('config.ini')
    else:
        print("Нет файла config.ini\nРазделителем будет ';'")

    if config.get("ib2_to_csv", "delimiter") == ";":
        delimiter = ';'
    elif config.get("ib2_to_csv", "delimiter") == ",":
        delimiter = ','
    elif config.get("ib2_to_csv", "delimiter") == "tab":
        delimiter = '\t'
    else:
        print("Разделитель в файле config.ini не указан. Разделителем будет ';'")
        delimiter = ';'

    if not os.path.exists(folder_out):
        os.makedirs(folder_out)
    if not os.path.exists(folder_out_dct):
        os.makedirs(folder_out_dct)

    files = [f for f in os.listdir(folder_in) if os.path.isfile(folder_in + "/" +f)]

    for fl in files:
        name, extension_in = fl.rsplit('.', 1)
        if extension_in == "txt":
            converter(name, folder_in, folder_out, folder_out_dct, delimiter)

    # Открыть в проводнике ОС
    if _platform == "linux" or _platform == "linux2":
        # Требует наличия xdg-open
        os.system('xdg-open "%s"' % folder_out)
    elif _platform == "darwin":
        os.system('open "%s"' % folder_out)
    elif _platform == "win32":
        os.startfile(folder_out.replace("/", "\\"))


def converter(name, folder_in, folder_out, folder_out_dct, delimiter):
    f = codecs.open("%s/%s.txt" % (folder_in, name), 'r', "cp1251")
    lines = f.readlines()

    before_text1 = "%s\n" % lines[0].rstrip()

    dict_file = open("%s/%s.dct" % (folder_out_dct, name), 'w')
    csv_file = open("%s/%s.csv" % (folder_out, name), 'w')

    before_text2 = '''Data-Type=dct
Import-Format=csv
First-String-Read=true

'''
    dict_file.write(before_text1)
    dict_file.write(before_text2)

    i = 0
    num_docs = 0
    before_line = ""
    csv = {}
    csv = OrderedDict(csv)

    # Костыль. Следует переписать так, чтобы алгорим отрабатывал без пустой строки в конце списка.
    if lines[-1] != "\r\n":
        lines.append("%s\r\n" % lines.pop())

    for line in lines[1:]:

        # Документы разделяются 1 или множеством путсых строк.
        if line == "\r\n":
            if before_line != "\r\n":
                num_docs += 1

                # Если в документе не было параметров от предыдущих документов, их стоит заполнить пустым значением
                for v in csv:
                    if len(csv[v]) < num_docs-1:
                        csv[v].append('""%s' % delimiter)

        else:
            data = line.split("=", 1)
            if len(data) == 1:
                print("Строка:\n\"%s\"\nв файле \"%s.txt\" не содержит разделитель '=' и будет пропущена." %
                      (line[:-2], name))
                continue

            # Если в новом документе есть новый параметр, то стоит заполнить пустыми значениями параметр для предыдущих документов
            if not csv.get(data[0]):
                csv.update({data[0]: []})
                while len(csv[data[0]])+1 < num_docs:
                    csv[data[0]].append('""%s' % delimiter)
            # Экранирование символа '"' в ячейки и самой ячейки этим символом
            csv[data[0]].append('"%s"%s' % (data[1][:-2].replace('"', '""'), delimiter))

        i += 1
        before_line = line
    # Если в документе нет значения для параметра, заполнить пустым значением
    for v in csv:
        if len(csv[v]) < num_docs:
            csv[v].append('""%s' % delimiter)
    i = 0
    for v in csv:
        dict_file.write(v + "=" + "${" + str(i) + "}" + "\n")
        dict_file.write('%s=${%s}\n' % (v, str(i)))
        i += 1
    # Список с пуcтыми списками количеством равным количеству документов
    values_list = [[] for x in range(num_docs)]
    # Каждый список равен строке
    for t in csv:
        i = 0
        while i < len(csv[t]):
            values_list[i].append(csv[t][i])
            i += 1
    i=0
    # Запись в csv построчно
    while i < num_docs:
        csv_data = "".join(values_list[i-1][:-1])+"\n"
        csv_file.write(csv_data)
        i+=1

    f.close()
    dict_file.close()
    csv_file.close()

if __name__ == '__main__':
    main()