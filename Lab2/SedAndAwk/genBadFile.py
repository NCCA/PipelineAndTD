#!/usr/bin/env python
import random,string

def randName() :
    return ''.join(random.choices(string.ascii_letters)+(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 20))))

with open('data.txt','w') as file :
    for i in range(0,200) :
        for l in range(0,random.randint(2,10)+2) :
            file.write(randName()+',')
        file.write('\r\n')

