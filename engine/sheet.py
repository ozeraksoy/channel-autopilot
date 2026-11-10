import sys,glob,os
from PIL import Image
ep=sys.argv[1];ts=sys.argv[2:]
ims=[Image.open(f'{ep}/chk/{t}.jpg').resize((270,480)) for t in ts]
W=Image.new('RGB',(270*8,480*((len(ims)+7)//8)),'white')
for i,im in enumerate(ims):W.paste(im,((i%8)*270,(i//8)*480))
W.save(f'{ep}/sheet.jpg',quality=80)
