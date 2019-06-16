#filepath='/home/yuriy/Documents/vipiski/kv_ffe45c81-441c-46c8-9530-330e74a8862e.xml' # - 001001000000 sobstvennik
#filepath='/home/yuriy/Documents/vipiski/kv_fb035656-99f2-4580-9831-b579356e2580.xml' # - 001002000000 dovelvka
#filepath='/home/yuriy/Documents/vipiski/kv_c7568c7d-abd1-4c60-98b3-66100b09fce4.xml' # - 001003000000 sovmestnoe

import re
import sys

filepath = sys.argv[1]

def sovmestnoe_parse_name(name):
    FIO = ''
    for i in name.split('\n'):
        if '<Surname>' in i:
            FIO += remove_html_tags(i) + " "
        elif '<First>' in i:
            FIO += remove_html_tags(i) + " "
        elif '<Patronymic>' in i:
            FIO += remove_html_tags(i) + " "
    return FIO

def remove_html_tags(i):
    p = re.compile(r'<.*?>')
    return p.sub('', i)

def get_flat_number(i):
    return re.findall('\d+', i)

def sobstvennik_parse(sobstvennik_data):
    pravo = ''
    for i in sobstvennik_data.split('\n'):
        if '<Name>' in i:
            pravo = remove_html_tags(i)
    return pravo

def sobstvennik(data):
    result = ''
    all_names = []
    name_flag = False
    name = ''
    flag = False
    sobstvennik_data = ''
    pravo = ''
    FIO = ''
    for i in data.split('\n'):
        if '<Area>' in i:
            area = remove_html_tags(i)
        elif '<FIO>' in i:
            name += i + '\n'
            name_flag = True
        elif '</FIO>' in i:
            FIO = sovmestnoe_parse_name(name)
            all_names.append(FIO)
            name = ''
            name_flag = False
        elif name_flag is True:
            name += i + '\n'
        elif '<Position NumberOnPlan' in i:
            flat_number = get_flat_number(i)[0]
        elif '<Right RightNumber' in i:
            sobstvennik_data += i + '\n'
            flag = True
        elif '</Registration>' in i:
            sobstvennik_data += i + '\n'
            flag = False
            pravo = sobstvennik_parse(sobstvennik_data)
        elif flag is True:
            sobstvennik_data += i + '\n'
    result += FIO + " | " + flat_number + " | " + pravo + " | " + "Собственность" + " | " + area + " | " + "1"
    print(result)

def dovelvka_separator(dovelvka_data):
    FIO = ''
    reg_number = False
    dolya_number = False
    dolya = ''
    pravo = ''
    for i in dovelvka_data.split('\n'):
        if '<Surname>' in i:
            FIO += " " + remove_html_tags(i)
        elif '<First>' in i:
            FIO += " " + remove_html_tags(i)
        elif '<Patronymic>' in i:
            FIO += " " + remove_html_tags(i)
        elif '<RegNumber>' in i:
            if reg_number is False:
                pravo = remove_html_tags(i)
                reg_number = True
            else:
                pass
        elif '<ShareText>' in i:
            if dolya_number is False:
                dolya = remove_html_tags(i)
                dolya_number = True
            else:
                pass
    return FIO, pravo, dolya

def dovelvka(data):
    result = ''
    dovelvka_data = ''
    flag = False
    FIO = ''
    for i in data.split('\n'):
        if '<Area>' in i:
            area = remove_html_tags(i)
        elif '<Position NumberOnPlan' in i:
            flat_number = get_flat_number(i)[0]
        elif '<Right RightNumber' in i:
            dovelvka_data += i + '\n'
            flag = True
        elif '</Right>' in i:
            dovelvka_data += i + '\n'
            flag = False
            FIO, pravo, dolya = dovelvka_separator(dovelvka_data)
            result += FIO + " | " + flat_number + " | " + pravo + " | " + "Долевая собственность" + " | " + area + " | " + dolya
            print(result)
            result = ''
            dovelvka_data = ''
        elif flag is True:
            dovelvka_data += i + '\n'

def sovmestnoe(data):
    result = ''
    sovmestnoe_data = ''
    flag = False
    FIO = ''
    name_flag = False
    name = ''
    all_names = []
    for i in data.split('\n'):
        if '<Area>' in i:
            area = remove_html_tags(i)
        elif '<Position NumberOnPlan' in i:
            flat_number = get_flat_number(i)[0]
        elif '<Content>' in i:
            pravo = remove_html_tags(i)
        elif '<Right RightNumber' in i:
            sovmestnoe_data += i + '\n'
            flag = True
        elif '</Registration>' in i:
            sovmestnoe_data += i + '\n'
            flag = False
        elif '<FIO>' in i:
            name += i + '\n'
            name_flag = True
        elif '</FIO>' in i:
            FIO = sovmestnoe_parse_name(name)
            all_names.append(FIO)
            name = ''
            name_flag = False
        elif name_flag is True:
            name += i + '\n'
        elif flag is True:
            sovmestnoe_data += i + '\n'
    for i in all_names:
        print(i + " | " + flat_number + " | " + pravo + " | " + "Совместная собственность" + " | " + area + " | " + str(100/len(all_names)))

data = ''
flag = False
type = 0
with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    type_find = False
    while line:
        if '<ExtractObject>' in line:
            data += line
            flag = True
        elif '</ExtractObject>' in line:
            data += line
            flag = False
        elif flag is True:
            data += line
        elif '<Position NumberOnPlan' in line:
            data += line
        elif '<Area>' in line:
            data += line
        if type_find is False:
            if '<Type>001001000000</Type>' in line:
                type = 1
                data += line
                type_find = True
            elif '<Type>001002000000</Type>' in line:
                type = 2
                data += line
                type_find = True
            elif '<Type>001003000000</Type>' in line:
                type = 3
                data += line
                type_find = True
        else:
            pass
        line = fp.readline()


if type is 1:
    sobstvennik(data)
elif type is 2:
    dovelvka(data)
elif type is 3:
    sovmestnoe(data)
