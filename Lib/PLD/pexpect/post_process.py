
def is_ascii(s):
    try:
        s.decode('ascii')
        return True
    except UnicodeDecodeError:
        return False
w = open('eccb_log.log','wb')
f = open('I-NE-DMPR-ENB-0030_2016-Dec-13_1656.eccb','rb')
for l in f:
     y = [x for x in l if is_ascii(x)]
     m =''.join(y).replace('[0m','')
     w.write(m.replace('\x1b',''))

w.close()
f.close()
