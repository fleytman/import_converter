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

    # Алгоритм работает для одного документа на импорт, не обрабатывает случая наличия путсых строк
    i = 0
    num_docs = 0
    before_line = ""
    for line in lines[1:]:

        if line == "\r\n":
            if before_line != "\r\n":
                num_docs += 1
                if num_docs > 1:
                    print("На данный момент нет поддержки нескольких документов в файле импорта, будет конвертирован только первый документ в файле %s.txt" % name)
                    break
        else:
            data = line.split("=", 1)
            if len(data) == 1:
                print("Строка ""%s"" некорректна в файле %s.txt и будет пропущена" % (line, name))
                continue

            dict_file.write(data[0] + "=" + "${" + str(i) + "}" + "\n")
            # экранирование символа '"' в ячейки и самой ячейки этим символом
            csv_data = '"' + data[1][:-2].replace('"', '""') + '"' + delimiter

            csv_file.write(csv_data)
        before_line = line
        i += 1

    f.close()
    dict_file.close()
    csv_file.close()

    if lines[-1] == "\r\n":
        num_docs -= 1
    print(num_docs)
if __name__ == '__main__':
    main()