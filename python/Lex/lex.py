import json
import re
import argparse

def tokenParser(token, startRow, startCol, endRow, endCol):
    if isComment == 1 or token == '':
        return

    if token in dic:
        results.append([token, dic[token] + 'number',
                        startRow, endRow, startCol + 1, endCol + 1])
    else:
        if re.match(r'^[0-9]+$', token):
            results.append([token, 'ICONSTnumber',
                        startRow, endRow, startCol + 1, endCol + 1])

        elif re.match(r'^\'.\'$', token):
            results.append([token, 'CCONSTnumber',
                        startRow, endRow, startCol + 1, endCol + 1])

        elif re.match('^\'.*\'$', token):
            results.append([token, 'SCONSTnumber',
                        startRow, endRow, startCol + 1, endCol + 1])

        elif re.match(r'^[0-9]+[a-zA-Z0-9]*$', token):
            errors.append([startRow, endRow, startCol + 1,endCol + 1,
                        token, '[SYNTAX ERROR]: Can not use this this as an identifier'])
        else:
            results.append([token, 'IDnumber', startRow,
                            endRow, startCol + 1, endCol + 1])
    return

parser = argparse.ArgumentParser("""
    *** PASC (Mini Pascal) lang                  ***
    *** 502057 (Programming Language Concepts)   ***
    *** Spring 2018-2019 assignment.             ***
""")

parser.add_argument('-i','--input',
                    help="Input path. Example: ./Lexical/Test05.txt")
args = parser.parse_args()

dict_file = './dictionary.json'
parse_file = args.input

dic = json.load(open(dict_file))
raw_text = open(parse_file).read()
raw_text = raw_text.replace('\n', ' \n')
isComment = 0
rowCnt = 1
token = ''
idx = 0
startCol = 0
lastCol = 0
results = []
errors = []
spaceTab = 0

while idx < len(raw_text):
    ch = raw_text[idx]
    if ch == '\n':
        rowCnt += 1
        tokenParser(token, rowCnt, startCol - lastCol + spaceTab,
                    rowCnt, idx - 1 - lastCol + spaceTab)
        token = ''
        idx += 1
        spaceTab = 0
        startCol = idx
        lastCol = idx

    elif ch == '\t':
        tokenParser(token, rowCnt, startCol - lastCol + spaceTab,
                    rowCnt, idx - 1 - lastCol + spaceTab)
        token = ''
        idx += 1
        spaceTab += 3
        startCol = idx

    elif ch == ' ':
        tokenParser(token, rowCnt, startCol - lastCol + spaceTab,
                    rowCnt, idx - 1 - lastCol + spaceTab)
        token = ''
        idx += 1
        startCol = idx

    elif ch == '(':
        if raw_text[idx + 1] == '*':
            isComment = 1
            token = ''
            idx += 1
            startCol = idx

        else:
            tokenParser(token, rowCnt, startCol - lastCol + spaceTab,
                        rowCnt, idx - 1 - lastCol + spaceTab)
            tokenParser(ch, rowCnt, idx - lastCol + spaceTab,
                        rowCnt, idx - lastCol + spaceTab)
            token = ''
            idx += 1
            startCol = idx

    elif ch == ')':
        tokenParser(token, rowCnt, startCol - lastCol + spaceTab,
                    rowCnt, idx - 1 - lastCol + spaceTab)
        tokenParser(ch, rowCnt, idx - lastCol + spaceTab, rowCnt,
                    idx - lastCol + spaceTab)
        token = ''
        idx += 1
        startCol = idx

    elif ch == ',':
        tokenParser(token, rowCnt, startCol - lastCol + spaceTab,
                    rowCnt, idx - 1 - lastCol + spaceTab)
        tokenParser(',', rowCnt, idx - lastCol + spaceTab, rowCnt,
                    idx - lastCol + spaceTab)
        idx += 1
        startCol = idx
        token = ''

    elif ch == '.' and raw_text[idx + 1] == '.':
        tokenParser(token, rowCnt, startCol - lastCol + spaceTab,
                    rowCnt, idx - 1 - lastCol + spaceTab)
        tokenParser('..', rowCnt, idx - lastCol + spaceTab,
                    rowCnt, idx + 1 - lastCol + spaceTab)
        idx += 2
        token = ''
        startCol = idx

    elif ch == ':':
        if raw_text[idx + 1] == '=':
            tokenParser(token, rowCnt, startCol - lastCol + spaceTab,
                        rowCnt, idx - 1 - lastCol + spaceTab)
            tokenParser(':=', rowCnt, idx - lastCol + spaceTab,
                        rowCnt, idx + 1 - lastCol + spaceTab)
            idx += 2
            token = ''
            startCol = idx

        else:
            tokenParser(token, rowCnt, startCol - lastCol + spaceTab,
                        rowCnt, idx - 1 - lastCol + spaceTab)
            tokenParser(':', rowCnt, idx - lastCol + spaceTab,
                        rowCnt, idx - lastCol + spaceTab)
            idx += 1
            token = ''
            startCol = idx

    elif ch == ';':
        tokenParser(token, rowCnt, startCol - lastCol + spaceTab,
                    rowCnt, idx - 1 - lastCol + spaceTab)
        tokenParser(ch, rowCnt, idx - lastCol + spaceTab,
                    rowCnt, idx - lastCol + spaceTab)
        idx += 1
        startCol = idx
        token = ''

    elif ch == '+':
        tokenParser(token, rowCnt, startCol - lastCol + spaceTab,
                    rowCnt, idx - 1 - lastCol + spaceTab)
        tokenParser(ch, rowCnt, idx - lastCol + spaceTab,
                    rowCnt, idx - lastCol + spaceTab)
        idx += 1
        startCol = idx
        token = ''

    elif ch == '-':
        if re.match(r'^[0-9]$', raw_text[idx + 1]):
            idx += 1
            token = token + ch
        else:
            tokenParser(token, rowCnt, startCol - lastCol + spaceTab,
                        rowCnt, idx - 1 - lastCol + spaceTab)
            tokenParser(ch, rowCnt, idx - lastCol + spaceTab,
                        rowCnt, idx - lastCol + spaceTab)
            idx += 1
            startCol = idx
            token = ''

    elif ch == '*':
        if raw_text[idx + 1] == ')' and isComment == 0:
            errors.append([rowCnt, rowCnt, idx - lastCol + spaceTab,
                            idx - lastCol + spaceTab,
                            '[ERROR]: Is this the end of comment?'])
            idx += 2

        elif raw_text[idx + 1] == ')':
            isComment = 0
            idx += 1
            startCol = idx
            token = ''

        else:
            tokenParser(token, rowCnt, startCol - lastCol + spaceTab,
                        rowCnt, idx - 1 - lastCol + spaceTab)
            tokenParser(ch, rowCnt, idx - lastCol + spaceTab,
                        rowCnt, idx - lastCol + spaceTab)
            idx += 1
            startCol = idx
            token = ''

    else:
        token = token + ch
        idx += 1

if len(token) > 0:
    tokenParser(token, rowCnt, startCol - lastCol, rowCnt, idx - 1 - lastCol)

fileOut = open('out.txt', 'w+')
for i in results:
    fileOut.write(str(i[0]) + ' ' + (i[1]) + ' ' + str(i[2]) + ' ' +
                str(i[3]) + ' ' + str(i[4]) + ' ' + str(i[5]) + '\n')

for i in errors:
    fileOut.write('ERROR ' + str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[2]) + '\n')

fileOut.close()
print('See: out.txt')
