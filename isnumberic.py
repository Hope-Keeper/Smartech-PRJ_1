#module
def isnumeric(string):
    flag = True
    tst_list = []
    for i in string:
        tst_list.append(i)
    
    for i in tst_list:
        try:
            x = int(i)
        
        except ValueError:
            
            flag = False
            break

    return flag
