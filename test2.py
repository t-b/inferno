tups=[('Demo',1),('Demo',1),('Demo',1),('Demo',1),('Demo',1),('Demo',1)]
uid_count = 0
uids=[]
for uniqueID in uids:
    if uniqueID.count('Demo'):
        uid_count += .5
demo_count = uid_count // 2
return serial+'%s'%(demo_count+1)

def getMC():
    s=serials.pop()
