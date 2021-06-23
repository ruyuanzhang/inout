#  create faceprf design
'''
20210526 RYZ create it 
'''
import numpy as np
import matplotlib.pyplot as plt
from RZutilpy.rzio import loadpkl

nFaces = 95 # number of faces in total
nViews = 7 # number of views in total
nPosi = 25 # number of positions
blank = 15 # secs
nBlankTrial = 10
nRun = 12 # number of runs

posiCondList,imageIdList, digitList = [],[],[]
for iRun in range(int(nRun/2)):

    # 50 trials + 10 blank trials
    posiCond = np.hstack([np.arange(nPosi), np.arange(nPosi), np.ones(nBlankTrial)*-1])
    while True:
        np.random.shuffle(posiCond)
        idx=np.where(posiCond==-1)[0] # find idx of blank trials
        # make sure blank trials not 1st trial, not last trial, not two consecutive trials
        if idx[0]!=0 and idx[-1]!=posiCond.size-1 and (np.diff(idx)!=1).all():
            break

    imageId = np.ones((posiCond.size, 5)) * -1
    # create face orders:
    for i in range(posiCond.size):
        # sample the first face
        f1 = np.random.randint(nFaces)
        view1 = np.random.randint(nViews)
        id1 = f1*nViews + view1
        
        # sample the second
        repeat1 = (np.random.rand() < 0.25)
        if repeat1:
            while 1:
                view2 = np.random.randint(nViews)
                if view2!=view1:
                    break            
            id2 = f1*nViews+view2
        else:
            f2 = np.random.randint(nFaces)
            view2 = np.random.randint(nViews)
            id2 = f2*nViews + view2
        
        # sample the third
        repeat2 = (np.random.rand() < 0.25)
        if repeat2:
            while 1:
                view3 = np.random.randint(nViews)
                if view3!=view2:
                    break            
            id3 = f2*nViews+view3
        else:
            f3 = np.random.randint(nFaces)
            view3 = np.random.randint(nViews)
            id3 = f3*nViews + view3
        
        # sample the third
        repeat3 = (np.random.rand() < 0.25)
        if repeat3:
            while 1:
                view4 = np.random.randint(nViews)
                if view4!=view3:
                    break            
            id4 = f3*nViews+view4
        else:
            f4 = np.random.randint(nFaces)
            view4 = np.random.randint(nViews)
            id4 = f4*nViews + view4

        if not any([repeat1, repeat2, repeat3]): # no
            repeat_tmp = np.random.randint(3)
            if repeat_tmp==0: # insert event on 2nd face
                while 1:
                    view2 = np.random.randint(nViews)
                    if view2!=view1:
                        break            
                id2 = f1*nViews+view2
            elif repeat_tmp==1:
                while 1:
                    view3 = np.random.randint(nViews)
                    if view3!=view2:
                        break            
                id3 = f2*nViews+view3
            elif repeat_tmp==2:
                while 1:
                    view4 = np.random.randint(nViews)
                    if view4!=view3:
                        break            
                id4 = f3*nViews+view4
        
        imageId[i, 0:4]=id1, id2, id3, id4

    imageId[posiCond==-1,:] = -1
    imageId = imageId.flatten()
    imageId = np.hstack((np.ones(blank)*-1, imageId, np.ones(blank)*-1))
    imageId = np.repeat(imageId, 2) # 0.5 secs per mriframe
    imageId = imageId.astype('int')
    # deal with position
    posiCond = np.hstack((np.ones(3)*-1, posiCond, np.ones(3)*-1))
    posiCond = np.repeat(posiCond, 10) # 0.5 secs per mriframe
    posiCond = posiCond.astype('int')

    #  
    imageIdList.append(imageId.copy())
    posiCondList.append(posiCond.copy())

    # create a digit procedure. digit within [0, 9]
    digits=[np.random.randint(10)] 
    for d in range(1, posiCond.size):
        rep = (np.random.rand()<1/11.32)
        if rep:
            digits.append(digits[d-1])
        else:
            while 1:
                tmp = np.random.randint(10)
                if tmp!=digits[d-1]:
                    break
            digits.append(tmp)
    posiCondList.append(digitList.copy())
        
    
imageIdList = imageIdList + imageIdList[::-1] # we reverse the order of the run
posiCondList = posiCondList + posiCondList[::-1]
digitList = digitList + digitList[::-1]

# load images
images = loadpkl('images.pkl')
images = images['images']

#np.savez('faceprfdesign2', imageIdList=imageIdList, posiCondList=posiCondList,images=images)

