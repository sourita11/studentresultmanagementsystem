#----------imports--------------
import tkinter

from tkinter import Toplevel,messagebox
from tkinter.ttk import Treeview
from tkinter import ttk
from tkinter import *
import time
import re
import sys
import mysql.connector

#-----------------------------

def trigger1():
    try:
        trigger ='CREATE TRIGGER COUNTSTUDENTS AFTER INSERT ON STUDENT FOR EACH ROW UPDATE studentcount SET studentcount.Students = (studentcount.Students+1)'
        mycursor.execute(trigger)
    except:
        pass
def trigger2():
    try:
        trigger ='CREATE TRIGGER STUDENTCOUNT AFTER DELETE ON STUDENT FOR EACH ROW UPDATE studentcount SET studentcount.Students = (studentcount.Students-1)'
        mycursor.execute(trigger)
    except:
        pass
def addstudent(): #add student window
    def submitadd(): #add student if details correct
        name= nameval.get()
        usn= usnval.get()
        dob= dobval.get()
        gender= genderval.get()
        email= emailval.get()
        deptid= deptidval.get()
        phoneno= phonenoval.get()
                
        try:
            usnformat= re.compile(r"^[0-9a-zA-Z]{3}[0-9]{2}[a-zA-Z]{2}[0-9]{3}$")
            usnmatch= usnformat.search(usn)
            dateformat= re.compile(r"^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$")
            datematch= dateformat.search(dob)
            emailformat= re.compile(r"^[a-zA-Z0-9_.]+@{1}[a-zA-Z0-9.]+$")
            emailmatch= emailformat.search(email)
            genderformat= re.compile(r"^(?:m|M|male|Male|O|o|Other|other|f|F|female|Female)$")
            gendermatch= genderformat.search(gender)
            deptformat= re.compile(r"[1-9]")
            deptmatch= deptformat.search(deptid)
                       
            if ((name=='') or not(name.isalpha)):
                messagebox.showerror('Notification','Please enter valid Name')
            elif (usnmatch == None):
                messagebox.showerror('Notification','Please enter valid USN')
            elif (datematch == None):
                messagebox.showerror('Notification','Please enter valid DOB')
            elif (emailmatch == None):
                messagebox.showerror('Notification','Please enter valid Email ID')
            elif (gendermatch == None):
                messagebox.showerror('Notification','Please enter valid gender')
            elif (deptmatch == None):
                messagebox.showerror('Notification','Please enter valid Department ID')
            elif (len(phoneno)!=10 or phoneno[0] not in '9876'):
                messagebox.showerror('Notification','Please enter a valid 10 digit phone number')
            else:
                trigger1()
                deptid=int(deptid)
                usn=usn.upper()
                name=name.upper()
                email=email.lower()
                insert1 = 'insert into student values(%s,%s,%s,%s,%s,%s,%s)'
                mycursor.execute(insert1,(usn,name,email,dob,gender,deptid,phoneno))
                con.commit()
                res= messagebox.askyesnocancel("Notification","USN {} added successfully...Clear form?".format(usn),parent=addroot)
                if res == True:
                    nameval.set('')
                    usnval.set('')
                    emailval.set('')
                    dobval.set('')
                    genderval.set('')
                    deptidval.set('')
                    phonenoval.set('')
                strr ='select * from student'
                mycursor.execute(strr)
                data = mycursor.fetchall()
                studenttable.delete(*studenttable.get_children())
                for i in data:
                    list1 = [i[0],i[1]]
                    studenttable.insert('',END,values=list1)
                count='select * from studentcount'
                mycursor.execute(count)
                data = mycursor.fetchall()
                for i in data:
                    list2=['TOTAL:',i[0]]
                    studenttable.insert('',END,values=list2)
                
        except:
            messagebox.showerror('Notification','An error occurred...Please try again',parent=addroot)
        
        
    addroot = Toplevel(master=DataEntryFrame)
    addroot.grab_set()
    addroot.geometry('400x470+150+160')
    addroot.title('STUDENT RESULT MANAGEMENT SYSTEM')
    addroot.config(bg='light blue')
    addroot.iconbitmap('icon.ico')
    
    addroot.resizable(False,False)
    #----------Add student labels
    #name
    namelabel = Label(addroot,text='Name : ',bg='white',font=('times',16,'bold'),relief=GROOVE,borderwidth=3,width=15,anchor='w')
    namelabel.place(x=10,y=10)
    #usn
    usnlabel = Label(addroot,text='USN : ',bg='white',font=('times',16,'bold'),relief=GROOVE,borderwidth=3,width=15,anchor='w')
    usnlabel.place(x=10,y=70)
    #DOB
    doblabel = Label(addroot,text='DOB(yyyy-mm-dd):',bg='white',font=('times',16,'bold'),relief=GROOVE,borderwidth=3,width=15,anchor='w')
    doblabel.place(x=10,y=130)
    #email
    emaillabel = Label(addroot,text='Email : ',bg='white',font=('times',16,'bold'),relief=GROOVE,borderwidth=3,width=15,anchor='w')
    emaillabel.place(x=10,y=190)
    #gender
    genderlabel = Label(addroot,text='Gender : ',bg='white',font=('times',16,'bold'),relief=GROOVE,borderwidth=3,width=15,anchor='w')
    genderlabel.place(x=10,y=250)
    #dept_id
    deptidlabel = Label(addroot,text='Department ID : ',bg='white',font=('times',16,'bold'),relief=GROOVE,borderwidth=3,width=15,anchor='w')
    deptidlabel.place(x=10,y=310)
    #phone number
    phonenumlabel = Label(addroot,text='Phone Number : ',bg='white',font=('times',16,'bold'),relief=GROOVE,borderwidth=3,width=15,anchor='w')
    phonenumlabel.place(x=10,y=370)
    #----add student entries
    nameval = StringVar()
    usnval=StringVar()
    dobval=StringVar()
    genderval=StringVar()
    emailval=StringVar()
    deptidval=StringVar()
    phonenoval=StringVar()
    nameentry = Entry(addroot,font=('times',15,'bold'),bd=3,textvariable=nameval)
    nameentry.place(x=210,y=10)
    usnentry = Entry(addroot,font=('times',15,'bold'),bd=3,textvariable=usnval)
    usnentry.place(x=210,y=70)
    dobentry = Entry(addroot,font=('times',15,'bold'),bd=3,textvariable=dobval)
    dobentry.place(x=210,y=130)
    emailentry = Entry(addroot,font=('times',15,'bold'),bd=3,textvariable=emailval)
    emailentry.place(x=210,y=190)
    genderentry = Entry(addroot,font=('times',15,'bold'),bd=3,textvariable=genderval)
    genderentry.place(x=210,y=250)
    deptidentry = Entry(addroot,font=('times',15,'bold'),bd=3,textvariable=deptidval)
    deptidentry.place(x=210,y=310)
    phonenoentry = Entry(addroot,font=('times',15,'bold'),bd=3,textvariable=phonenoval)
    phonenoentry.place(x=210,y=370)
    #------submit button
    submitbtn = Button(addroot,text='Submit',font=('times',15,'bold'),width=20,bd=4,activebackground='blue',activeforeground='white',command=submitadd)
    submitbtn.place(x=110,y=420)
    addroot.mainloop()
def storedprocedure():
    try:
        strr = 'create procedure display() select * from student'
        mycursor.execute(strr)
    except:
        pass  
def deletestudent(): #delete student window 
    def delete(): #delete student if details correct
        name = nameval.get()
        usn= usnval.get()  
        try:
            
            usnformat= re.compile(r"^[0-9a-zA-Z]{3}[0-9]{2}[a-zA-Z]{2}[0-9]{3}$")
            usnmatch= usnformat.search(usn)
            if (usnmatch == None):
                messagebox.showerror('Notification','Please enter valid USN')
            else:
                trigger2()
                usn=usn.upper()
                strr = 'select count(usn) from student where usn=%s'
                mycursor.execute(strr,(usn,))
                for i in mycursor.fetchall():
                    data=i[0]
                if (data != 0):
                    strr = 'delete from student where usn=%s'
                    mycursor.execute(strr,(usn,))
                    con.commit()  
                    res = messagebox.askyesnocancel('Notification',('USN {} Deleted successfully..Clear form?').format(usn),parent=delroot)
                    if(res==True):
                        nameval.set('')
                        usnval.set('')
                    studenttable.delete(*studenttable.get_children())
                    strr ='select * from student'
                    mycursor.execute(strr)
                    data = mycursor.fetchall()
                    for i in data:
                        list1 = [i[0],i[1]]
                        studenttable.insert('',END,values=list1)
                                    
                    count='select * from studentcount'
                    mycursor.execute(count)
                    data = mycursor.fetchall()
                    for i in data:
                        list2=['TOTAL:',i[0]]
                        studenttable.insert('',END,values=list2) 
                    
                else:
                    messagebox.showerror('Notification','USN {} does not exist..'.format(usn),parent=delroot)

        except:
            messagebox.showerror('Notification','An error occurred...Please try again',parent=delroot)
        
        

        
    delroot =Toplevel(master=DataEntryFrame)
    delroot.grab_set()
    delroot.geometry('400x200+125+150')
    delroot.title('STUDENT RESULT MANAGEMENT SYSTEM')
    delroot.config(bg='light blue')
    delroot.iconbitmap('icon.ico')
    
    delroot.resizable(False,False)
    #----------delete student labels
    #usn
    namelabel = Label(delroot,text='Name : ',bg='white',font=('times',16,'bold'),relief=GROOVE,borderwidth=3,width=15,anchor='w')
    namelabel.place(x=10,y=10)
    #usn
    usnlabel = Label(delroot,text='USN : ',bg='white',font=('times',16,'bold'),relief=GROOVE,borderwidth=3,width=15,anchor='w')
    usnlabel.place(x=10,y=70)

    #----delete student entries
    nameval=StringVar()
    usnval=StringVar()
    nameentry = Entry(delroot,font=('times',15,'bold'),bd=3,textvariable=nameval)
    nameentry.place(x=210,y=10)
    usnentry = Entry(delroot,font=('times',15,'bold'),bd=3,textvariable=usnval)
    usnentry.place(x=210,y=70)
    #------submit button
    delbtn = Button(delroot,text='Delete',font=('times',15,'bold'),width=10,bd=4,activebackground='blue',activeforeground='white',command=delete)
    delbtn.place(x=110,y=130)
    delroot.mainloop()
def updateattend(): #update attendance window
    def attend(): #update and display attendance if details correct
        usn=usnval.get()
        course_id=courseval.get()
        taken=takenval.get()
        attended=attendedval.get()
        if taken=='':
            taken = 0
        if attended=='':
            attended=0
        try:
            usnformat= re.compile(r"^[0-9a-zA-Z]{3}[0-9]{2}[a-zA-Z]{2}[0-9]{3}$")
            usnmatch= usnformat.search(usn)
            courseformat=re.compile(r"^[1][0-9][a-zA-Z]+[1-8][0-9]$")
            coursematch= courseformat.search(course_id)
            if (usnmatch == None):
                messagebox.showerror('Notification','Please enter valid USN')
            elif (coursematch == None):
                messagebox.showerror('Notification','Please enter valid Course ID')
            else:
                usn=usn.upper()
                course_id=course_id.upper()
                strr = 'select count(usn) from student where usn=%s'
                mycursor.execute(strr,(usn,))
                for i in mycursor.fetchall():
                    students=i[0]
                if students!=0:
                    strr = 'select count(course_id) from course where course_id=%s'
                    mycursor.execute(strr,(course_id,))
                    for i in mycursor.fetchall():
                        courses=i[0]
                    if courses != 0:
                        strr='delete from attendance where usn=%s and course_id=%s'
                        mycursor.execute(strr,(usn,course_id))
                        strr='insert into attendance values(%s,%s,%s,%s)'
                        mycursor.execute(strr,(usn,course_id,taken,attended))
                        con.commit()
                        res = messagebox.askyesnocancel('Notification',('Attendance for USN {} Added successfully..Clear form?').format(usn),parent=attroot)
                        if(res==True):
                            usnval.set('')
                            courseval.set('')
                            takenval.set('')
                            attendedval.set('')
                        attended=int(attended)
                        taken=int(taken)
                        attendance=(attended/taken)*100
                        studenttable.delete(*studenttable.get_children())
                        name='select s.name,c.course_name from student s, course c where usn=%s and c.course_id=%s'
                        mycursor.execute(name,(usn,course_id))
                        for i in mycursor.fetchall():
                            data=[usn,i[0],course_id,i[1]]
                            studenttable.insert('',END,values=data)
                        list2=['ATTENDANCE:',attendance]
                        studenttable.insert('',END,values=list2)
                    else:
                        messagebox.showerror('Notification',"Course {} does not exist..".format(course_id),parent=attroot)
                else:
                    messagebox.showerror('Notification',"USN {} does not exist..".format(usn),parent=attroot)
            
  
        except:
            messagebox.showerror('Notification',"An error occurred...Please try again",parent=attroot)
        
            
    attroot = Toplevel(master=DataEntryFrame)
    attroot.grab_set()
    attroot.geometry('400x350+125+150')
    attroot.title('STUDENT RESULT MANAGEMENT SYSTEM')
    attroot.config(bg='light blue')
    attroot.iconbitmap('icon.ico')
    
    attroot.resizable(False,False)
    #----------update attendance labels
    #name
    usnlabel = Label(attroot,text='USN : ',bg='white',font=('times',16,'bold'),relief=GROOVE,borderwidth=3,width=15,anchor='w')
    usnlabel.place(x=10,y=10)
   
    courselabel = Label(attroot,text='Course ID : ',bg='white',font=('times',16,'bold'),relief=GROOVE,borderwidth=3,width=15,anchor='w')
    courselabel.place(x=10,y=70)
    takenlabel = Label(attroot,text='Classes taken : ',bg='white',font=('times',16,'bold'),relief=GROOVE,borderwidth=3,width=15,anchor='w')
    takenlabel.place(x=10,y=130)
    attendedlabel = Label(attroot,text='Classes attended : ',bg='white',font=('times',16,'bold'),relief=GROOVE,borderwidth=3,width=15,anchor='w')
    attendedlabel.place(x=10,y=190)
    #----update attendance entries
    usnval=StringVar()
    courseval=StringVar()
    takenval=StringVar()
    attendedval=StringVar()
    usnentry = Entry(attroot,font=('times',15,'bold'),bd=3,textvariable=usnval)
    usnentry.place(x=210,y=10)
    
    courseentry = Entry(attroot,font=('times',15,'bold'),bd=3,textvariable=courseval)
    courseentry.place(x=210,y=70)
    
    takenentry = Entry(attroot,font=('times',15,'bold'),bd=3,textvariable=takenval)
    takenentry.place(x=210,y=130)
    
    attendedentry = Entry(attroot,font=('times',15,'bold'),bd=3,textvariable=attendedval)
    attendedentry.place(x=210,y=190)
    #------submit button
    updatebtn = Button(attroot,text='Update',font=('times',15,'bold'),width=10,bd=4,activebackground='blue',activeforeground='white',command=attend)
    updatebtn.place(x=110,y=250)
    attroot.mainloop()
def updatemarks(): #update marks window
    def marks(): #update and display marks if details correct
        usn=usnval.get()
        course_id=courseval.get()
        iat1=iat1val.get()
        iat2=iat2val.get()
        iat3=iat3val.get()
        iat4=iat4val.get() 
        if iat1=='':
            iat1=0
        if iat2=='':
            iat2=0
        if iat3=='':
            iat3=0
        if iat4=='':
            iat4=0
        iat1,iat2,iat3,iat4=int(iat1),int(iat2),int(iat3),int(iat4)
        iat1=(iat1*4)/5
        iat2=(iat2*4)/5
        iat3=(iat3*4)/5
        iat4=(iat4*4)/5
        finalia=0
        try:
            usnformat= re.compile(r"^[0-9a-zA-Z]{3}[0-9]{2}[a-zA-Z]{2}[0-9]{3}$")
            usnmatch= usnformat.search(usn)
            courseformat=re.compile(r"^[1][0-9][a-zA-Z]+[1-8][0-9]$")
            coursematch= courseformat.search(course_id)
            if (usnmatch == None):
                messagebox.showerror('Notification','Please enter valid USN')
            elif (coursematch == None):
                messagebox.showerror('Notification','Please enter valid Course ID')
            else:
                usn=usn.upper()
                course_id=course_id.upper()
                strr='select exists(select * from marks where usn=%s and course_id=%s)'
                mycursor.execute(strr,(usn,course_id))
                for i in mycursor.fetchall():
                    data=i[0]
                if data==0:
                    strr = 'select count(usn) from student where usn=%s'
                    mycursor.execute(strr,(usn,))
                    for i in mycursor.fetchall():
                        students=i[0]
                    if students!=0:
                        strr = 'select count(course_id) from course where course_id=%s'
                        mycursor.execute(strr,(course_id,))
                        for i in mycursor.fetchall():
                            courses=i[0]
                        if courses != 0:
                            
                            strr='insert into marks values(%s,%s,%s,%s,%s,%s,%s)'
                            mycursor.execute(strr,(usn,course_id,iat1,iat2,iat3,iat4,finalia))
                            strr='update marks set finalia = (((iat1+iat2+iat3+iat4)-least(iat1,iat2,iat3,iat4))/3)'
                            mycursor.execute(strr)
                            con.commit()
                            res = messagebox.askyesnocancel('Notification',('Marks for USN {} Added successfully..Clear form?').format(usn),parent=markroot)
                            if(res==True):
                                usnval.set('')
                                courseval.set('')
                                iat1val.set('')
                                iat2val.set('')
                                iat3val.set('')
                                iat4val.set('') 
                            strr='select m.usn,s.name,m.course_id,c.course_name,m.iat1,m.iat2,m.iat3,m.iat4,m.finalia from marks m,course c,student s where m.usn=%s and s.usn=%s and m.course_id=%s and m.course_id=c.course_id'
                            mycursor.execute(strr,(usn,usn,course_id))
                            studenttable.delete(*studenttable.get_children())
                            for i in mycursor.fetchall():
                                data=[i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]]
                                studenttable.insert('',END,values=data)
                        else:
                            messagebox.showerror('Notification',"Course {} does not exit".format(course_id),parent=markroot)
                    else:
                        messagebox.showerror('Notification',"USN {} does not exist".format(usn),parent=markroot)
                elif data==1:
                    strr='select iat1,iat2,iat3,iat4 from marks where usn=%s and course_id=%s'
                    mycursor.execute(strr,(usn,course_id))
                    for i in mycursor.fetchall():
                        ia1,ia2,ia3,ia4=i[0],i[1],i[2],i[3]

                    if(iat1==0 and iat2==0 and iat3==0 and iat4==0):
                        iat1,iat2,iat3,iat4=ia1,ia2,ia3,ia4
                    elif(iat1==0 and iat2==0 and iat3==0):
                        iat1,iat2,iat3=ia1,ia2,ia3
                    elif(iat1==0 and iat2==0 and iat4==0):
                        iat1,iat2,iat4=ia1,ia2,ia4
                    elif(iat1==0 and  iat3==0 and iat4==0):
                        iat1,iat3,iat4=ia1,ia3,ia4
                    elif(iat2==0 and iat3==0 and iat4==0):
                        iat2,iat3,iat4=ia2,ia3,ia4
                    elif(iat1==0 and iat2==0):
                        iat1,iat2=ia1,ia2
                    elif(iat1==0 and iat3==0):
                        iat1,iat3=ia1,ia3
                    elif(iat1==0 and iat4==0):
                        iat1,iat4=ia1,ia4
                    elif(iat2==0 and iat3==0):
                        iat2,iat3=ia2,ia3
                    elif(iat2==0 and iat4==0):
                        iat2,iat4=ia2,ia4
                    elif(iat3==0 and iat4==0):
                        iat3,iat4=ia3,ia4
                    elif(iat1==0):
                        iat1=ia1
                    elif(iat2==0):
                        iat2=ia2
                    elif(iat3==0 ):
                        iat3=ia3
                    elif(iat4==0):
                        iat4=ia4
                    strr='update marks set iat1=%s,iat2=%s,iat3=%s,iat4=%s,finalia=%s where usn=%s and course_id=%s'
                    mycursor.execute(strr,(iat1,iat2,iat3,iat4,finalia,usn,course_id))
                    strr='update marks set finalia =(((iat1+iat2+iat3+iat4)-least(iat1,iat2,iat3,iat4))/3)'
                    mycursor.execute(strr)
                    con.commit()
                    res = messagebox.askyesnocancel('Notification',('Marks for USN {} Added successfully..Clear form?').format(usn),parent=markroot)
                    if(res==True):
                        usnval.set('')
                        courseval.set('')
                        iat1val.set('')
                        iat2val.set('')
                        iat3val.set('')
                        iat4val.set('') 
                    strr='select m.usn,s.name,m.course_id,c.course_name,m.iat1,m.iat2,m.iat3,m.iat4,m.finalia from marks m,course c,student s where m.usn=%s and s.usn=%s and m.course_id=%s and m.course_id=c.course_id'
                    mycursor.execute(strr,(usn,usn,course_id))
                    studenttable.delete(*studenttable.get_children())
                    for i in mycursor.fetchall():
                        data=[i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]]
                        studenttable.insert('',END,values=data)
              
        except:
            messagebox.showerror('Notification',"An error occurred...Please try again",parent=markroot)              
            
            
    markroot = Toplevel(master=DataEntryFrame)
    markroot.grab_set()
    markroot.geometry('400x450+125+150')
    markroot.title('STUDENT RESULT MANAGEMENT SYSTEM')
    markroot.config(bg='light blue')
    markroot.iconbitmap('icon.ico')
    
    markroot.resizable(False,False)
    #----------update marks labels
    #name
    usnlabel = Label(markroot,text='USN : ',bg='white',font=('times',16,'bold'),relief=GROOVE,borderwidth=3,width=15,anchor='w')
    usnlabel.place(x=10,y=10)
   
    courselabel = Label(markroot,text='Course ID : ',bg='white',font=('times',16,'bold'),relief=GROOVE,borderwidth=3,width=15,anchor='w')
    courselabel.place(x=10,y=70)
    iat1label = Label(markroot,text='IAT-1 : ',bg='white',font=('times',16,'bold'),relief=GROOVE,borderwidth=3,width=15,anchor='w')
    iat1label.place(x=10,y=130)
    iat2label = Label(markroot,text='IAT-2 : ',bg='white',font=('times',16,'bold'),relief=GROOVE,borderwidth=3,width=15,anchor='w')
    iat2label.place(x=10,y=190)
    iat3label = Label(markroot,text='IAT-3 : ',bg='white',font=('times',16,'bold'),relief=GROOVE,borderwidth=3,width=15,anchor='w')
    iat3label.place(x=10,y=250)
    iat4label = Label(markroot,text='IAT-4 : ',bg='white',font=('times',16,'bold'),relief=GROOVE,borderwidth=3,width=15,anchor='w')
    iat4label.place(x=10,y=310)
    #----update marks entries
    usnval=StringVar()
    courseval=StringVar()
    iat1val=StringVar()
    iat2val=StringVar()
    iat3val=StringVar()
    iat4val=StringVar()
    usnentry = Entry(markroot,font=('times',15,'bold'),bd=3,textvariable=usnval)
    usnentry.place(x=210,y=10)
    
    courseentry = Entry(markroot,font=('times',15,'bold'),bd=3,textvariable=courseval)
    courseentry.place(x=210,y=70)
    
    iat1entry = Entry(markroot,font=('times',15,'bold'),bd=3,textvariable=iat1val)
    iat1entry.place(x=210,y=130)
    
    iat2entry = Entry(markroot,font=('times',15,'bold'),bd=3,textvariable=iat2val)
    iat2entry.place(x=210,y=190)
    
    iat3entry = Entry(markroot,font=('times',15,'bold'),bd=3,textvariable=iat3val)
    iat3entry.place(x=210,y=250)
    
    iat4entry = Entry(markroot,font=('times',15,'bold'),bd=3,textvariable=iat4val)
    iat4entry.place(x=210,y=310)
    #------submit button
    updatebtn = Button(markroot,text='Update',font=('times',15,'bold'),width=10,bd=4,activebackground='blue',activeforeground='white',command=marks)
    updatebtn.place(x=110,y=370)
    markroot.mainloop()

def adminmenu(): #menu after admin login
    menuroot = Toplevel(master = DataEntryFrame)
    menuroot.geometry('400x450+100+100')
    menuroot.config(bg='gray20')
    menuroot.iconbitmap('icon.ico')
    menuroot.grab_set()
    menuroot.resizable(False,False)
    #----------------admin menu buttons
    addstudentbtn=Button(menuroot,text='Add Student',width=20,font=('helvetica',20,'bold'),bd=6,bg='light blue',activebackground='skyblue3',relief=RIDGE,activeforeground='white',command=addstudent)
    addstudentbtn.pack(side=TOP,expand=True)
    deletestudentbtn=Button(menuroot,text='Delete Student',width=20,font=('helvetica',20,'bold'),bd=6,bg='light blue',activebackground='skyblue3',relief=RIDGE,activeforeground='white',command=deletestudent)
    deletestudentbtn.pack(side=TOP,expand=True)
    attendancebtn=Button(menuroot,text='Update Attendance',width=20,font=('helvetica',20,'bold'),bd=6,bg='light blue',activebackground='skyblue3',relief=RIDGE,activeforeground='white',command=updateattend)
    attendancebtn.pack(side=TOP,expand=True)
    marksbtn=Button(menuroot,text='Update Marks',width=20,font=('helvetica',20,'bold'),bd=6,bg='light blue',activebackground='skyblue3',relief=RIDGE,activeforeground='white',command=updatemarks)
    marksbtn.pack(side=TOP,expand=True)
    gobackbtn=Button(menuroot,text='Go Back',width=10,font=('helvetica',20,'bold'),bd=6,bg='light blue',activebackground='skyblue3',relief=RIDGE,activeforeground='white',command=menuroot.destroy)
    gobackbtn.pack(side=TOP,expand=True)
    menuroot.mainloop()


def adminlogin(): #admin login wwindow
    def checklogin(): #check login credential, display menu if correct
        id = adminval.get()
        pwd = passwordval.get()
        try:
            strr='use studentresultsystem'
            mycursor.execute(strr)
            if (id=='admin' and pwd=='123'):
                messagebox.showinfo('Notification','Successfully logged in')
                adminroot.destroy()  
                adminmenu()  
            else:
                messagebox.showerror('Notification','Incorrect User ID/Password! Please try again')
        except:
            messagebox.showerror('Notification','Please connect to database')
    adminroot = Toplevel(master = DataEntryFrame)
    adminroot.geometry('450x250+100+200')
    adminroot.title('STUDENT RESULT MANAGEMENT SYSTEM')
    adminroot.config(bg='gray10')
    adminroot.grab_set()
    adminroot.iconbitmap('icon.ico')
    
    adminroot.resizable(False,False)
    
    #----------------admin login labels
    idlabel = Label(adminroot,text='User ID :',bg='alice blue',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=11,anchor='w')
    idlabel.place(x=10,y=10)
    pwdlabel = Label(adminroot,text='Password :',bg='alice blue',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=11,anchor='w')
    pwdlabel.place(x=10,y=70)
    #-------------------admin entry values
    adminval = StringVar()
    adminentry = Entry(adminroot,font=('times',15,'bold'),bd=5,textvariable=adminval)
    adminentry.place(x=220,y=10)
    passwordval = StringVar()
    passwordentry = Entry(adminroot,font=('times',15,'bold'),bd=5,textvariable=passwordval)
    passwordentry.place(x=220,y=70)

    #------login button
    loginbutton = Button(adminroot,text='Login',font=('helvetica',15,'bold'),width=20,activebackground='cyan2',command=checklogin)
    loginbutton.place(x=70,y=130)
    adminroot.mainloop()

def studentlogin(): 
    
    def showdata(): #if entered data correct, display data
              
        usn=usnval.get()
        sem=semval.get()

        
        try:
            strr='use studentresultsystem'
            mycursor.execute(strr)
        
            usnformat= re.compile(r"^[0-9a-zA-Z]{3}[0-9]{2}[a-zA-Z]{2}[0-9]{3}$")
            usnmatch= usnformat.search(usn)
            semformat=re.compile(r"[1-8]{1}")
            semmatch = semformat.search(sem)
            if (usnmatch == None):
                messagebox.showerror('Notification','Please enter valid USN')
            elif (semmatch == None):
                messagebox.showerror('Notification','Please enter valid semester')

            else:
                result = 'select m.usn,s.name,c.course_id,c.course_name,m.iat1,m.iat2,m.iat3,m.iat4,m.finalia from marks m, student s, course c,semester se\
                where se.semester=%s and m.usn=%s and s.usn=%s and se.course_id=c.course_id and se.course_id=m.course_id order by course_id'
                mycursor.execute(result,(sem,usn,usn))
                data = mycursor.fetchall()
                if data==[]:
                    messagebox.showerror('Notification',"Data unavailabale...")
                else:
                    studenttable.delete(*studenttable.get_children())
                    for i in data:
                        list1 = [i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]]
                        studenttable.insert('',END,values=list1)
        except:
            messagebox.showerror('Notification',"Please connect to database..",parent=studentroot)   
           

    studentroot = Toplevel(master = DataEntryFrame)
    studentroot.grab_set()
    studentroot.geometry('450x250+100+200')
    studentroot.title('STUDENT RESULT MANAGEMENT SYSTEM')
    studentroot.config(bg='gray1')
    studentroot.iconbitmap('icon.ico')
    
    studentroot.resizable(False,False)
    
    #----------------student login labels
    usnlabel = Label(studentroot,text='Enter USN :',bg='alice blue',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=13,anchor='w')
    usnlabel.place(x=10,y=10)
    semlabel = Label(studentroot,text='Enter semester :',bg='alice blue',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=13,anchor='w')
    semlabel.place(x=10,y=70)
    #-------------------student entry values
    usnval = StringVar()
    semval = StringVar()
    usnentry = Entry(studentroot,font=('times',15,'bold'),bd=5,textvariable=usnval)
    usnentry.place(x=250,y=10)
    
    sementry = Entry(studentroot,font=('times',15,'bold'),bd=5,textvariable=semval)
    sementry.place(x=250,y=70)
    

    #------check button
    checkbutton = Button(studentroot,text='Check result',font=('helvetica',15,'bold'),width=20,activebackground='cyan2',command=showdata)
    checkbutton.place(x=70,y=130)
    studentroot.mainloop()

def exitwindow(): #exit app pop-up
    res = messagebox.askyesnocancel('Notification','Do you want to exit?')
    if(res == True):
        root.destroy()



##----------------------connect database

def connectdb():
    
    def submitdb():
        global con, mycursor
        host = hostval.get()
        user = userval.get()
        password = passwordval.get()
        
        try:
            con = mysql.connector.connect(host=host,user=user,password=password)
            mycursor = con.cursor()
            dbroot.destroy()
            messagebox.showinfo('Notification','Successfully connected to database')           
            
            
        except:
            messagebox.showerror('Notification','Data is incorrect! Please try again')
            return
        try:
            createdb = 'create database studentresultsystem'
            mycursor.execute(createdb)
            usedb = 'use studentresultsystem'
            mycursor.execute(usedb)
            createtable1 = 'create table department(department_id int primary key,department_name varchar(60))' 
            mycursor.execute(createtable1)
            insertdept = "insert into department values(1,'CIVIL ENGINEERING'),\
            (2,'COMPUTER SCIENCE ENGINEERING'),(3,'ELECTRICAL AND ELECTRONICS ENGINEERING'),\
            (4,'ELECTRONICS AND COMMUNICATION ENGINEERING'),(5,'INFORMATION SCIENCE AND ENGINEERING'),\
            (6,'MECHANICAL ENGINEERING')"
            mycursor.execute(insertdept)
            createtable2 = 'create table course(course_id varchar(10) primary key,course_name varchar(60), credits int)'
            mycursor.execute(createtable2)
            insertcourse ="insert into course values('18CIV14','ELEMENTS OF CIVIL ENGINEERING AND MECHANICS',3),\
            ('18CIV59','ENVIRONMENTAL STUDIES',1),\
            ('18CPC39','CONSTITUTION OF INDIA,PROFESSIONAL ETHICS AND CYBER LAW',1),\
            ('18CS32','DATA STRUCTURES AND APPLICATIONS',4),('18CS33','ANALOG AND DIGITAL ELECTRONICS',3),\
            ('18CS34','COMPUTER ORGANIZATION',3),('18CS35','SOFTWARE ENGINEERING',3),('18CS36','DISCRETE MATHEMATICAL STRUCTURES',3),\
            ('18CS51','MANAGEMENT AND ENTREPRENEURSHIP FOR IT INDUSTRY',3),\
            ('18CS52','COMPUTER NETWORKS AND SECURITY',4),('18CS53','DATABASE MANAGEMENT SYSTEM',4),\
            ('18CS54','AUTOMATA THEORY AND COMPUTABILITY',3),('18CS55','APPLICATION DEVELOPMENT WITH PYTHON',3),\
            ('18CS56','UNIX PROGRAMMING',3),('18CSL37','DATA STRUCTURES LABORATORY',2),\
            ('18CSL38','ANALOG AND DIGITAL ELECTRONICS LABORATORY',2),\
            ('18CSL57','COMPUTER NETWORKS LABORATORY',2),('18CSL58','DBMS LABORATORY',2),\
            ('18EGDL15','ENGINEERING GRAPHICS',3),('18EGH18','TECHNICAL ENGLISH-I',1),\
            ('18ELE13','BASIC ELECTRICAAL ENGINEERING',3),('18ELEL17','BASIC ELECTRICAL ENGINEERING LABORATORY',1),\
            ('18MAT11','CALCULUS AND LINEAR ALGEBRA',4),('18MAT31','TRANSFORM CALCULUS, FOURIER SERIES AND NUMERICAL TECHNIQUES',3),\
            ('18PHY12','ENGINEERING PHYSICS',2),('18PHYL16','ENGINEERING PHYSICS LABORATORY',1),\
            ('18IS51','MANAGEMENT AND ENTREPRENEURSHIP FOR IT INDUSTRY',3),\
            ('18IS52','COMPUTER NETWORKS AND SECURITY',4),('18IS53','DATABASE MANAGEMENT SYSTEM',4),\
            ('18IS54','AUTOMATA THEORY AND COMPUTABILITY',3),('18IS55','APPLICATION DEVELOPMENT WITH PYTHON',3),\
            ('18IS56','UNIX PROGRAMMING',3),('18ISL37','DATA STRUCTURES LABORATORY',2),\
            ('18ISL38','ANALOG AND DIGITAL ELECTRONICS LABORATORY',2),\
            ('18ISL57','COMPUTER NETWORKS LABORATORY',2),('18ISL58','DBMS LABORATORY',2),\
            ('18IS32','DATA STRUCTURES AND APPLICATIONS',4),('18IS33','ANALOG AND DIGITAL ELECTRONICS',3),\
            ('18IS34','COMPUTER ORGANIZATION',3),('18IS35','SOFTWARE ENGINEERING',3),('18IS36','DISCRETE MATHEMATICAL STRUCTURES',3)"
            mycursor.execute(insertcourse)
            createtable7 = 'create table semester(semester int NOT NULL, course_id varchar(10),foreign key(course_id) references course(course_id) on delete cascade)'
            mycursor.execute(createtable7)
            insertsem = "insert into semester values(5,'18CIV59'),\
            (3,'18CPC39'),(3,'18CS32'),(3,'18CS33'),(3,'18CS34'),(3,'18CS35'),(3,'18CS36'),\
            (5,'18CS51'),(5,'18CS52'),(5,'18CS53'),(5,'18CS54'),(5,'18CS55'),\
            (5,'18CS56'),(3,'18CSL37'),(3,'18CSL38'),(5,'18CSL57'),(5,'18CSL58'),\
            (3,'18IS32'),(3,'18IS33'),(3,'18IS34')"
            mycursor.execute(insertsem)
            createtable4 =  'create table student(usn varchar(10) primary key, name varchar(40), email varchar(30) UNIQUE,dob date,gender varchar(6),department_id int, phonenumber varchar(10),foreign key(department_id) references department(department_id) on delete cascade)'
            mycursor.execute(createtable4)
            createtable5 =  'create table attendance(usn varchar(10),course_id varchar(10),classes_taken int,classes_attended int,foreign key(usn) references student(usn) on delete cascade,foreign key(course_id) references course(course_id) on delete cascade)'
            mycursor.execute(createtable5)
            createtable6 = 'create table marks(usn varchar(10),course_id varchar(10),iat1 int,iat2 int,iat3 int,iat4 int,finalia int,foreign key(usn) references student(usn) on delete cascade,foreign key(course_id) references course(course_id) on delete cascade)'
            mycursor.execute(createtable6)
            strr = 'create table studentcount(Students int)'
            mycursor.execute(strr)
            strr = 'insert into studentcount values(0)'
            mycursor.execute(strr)      
            trigger1()
            trigger2()
            storedprocedure()

        except:
            strr = 'use studentresultsystem'
            mycursor.execute(strr)
    
    dbroot = Toplevel()
    dbroot.grab_set()
    dbroot.geometry('470x250+650+230')
    dbroot.iconbitmap('icon.ico')

    dbroot.resizable(False,False)
    dbroot.config(bg='gray1')
    #---------------labels
    hostlabel = Label(dbroot,text='Host : ',bg='alice blue',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=11,anchor='w')
    hostlabel.place(x=10,y=10)
    userlabel = Label(dbroot,text='Username : ',bg='alice blue',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=11,anchor='w')
    userlabel.place(x=10,y=70)
    passwordlabel = Label(dbroot,text='Password : ',bg='alice blue',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=11,anchor='w')
    passwordlabel.place(x=10,y=130)

    #-----------db entry
    hostval = StringVar()
    hostentry = Entry(dbroot,font=('times',15,'bold'),bd=5,textvariable=hostval)
    hostentry.place(x=250,y=10)
    userval = StringVar()
    userentry = Entry(dbroot,font=('times',15,'bold'),bd=5,textvariable=userval)
    userentry.place(x=250,y=70)
    passwordval = StringVar()
    passwordentry = Entry(dbroot,font=('times',15,'bold'),bd=5,textvariable=passwordval)
    passwordentry.place(x=250,y=130)

    #------submit button
    submitbutton = Button(dbroot,text='Submit',font=('times',15,'bold'),width=12,activebackground='sky blue',command= submitdb)
    submitbutton.place(x=210,y=190)
    

    dbroot.mainloop()

def tick(): #date time clock
    time_string=time.strftime("%H:%M:%S")
    date_string=time.strftime("%d-%m-%Y")
    clock.config(text='Date : '+date_string+'\nTime : '+time_string)
    clock.after(125,tick)
def IntroLabelTick(): #intro slider label
    global count,text
    if (count>=len(heading)):
        Sliderlabel.config(text=heading)
    else:
        text += heading[count]
        Sliderlabel.config(text=text)
        count += 1
    Sliderlabel.after(125,IntroLabelTick)


##################################################################

root = Tk()
root.title("STUDENT RESULT MANAGEMENT SYSTEM")

root.config(background='gray28')
root.geometry('1174x650+75+60')
root.iconbitmap('icon.ico')
root.resizable(False,False)
#################################################################
#Frames
DataEntryFrame = Frame(root,bg = 'gray75',relief = GROOVE,borderwidth = 5)
DataEntryFrame.place(x=10,y=80,width=500,height=400)
#----------------------dataentry intro frame
frontlabel = Label(DataEntryFrame,text='----------------Welcome----------------',width=30,font=('arial',20,'italic bold'),bg='lightsteelblue2')
frontlabel.pack(side=TOP,expand=True)
adminbtn=Button(DataEntryFrame,text='Admin Login',width=25,font=('helvetica',20,'bold'),bd=6,bg='alice blue',activebackground='slategray4',relief=RIDGE,activeforeground='white',command=adminlogin)
adminbtn.pack(side=TOP,expand=True)
studentbtn=Button(DataEntryFrame,text='Student Result',width=25,font=('helvetica',20,'bold'),bd=6,bg='alice blue',activebackground='slategray4',relief=RIDGE,activeforeground='white',command=studentlogin)
studentbtn.pack(side=TOP,expand=True)
exitbtn=Button(DataEntryFrame,text='Exit',width=25,font=('helvetica',20,'bold'),bd=6,bg='alice blue',activebackground='slategray4',relief=RIDGE,activeforeground='white',command=exitwindow)
exitbtn.pack(side=TOP,expand=True)
#-------------------------------------
ShowDataFrame = Frame(root,bg = 'gray90',relief = GROOVE,borderwidth = 5)

ShowDataFrame.place(x=550,y=80,width=620,height=500)
#############################################################################
style = ttk.Style()
style.configure('Treeview.Heading',font=('helvetica',15,'bold'),foreground='sky blue')
style.configure('Treeview',font=('times',10,'bold'),foreground='black')
scroll_x= Scrollbar(ShowDataFrame,orient=HORIZONTAL)
scroll_y= Scrollbar(ShowDataFrame,orient=VERTICAL)
studenttable = Treeview(ShowDataFrame,columns=('USN','NAME','COURSE_ID','COURSE_NAME','IAT-1','IAT-2','IAT-3','IAT-4','FINAL'),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)
scroll_x.pack(side=BOTTOM,fill=X)
scroll_y.pack(side=RIGHT,fill=Y)
scroll_x.config(command=studenttable.xview)
scroll_y.config(command=studenttable.yview)
studenttable.heading('USN',text='USN')
studenttable.heading('NAME',text='NAME')
studenttable.heading('COURSE_ID',text='COURSE')
studenttable.heading('COURSE_NAME',text='COURSE NAME')
studenttable.heading('IAT-1',text='IAT-1')
studenttable.heading('IAT-2',text='IAT-2')
studenttable.heading('IAT-3',text='IAT-3')
studenttable.heading('IAT-4',text='IAT-4')
studenttable.heading('FINAL',text='FINAL IAT')
studenttable['show']='headings'
studenttable.column('USN',width=150)
studenttable.column('NAME',width=200)
studenttable.column('COURSE_ID',width=110)
studenttable.column('COURSE_NAME',width=275)
studenttable.column('IAT-1',width=110)
studenttable.column('IAT-2',width=110)
studenttable.column('IAT-3',width=110)
studenttable.column('IAT-4',width=110)
studenttable.column('FINAL',width=120)


studenttable.pack(fill=BOTH,expand=1)

heading = "WELCOME TO STUDENT RESULT SYSTEM"
count = 0
text= ''
Sliderlabel = Label(root,text=heading,font=('helvetica',20,'italic bold'),relief=RIDGE,borderwidth=4,width=35,bg='light grey')
Sliderlabel.place(x=260,y=0)
IntroLabelTick()
clock = Label(root,font=('times',14,'bold'),relief=RIDGE,borderwidth=4,bg='lightskyblue2')
clock.place(x=0,y=0)
tick()
connectbutton = Button(root,text='Connect to Database',width=23,font=('helvetica',12,'italic bold'),borderwidth=4,bg='palegreen2',activebackground='blue2',activeforeground='white',command=connectdb)
connectbutton.place(x=930,y=0)

root.mainloop()