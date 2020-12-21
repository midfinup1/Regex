import csv
import re


def read_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        rows = csv.reader(file, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def format_number(contacts_list):
    number_pattern_raw = r'(\+7|8)(\s*)(\(*)(\d{3})(\)*)(\s*|\-*)(\d{3})(\-|\s*)' \
                            r'(\d{2})(\-|\s*)(\d{2})' \
                            r'(\s*)(\(*)(доб)*(\.*)(\s*)(\d*)(\)*)'
    number_pattern_new = r'+7(\4)\7-\9-\11\12\14\15\17'
    contacts_list_updated = list()
    for number in contacts_list:
        number_raw = ','.join(number)
        number_formatted = re.sub(number_pattern_raw, number_pattern_new, number_raw)
        card_as_list = number_formatted.split(',')
        contacts_list_updated.append(card_as_list)
    return contacts_list_updated


def format_fcs(contacts_list):
    fcs_pattern_raw = r'^([А-ЯЁа-яё]+)' \
                        r'(\s*)(\,?)([А-ЯЁа-яё]+)' \
                        r'(\s*)(\,?)([А-ЯЁа-яё]*)' \
                        r'(\,?)(\,?)(\,?)'
    fcs_pattern_new = r'\1\3\10\4\6\9\7\8'
    contacts_list_updated = list()
    for fcs in contacts_list:
        fcs_as_string = ','.join(fcs)
        formatted_fcs = re.sub(fcs_pattern_raw, fcs_pattern_new, fcs_as_string)
        fcs_as_list = formatted_fcs.split(',')
        contacts_list_updated.append(fcs_as_list)
    return contacts_list_updated


def join_duplicates(contacts_list):
    for i in contacts_list:
        for j in contacts_list:
            if i[0] == j[0] and i[1] == j[1] and i is not j:
                if i[2] == '':
                    i[2] = j[2]
                if i[3] == '':
                    i[3] = j[3]
                if i[4] == '':
                    i[4] = j[4]
                if i[5] == '':
                    i[5] = j[5]
                if i[6] == '':
                    i[6] = j[6]

    contacts_list_updated = list()
    for string in contacts_list:
        if string not in contacts_list_updated:
            contacts_list_updated.append(string)
    return contacts_list_updated


def write_file(contacts_list):
    with open("phonebook.csv", "w", encoding='utf-8') as f:
        data_writer = csv.writer(f, delimiter=',')
        data_writer.writerows(contacts_list)


if __name__ == '__main__':
    phonebook = read_file('phonebook_raw.csv')
    phonebook_changed = format_number(phonebook)
    phonebook_changed = format_fcs(phonebook_changed)
    phonebook_changed = join_duplicates(phonebook_changed)
    write_file(phonebook_changed)
