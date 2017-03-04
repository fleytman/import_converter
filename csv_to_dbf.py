import os
import codecs
from sys import platform as _platform
from collections import OrderedDict
import dbf
import csv


def main():
    """Конвертер файлов импорта формата csv в формат dbf"""
    folder_in = 'in/csv'
    folder_in_dct = folder_in + "/dct"
    folder_out = 'out/dbf'
    folder_out_dct = folder_out + "/dct"

    delimiter = ';'

    if not os.path.exists(folder_out):
        os.makedirs(folder_out)
    if not os.path.exists(folder_out_dct):
        os.makedirs(folder_out_dct)

    files = [f for f in os.listdir(folder_in) if os.path.isfile(folder_in + "/" +f)]

    for fl in files:
        name, extension_in = fl.rsplit('.', 1)

        # Проверка, что файл имеет расширение csv и наличие словаря к файлу
        if extension_in == "csv" and os.path.isfile(folder_in_dct + "/" + name + ".dct"):
            reader = csv.reader(open(folder_in+ "/" + name + "." + extension_in), delimiter=delimiter, quotechar='"')
            # Замена разделителя на запятую(требуется для работы from_csv)
            with(open(folder_out + "/" + 'output.csv', 'w', newline="")) as infile:
                writer = csv.writer(infile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                for row in reader:
                    if row:
                        writer.writerow(row)
            # Удаление пустых строк
            with(codecs.open(folder_out + "/" + 'output.csv', 'r', "cp1251")) as infile:
                with(codecs.open(folder_out + "/" + 'output2.csv', 'w', "cp1251")) as infile2:
                    infile2.write(infile.read().rstrip())

            csvfile = folder_out + '/output2.csv'
            dbf_outfile = folder_out + "/" + name + ".dbf"
            dctfile = folder_in_dct + "/" + name + ".dct"
            dct_outfile = folder_out_dct + "/" + name + ".dct"

            converter(csvfile, dctfile, dbf_outfile, dct_outfile)
            os.remove(folder_out + "/" + 'output.csv')
            os.remove(folder_out + "/" + 'output2.csv')

    # Открыть в проводнике ОС
    if _platform == "linux" or _platform == "linux2":
        # Требует наличия xdg-open
        os.system('xdg-open "%s"' % folder_out)
    elif _platform == "darwin":
        os.system('open "%s"' % folder_out)
    elif _platform == "win32":
        os.startfile(folder_out.replace("/", "\\"))


def converter(csvfile, dctfile, dbf_outfile, dct_outfile):
    print(csvfile)

    some_table = from_csv(csvfile=csvfile, encoding="cp1251", to_disk=False, filename=dbf_outfile, field_names=None, extra_fields=None, dbf_type="db3", memo_size=64, min_field_size=1)
    #os.remove(dbf_outfile[:-4] + ".dbt")

    with(codecs.open(dctfile, 'r', "cp1251")) as infile:
        with(codecs.open(dct_outfile, 'w', "cp1251")) as outfile:
            i = 0
            f = 0
            for line in infile.readlines():
                if i == 2:
                    print(line.replace("csv", "dbf"))
                    outfile.write(line.replace("csv", "dbf"))
                elif i > 4:
                    print("%s=${F%d,M}" % (line.split("=", 1)[0], f))
                    outfile.write("%s=${F%d,M}\r\n" % (line.split("=", 1)[0], f))
                    f += 1
                else:
                    print(line)
                    outfile.write(line)
                i += 1

"""
функция кусок from_csv - изменённый код из пакета https://pypi.python.org/pypi/dbf
Изменена кодировка с cp1252 на cp1251
=========
Copyright
=========
    - Portions copyright: 2008-2012 Ad-Mail, Inc -- All rights reserved.
    - Portions copyright: 2012-2013 Ethan Furman -- All rights reserved.
    - Author: Ethan Furman
    - Contact: ethan@stoneleaf.us

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    - Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    - Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    - Neither the name of Ad-Mail, Inc nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED ''AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
ITS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
def from_csv(csvfile, to_disk=False, filename=None, field_names=None, extra_fields=None,
             dbf_type='db3', memo_size=64, min_field_size=1,
             encoding=None, errors=None):

    """
    creates a Character table from a csv file
    to_disk will create a table with the same name
    filename will be used if provided
    field_names default to f0, f1, f2, etc, unless specified (list)
    extra_fields can be used to add additional fields -- should be normal field specifiers (list)
    """
    with codecs.open(csvfile, 'r', encoding='cp1251', errors=errors) as fd:
        reader = csv.reader(fd)
        if field_names:
            if isinstance(field_names, dbf.basestring):
                field_names = field_names.split()
            if ' ' not in field_names[0]:
                field_names = ['%s M' % fn for fn in field_names]
        else:
            field_names = ['f0 M']
        if filename:
            to_disk = True
        else:
            filename = os.path.splitext(csvfile)[0]
        if to_disk:
            csv_table = dbf.Table(filename, [field_names[0]], dbf_type=dbf_type, memo_size=memo_size, codepage=encoding)
        else:
            csv_table = dbf.Table(':memory:', [field_names[0]], dbf_type=dbf_type, memo_size=memo_size,
                              codepage=encoding, on_disk=False)
        csv_table.open()
        fields_so_far = 1
        while reader:
            try:
                row = next(reader)
            except UnicodeEncodeError:
                row = ['']
            except StopIteration:
                break
            while fields_so_far < len(row):
                if fields_so_far == len(field_names):
                    field_names.append('f%d M' % fields_so_far)
                csv_table.add_fields(field_names[fields_so_far])
                fields_so_far += 1
            csv_table.append(tuple(row))
        if extra_fields:
            csv_table.add_fields(extra_fields)
        csv_table.close()
        return csv_table


if __name__ == '__main__':
    main()