import re
s = 'csev@umich.edu'
lst = re.findall(r'@([A-Za-z0-9.-]+)', s)
print(lst[0])