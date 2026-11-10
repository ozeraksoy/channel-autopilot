# python3 engine/sheet.py <episode_dir> <t1> <t2> ... -> sheet.jpg (contact sheet of the control frames in chk/)
import sys
from PIL import Image
ep=sys.argv[1];ts=sys.argv[2:]
first=Image.open(f'{ep}/chk/{ts[0]}.jpg');land=first.width>first.height
tw,th,cols=(480,270,4) if land else (270,480,8)
ims=[Image.open(f'{ep}/chk/{t}.jpg').resize((tw,th)) for t in ts]
W=Image.new('RGB',(tw*cols,th*((len(ims)+cols-1)//cols)),'white')
for i,im in enumerate(ims):W.paste(im,((i%cols)*tw,(i//cols)*th))
W.save(f'{ep}/sheet.jpg',quality=80)
