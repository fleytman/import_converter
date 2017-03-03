import os
import codecs
from sys import platform as _platform
from collections import OrderedDict
import dbf
import csv


def main():
    """Конвертер файлов импорта формата ibank2 в формат CSV"""
    folder_in = 'in/csv'
    folder_in_dct = folder_in + "/dct"
    folder_out = 'out/dbf'
    folder_out_dct = folder_out + "/dct"
    if not os.path.exists(folder_out):
        os.mkdir(folder_out)
    if not os.path.exists(folder_out_dct):
        os.mkdir(folder_out_dct)

    files = [f for f in os.listdir(folder_in) if os.path.isfile(folder_in + "/" +f)]

    for fl in files:
        path_to_file = os.path.join(folder_in, fl)
        name, extension_in = fl.rsplit('.', 1)

        if extension_in == "csv" and os.path.isfile(folder_in_dct + "/" + name + ".dct"):
            print("ura")

            reader = csv.reader(open(folder_in+ "/" + name + "." + extension_in), delimiter=';', quotechar='"')
            with(open(folder_out + "/" + 'output.csv', 'w', newline="")) as infile:
                writer = csv.writer(infile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                for row in reader:
                    if row != []:
                        #print('"' + '","'.join(row))

                        writer.writerow(row)
            with(codecs.open(folder_out + "/" + 'output.csv', 'r', "cp1251")) as infile:
                with(codecs.open(folder_out + "/" + 'output2.csv', 'w', "cp1251")) as infile2:

                    infile2.write(infile.read().rstrip())

            from_csv(folder_out + '/output2.csv')

            #converter(name, folder_out, folder_out_dct)

    # # Открыть в проводнике ОС
    # if _platform == "linux" or _platform == "linux2":
    #     # Требует наличия xdg-open
    #     os.system('xdg-open "%s"' % folder_out)
    # elif _platform == "darwin":
    #     os.system('open "%s"' % folder_out)
    # elif _platform == "win32":
    #     os.startfile(folder_out.replace("/", "\\"))


def converter(name, folder_out, folder_out_dct):
    delimiter = ';'
    some_table = dbf.from_csv(csvfile='in/csv/' + name + '.csv', to_disk=True)
    for a in some_table:
        print(a)


    #before_text1 = lines[0][:-2] + "\n"

    dict_file = open(folder_out_dct + "/" + name + "." + "dct", 'w')
    dbf_file = open(folder_out + "/" + name + "." + "dbf", 'w')

    before_text2 = '''Data-Type=dct
Import-Format=dbf
First-String-Read=true

'''
    #dict_file.write(before_text1)
    dict_file.write(before_text2)

    i = 0
    num_docs = 0
    before_line = ""
    csv = {}
    csv = OrderedDict(csv)



    f.close()
    dict_file.close()
    dbf_file.close()



def from_csv(csvfile, to_disk=False, filename=None, field_names=None, extra_fields=None, dbf_type='db3', memo_size=64, min_field_size=1,
    delimiter=','):
    print(csvfile)
    # dbf.default_codepage = 'cp1251'
    # dbf._codepage_lookup = 'cp1251'
    some_table = dbf.from_csv(csvfile=csvfile, encoding="cp1251" ,to_disk=True, filename=None, field_names=None, extra_fields=None, dbf_type='db3', memo_size=64, min_field_size=1)
    print(some_table)



if __name__ == '__main__':
    main()