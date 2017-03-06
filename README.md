# import_converter
Несколько утилит по конвертированию файлов импорта ibank2

Предполагается, что все файлы для конвертирования имеют первоначальную кодировку cp1251 и окончания строк crlf [подробнее](https://github.com/fleytman/import_converter/issues/1#issuecomment-276956924)

Утилиты обрабатываются все файлы указанного формата, игонрируя все остальные файлы и директории.

**ufebs.py** - конвертирует УФЭБС(xml) в base64. В директории `in/ufebs` лежит файл importUfebs.xml как пример. На выходе в директории `out/base64` создаются конвертированные файлы 

**ib2_to_csv.py** - конвертер из формата ibank2(txt) в csv. В директории `in/ibank2` лежит пример. На выходе в директории `out/scv` создаётся csv файлы, в `out/csv/dct` словарь

**csv_to_dbf.py** - конвертер из формата csv в формат dbf. Файл csv лежит в директории `in/csv` как пример, файл словаря в директории `in/csv/dct`. На выходе в директории `out/dbf` создаётся dbf и dbt файлы, в `out/dbf/dct` словарь. 



Для работы утилит требуется python3.5 и модули, которые можно установить с помощью
`pip3 install -r requirements.txt`

Утилиты работают на Windows 10, для работы на других ОС могут понадобиться мелкие правки кода.
