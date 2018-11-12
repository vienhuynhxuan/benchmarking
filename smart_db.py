#!/usr/bin/env python3
import json
import sys
import resource

# first_name,last_name,username,age,gender,city
pos = {'first_name': 0,'last_name': 1,'username': 2,'age': 3,'gender': 4,
        'city': 5}

lstselect = []

def get_query():
    global lstselect
    f = open(str(sys.argv[-1]), "r")
    query = json.load(f)
    for i in query:
        temp = {}
        for j in i['select'].split(', '):
            temp[j] = i['select'].split(', ').index(j)
        lstselect.append(temp)
    return query


def compare(a, b, sign):
    if a.isdigit() and b.isdigit():
        a = int(a)
        b = int(b)
    if sign == '=':
        return a == b
    elif sign == '<':
        return a < b
    elif sign == '>':
        return a > b
    elif sign == '!=':
        return a != b


def check_condition(fielddict, value):
    global pos
    if 'first_letter' in fielddict['left']:
        temp = fielddict['left'].split(' ')[-1]
        newtemp = value[pos[temp]][0]
    else:
        temp = fielddict['left']
        newtemp = value[pos[temp]]
    return compare(newtemp, fielddict['right'], fielddict['op'])


def check_where_and(lst, value):
    for i in lst:
        if check_condition(i, value) == False:
            return False
    return True


def check_where_or(lst, value):
    for i in lst:
        if check_condition(i, value) == True:
            return True
    return False


def compare_line(a, b, order):
    global lstselect
    if a[lstselect[order]] < b[lstselect[order]]:
        return True
    return False


def print_result(lst):
    for i in lst:
        print(', '.join(i))


def check_line(line, query):
    global pos
    lst = []
    check = False
    if 'where_and' in query.keys():
        check =  check_where_and(query['where_and'], line)
    elif 'where_or' in query.keys():
        check =  check_where_or(query['where_or'], line)
    else:
        check = True
    if check:
        for i in query['select'].split(', '):
            if line[pos[i]][-1] == '\n':
                newline = line[pos[i]][0:len(line[pos[i]]) - 1]
            else:
                newline = line[pos[i]]
            lst.append(newline)
    return lst


def get_result():
    global pos, lstselect
    res = []
    temp = {}
    query = get_query()
    for i in range(len(query)):
        temp[i] = []
    line = sys.stdin.readline()
    while line != '':
        line = line.split(',')
        for i in range(len(query)):
            if len(check_line(line,query[i])) > 0:
                temp[i].append(check_line(line,query[i]))
        line = sys.stdin.readline()
    for i in range(len(query)):
        if 'order' in query[i].keys():
            temp[i].sort(key=lambda k:[k[lstselect[i][query[i]['order']]]])
            res.append(temp[i])
    for i in res:
        print_result(i)

def main():
    get_result()



main()
