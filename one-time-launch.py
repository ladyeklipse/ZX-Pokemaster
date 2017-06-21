#31 FOR i=65216 TO 65471 STEP 2: POKE i,237: POKE i+1,160: NEXT i
for i in range(65216, 65471, 2):
    print('M 8 '+str(i)+' 237 0')
    print('M 8 '+str(i+1)+' 160 0')