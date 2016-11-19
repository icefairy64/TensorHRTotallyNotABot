def create_new_user(id,name,surname):
    import os
    y=os.getcwd()+'/info_candidats'
    create_new(y)
    b=os.getcwd()+'/info_candidats/'+id
    create_new(b)
    f=file(name+'_'+surname+'_perepiska'+'.html','wb')
    str = "<HTML><BODY><TITLE>" + Name + " " + surname + "<br><\TITlE>"
    f.write(str)
    f.close()
def get_info_user(id):
    f = file(id+'*_perepiska.html')
    str="</BODY></HTML>"
    f.write("<b>" + str + "</br>")
    f.close()
def write_characteristic(id,message):
   print('pusto')
def write_message(id,message):
    f=file(id+'*_perepiska.html')
    f.write("<b>"+message+"=>"+"</b>")
    f.close()
def write_answer(id,message):
    f=file(id+'*_perepiska.html')
    f.write("<b>"+message+"</br>")
    f.close()
def create_new(y):
    print(y)
    os.mkdir(y)
