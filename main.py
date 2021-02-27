import csv
import re

# поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно.
# В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О;
# привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999;
# объединить все дублирующиеся записи о человеке в одну.

with open("phonebook_raw.csv", newline="", encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

pattern_phone = re.compile(r"(\+7|8)?[\s-]*\(*(\d{3})\)*[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d+)([\s]*\(*)(доб?\)*\.?[\s]*)*(\d+)*([\s)]*)")

for text in contacts_list[1:]:
    new_text = pattern_phone.sub(r"+7(\2)\3-\4-\5 \7\8", text[5])
    text[5] = new_text
new_contacts_list = list()

for person in contacts_list:
    last_name = re.split(r" ", person[0])
    last_name.extend(person[1:])
    name = re.split(r" ", last_name[1])
    if len(name) > 1:
        last_name[1] = name[0]
        last_name[2] = name[1]
    new_contacts_list.append(last_name)


for person in new_contacts_list:
    pattern = re.compile(person[0])
    person_count = pattern.findall(str(new_contacts_list))
    if len(person_count) > 1:
        new_contacts_list.remove(person)

with open("phonebook.csv", "w", newline="", encoding='UTF-8') as file:
    datawriter = csv.writer(file, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')
    datawriter.writerows(new_contacts_list)
