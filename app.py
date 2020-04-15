import numpy as np
from PIL import Image
import gc

Image.MAX_IMAGE_PIXELS = 1221120000 

base ='fonts/'
caps=base+"caps/"
cursive=base+"cursive/"
numbers=base+"numbers/"
symbols="fonts/symbols/"
temp='temp/'
no_of_characters_per_line = 50 #set how many char to add per line
no_of_lines_per_page = 35       #set how many lines to add per page
#create lines
def make_line(list1,count):
 imgs    = [ Image.open(i) for i in list1 ]
 #min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
 print("making line "+str(count))
 min_shape=(10*20,10*30)
 imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
 imgs_comb = Image.fromarray( imgs_comb)
 imgs_comb.save( temp+str(count)+'.png' ) 
 del imgs_comb
 imgs=[]
 gc.collect()
 print("made") 

 #combine each line 
def make_page(img_list,filename):
 list1=img_list
 imgs    = [ Image.open(i) for i in list1 ]
 min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
# min_shape=(300*y,200*y)
 imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
 imgs_comb = Image.fromarray( imgs_comb)
 imgs_comb.save(filename)
 img = Image.open(filename)
 x, y = 2480,3508 #page size
 img = img.resize((x,y),Image.ANTIALIAS)
 img.save(filename,quality=55)
 
 

x=open("text.txt","r")
#print("ENTER TEXT TO CONVERT")
#x.write(input()+"\n")
list1=[]
listx=[i for i in x.read()]
listx=listx[3:]
listx.insert(0,"\n")

#adding \n after every "no_of_characters_per_line" letters
for i in range(0,len(listx)):
 if i%(no_of_characters_per_line-1)==0:
   if(i==0) :
     pass
    
   else:
     listx.insert(i+1,"\n")

#adding line break in the end of the listx
if '\n' in listx[-1]:
    pass
else:
    listx.append('\n')

print(listx)

#print(listx)
y=0
count=0
for i in listx:
 if len(list1)==0:
  list1.append('fonts/space.png')
 
  
 if i=='\n':        #counting linebreaks and completing "no_of_characters_per_line" letters in each line 
  count=count+1
  list1.append('fonts/space.png')

  
   
  if(len(list1)<no_of_characters_per_line):
   for i in range(len(list1),no_of_characters_per_line,1):
    list1.append('fonts/space.png')
  make_line(list1,count) #creating a line
  del list1
  list1=[]
  continue

#checking the type of input and appending png in list1
 if(i>='a' and i<= 'z'):
   
   z=cursive+i.lower()+".png"

 elif(i>='A' and i<='Z') :
   
   z=caps+i.lower()+".png"

 elif(i>="0" and i<="9") :
   
   z=numbers+i.lower()+".bmp"

 elif i==":":
   z=symbols+"colon.bmp"
 
 elif i==";":
   z=symbols+"semicolon.bmp"
 
 elif i==".":
   z=symbols+"dot.bmp"

 elif i==",":
   z=symbols+"comma.bmp"

 elif i=='-':
   z=symbols+"dash.bmp"
 
 elif i==')':
   z=symbols+"rbr.bmp" 
 
 elif i=='(':
   z=symbols+"rbl.bmp" 
 
 elif i=='"':
   z=symbols+"apostrophe.bmp" 

 elif i=="'":
   z=symbols+"singleapostrophe.bmp"
 
 elif i=="&":
   z=symbols+"and.bmp"
 
 elif i=="!":
   z=symbols+"exclamation.bmp"
 
 elif i=="?":
   z=symbols+"questionmark.bmp"  

 else: 
  z=base+'space.png'
 list1.append(z)
 y=y+1

#appending all lines in list1 
for i in range(1,count+1,1):
  z=temp+str(i)+".png"
  list1.append(z)

#merging all lines; 35 lines per page
list2=[]
i=0
c=1
while(len(list1)!=0):
  
  if i>=0 and i<no_of_lines_per_page and len(list1)!=0:
    list2.append(list1[i])
    i+=1
    #print("appending"+str(i))
    
    if len(list2)==no_of_lines_per_page:    #make page if all lines completed
      make_page(list2,"final"+str(c)+".png")
      print("made page "+str(c))
      c+=1
      list2=[]
      continue

    elif len(list1)-len(list2)==0:    #make page after end of list1
      if len(list2)<no_of_lines_per_page:
        for i in range(len(list2),no_of_lines_per_page):
          list2.append(base+"line.png")
      make_page(list2,"final"+str(c)+".png")
      print("made page "+str(c))
      list2.clear
      list1.clear
      print("done")
      break
  

  else:       #remove previous 35 lines from list1 after making each page and set i=0
    if len(list1)!=0:
      list1=list1[i:]
      i=0 




