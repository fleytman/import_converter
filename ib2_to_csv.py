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
    f = codecs.open('in/' + name + '.txt', 'r', "cp1251")
    lines = f.readlines()
    print(lines)

    # f = open('in/' + name + '.txt', 'r')
    #
    # lines = f.readlines()
    print(lines[0][:-1])
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
    for line in lines[2:]:
        data = line.split("=", 1)
        dict_file.write(data[0] + "=" + "${" + str(i) + "}" + "\n")

        if data[1].find('"') != -1:
            csv_data = '"' + data[1][:-2].replace('"', '""') + '"' + ";"
            csv_file.write(csv_data)
        else:
            csv_file.write(data[1][:-2] + ";")
        i += 1

    f.close()
    dict_file.close()
    csv_file.close()


if __name__ == '__main__':
    main()