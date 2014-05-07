tups=[('Demo',1,1),('Demo',2,2),('Demo',1,3),('Demo',2,4),('Demo',1,5),('Demo',2,6)]
uids=[]

def checkDemo(serial,uidtup)
    if serial == 'Demo':
        
        for uniqueID in uids:
            if uniqueID.count('Demo'):
                uid_count += .5
        demo_count = uid_count // 2
        serial+'%s'%(demo_count+1)
    else:
        return serial

def makeUID(uidTup):
    serial,channel,pointer = uidTup
    serial = checkDemo(serial)
    uid = serial + '_%s'%channel
    return uid


while 1: #ICK
    try:
        s=tups.pop()
        uids.append(makeUID(uidTup))
    except IndexError:
        break

print(uids)
