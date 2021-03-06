﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import base64
import textwrap
from sys import platform as _platform


def main():
    """Конвертер файлов импорта формата xml в формат УФЭБС"""
    folder_in = 'in/ufebs'
    folder_out = 'out/base64'
    if not os.path.exists(folder_out):
        os.makedirs(folder_out)

    files = [f for f in os.listdir(folder_in) if os.path.isfile(folder_in + "/" + f)]

    for fl in files:
        name, extension_in = fl.rsplit('.', 1)
        if extension_in == "xml":
            converter(name, folder_in, folder_out)

    # Открыть в файловом менеджере операционной системы
    if _platform == "linux" or _platform == "linux2":
        # Требует наличия xdg-open
        os.system('xdg-open "%s"' % folder_out)
    elif _platform == "darwin":
        os.system('open "%s"' % folder_out)
    elif _platform == "win32":
        os.startfile(folder_out.replace("/", "\\"))


def converter(name, folder_in, folder_out):
    extension_out = "base64"
    xmlfile = open("%s/%s.xml" % (folder_in, name), 'rb')
    before_text = '''<?xml version="1.0" encoding="windows-1251"?>
<sen:SigEnvelope xmlns:sen="urn:cbr-ru:dsig:env:v1.1">
<sen:SigContainer><dsig:MACValue xmlns:dsig="urn:cbr-ru:dsig:v1.1">MIIBZAYJKoZIhvcNAQcCoIIBVTCCAVECAQExDzANBgkrBgEEAZxWAQEFADALBgkqhkiG9w0BBwExggEsMIIBKAIBATBYMEQxCzAJBgNVBAYTAlJVMQswCQYDVQQIEwIzNTEMMAoGA1UEChMDQ0JSMQ0wCwYDVQQLEwRPQlpJMQswCQYDVQQDEwJDQQIQQDYQy35+XbiHQh5+VSfBBjANBgkrBgEEAZxWAQEFAKBpMBgGCSqGSIb3DQEJAzELBgkqhkiG9w0BBwEwHAYJKoZIhvcNAQkFMQ8XDTE1MTIyMTA4NTc0NlowLwYJKoZIhvcNAQkEMSIEIF5lq3qlGU4Qm+P26tewGSN/tiexRGNpZzV+zZctrRgbMA0GCSsGAQQBnFYBAgUABED8x0TsFwQaigF5HgakwZ2Fq/zz7WFGLFwqAc5bfU7LWkk2pTdIjJdhHXc+VVGmqlLIl0yUphlpkjTsGt3kxkGu</dsig:MACValue></sen:SigContainer>
<sen:Object>'''
    text = xmlfile.read()
    after_text = '''</sen:Object>
</sen:SigEnvelope>
'''

    # Преобразование байтовой строки text base64
    encoded = base64.b64encode(text)
    # ПДекодирование из байтовой строки с base64 в utf-8
    encoded = encoded.decode("utf-8")
    # Разбиение строчки на 72 символа
    file72 = textwrap.fill(encoded, 72)
    converted_file = open(folder_out + "/" + name + "." + extension_out, 'w')
    converted_file.write(before_text + file72 + after_text)

    xmlfile.close()
    converted_file.close()

if __name__ == '__main__':
    main()
