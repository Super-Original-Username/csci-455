import re

parenbracket_reg = r'[\(\[\)\]]'

tester = '[no ' 'yes '+ '"of course" ' + '\"I don\'t have a nose\"]'
#split = []
print(tester)

#tester = re.sub(parenbracket_reg,'',tester)
def process_multi_word(line):
        split = []
        in_line = re.sub(parenbracket_reg,'',line)
        last = 0
        first_quote_found = False
        for i in range(len(in_line)):
            temp = ''
            if in_line[i] == '"':
                if not first_quote_found:
                    first_quote_found = True
                    last += 1
                elif first_quote_found:
                    first_quote_found = False
                    temp = in_line[last:i]
                    temp.strip()
                    temp = re.sub(r'\\','',temp)
                    if not re.match(r'\s',temp):
                        split.append(temp)
                    last = i+1
            elif not first_quote_found:
                if re.match(r'\s', in_line[i]):
                    temp = in_line[last:i]
                    temp.strip()
                    temp = re.sub(r'\\','',temp)
                    if not re.match(r'\s',temp):
                        split.append(temp)
                    last = i+1
        return split

if __name__ == '__main__':
    print(process_multi_word(tester))