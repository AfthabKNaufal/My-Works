
str = input()
list = []
flag_of_brac = 0
flag_of_sq = 0
flag_of_para = 0
flag_of_clo_para = 0
flag_of_clo_sq = 0
flag_of_clo_brac = 0
for rec in str:
    list.append(rec)
print(list)
for record in list:
    if record == '{' or record == '[' or record == '(':
        if record == '{':
            list.remove('{')
            flag_of_para += 1
        if record == '[':
            list.remove('[')
            flag_of_sq += 1
        if record == '(':
            list.remove('(')
            flag_of_brac += 1

    print(list)
for records in list:
    if records != '{' or records != '[' or records !
    = '(':
        if records == '}':
            flag_of_clo_para += 1
        elif records == ']':
            flag_of_clo_sq += 1
        else:
            flag_of_clo_brac += 1


# open =flag_of_sq + flag_of_brac + flag_of_para
# close = flag_of_clo_sq + flag_of_clo_brac + flag_of_clo_para
if flag_of_sq == flag_of_clo_sq and flag_of_brac == flag_of_clo_brac and flag_of_para == flag_of_clo_para:
    # return True
    print("yes")
else:
    # return False
    print("no")