import os
import codecs
from sys import platform as _platform


def main():
    """Конвертер файлов импорта формата ibank2 в формат CSV"""
    folder_in = 'in'
    folder_out = 'out'
    folder_out_dct = folder_out + "/dct"
    if not os.path.exists("out"):
        os.mkdir(folder_out)
    if not os.path.exists("out/dct"):
        os.mkdir(folder_out_dct)

    files = os.listdir(folder_in)

    for fl in files:
        path_to_file = os.path.join(folder_in, fl)
        name, extension_in = fl.rsplit('.', 1)
        if extension_in == "txt":
            converter(name, folder_out, folder_out_dct)

    # Открыть в проводнике ОС
    if _platform == "linux" or _platform == "linux2":
        # Требует наличия xdg-open
        os.system('xdg-open "%s"' % folder_out)
    elif _platform == "darwin":
        os.system('open "%s"' % folder_out)
    elif _platform == "win32":
        os.startfile(folder_out)


def converter(name, folder_out, folder_out_dct):
    delimiter = ';'
    f = codecs.open('in/' + name + '.txt', 'r', "cp1251")
    lines = f.readlines()

    # f = open('in/' + name + '.txt', 'r')
    #
    # lines = f.readlines()
    before_text1 = lines[0][:-1]

    dict_file = open(folder_out_dct + "/" + name + "." + "dct", 'w')
    csv_file = open(folder_out + "/" + name + "." + "csv", 'w')

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

    # Костыль. Следует переписать так, чтобы алгорим отрабатывал без пустой строки в конце списка.
    if lines[-1] != "\r\n":
        lines.append(lines.pop()+"\r\n")
    else:
        print(lines)

    for line in lines[1:]:

        # Документы разделяются 1 или множеством путсых строк.
        if line == "\r\n":
            if before_line != "\r\n":
                num_docs += 1

                #Если в документе не было параметров от предыдущих документов, их стоит заполнить пустым значением
                for v in csv:
                    if len(csv[v]) < num_docs-1:
                        csv[v].append("\"\";")

        else:
            data = line.split("=", 1)
            if len(data) == 1:
                print("Строка:\n\"%s\"\nв файле \"%s.txt\" не содержит разделитель '=' и будет пропущена." % (line[:-2], name))
                continue

            # Если в новом документе есть новый параметр, то стоит заполнить пустыми значениями параметр для предыдущих документов
            if not csv.get(data[0]):
                csv.update({data[0]: []})
                while len(csv[data[0]])+1 < num_docs:
                    csv[data[0]].append("\"\";")
            # экранирование символа '"' в ячейки и самой ячейки этим символом
            csv[data[0]].append('"' + data[1][:-2].replace('"', '""') + '"' + delimiter)

            # dict_file.write(data[0] + "=" + "${" + str(i) + "}" + "\n")
            # # экранирование символа '"' в ячейки и самой ячейки этим символом
            # csv_data = '"' + data[1][:-2].replace('"', '""') + '"' + delimiter
            #
            # csv_file.write(csv_data)

        i += 1
        before_line = line

    for v in csv:
        if len(csv[v]) < num_docs:
            csv[v].append("\"\";")

    f.close()
    dict_file.close()
    csv_file.close()
    print(csv)


    print(num_docs)
if __name__ == '__main__':
    main()