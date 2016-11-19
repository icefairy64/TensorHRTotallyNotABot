def create_new_user(id,name,surname):
    import os
    y=os.getcwd()+'/info_candidats'
    create_new(y)
    b=os.getcwd()+'/info_candidats/'+id
    create_new(b)
    f=file(name+'_'+surname+'_perepiska'+'.html','wb')
    write_characteristic(f)
def get_info_user(id):
    f = file('*_perepiska.html')
    str="</BODY></HTML>"
    f.write("<b>" + str + "</br>")
    f.close()
def write_characteristic(id,message):
    str = "<HTML><BODY><TITLE>" + Name + " " + surname + "<br><\TITlE>"
    f.write(str)
    f.close()
def write_message(id,message):
    f=file('*_perepiska.html')
    f.write("<b>"+str+"=>"+"</b>")
    f.close()
def write_answer(id,message):
    f=file('*_perepiska.html')
    f.write("<b>"+str+"</br>")
    f.close()
def create_new(y):
    print(y)
    os.mkdir(y)
