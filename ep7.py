from tkinter import *
from tkinter import ttk, messagebox
import csv
from datetime import datetime


GUI = Tk()
GUI.title("Program บันทึกค่าใช้จ่าย By Yingnaja V.1.0")
GUI.geometry('600x550+500+50')

####################### MENU BAR #########################
menubar = Menu(GUI)
GUI.config(menu=menubar)

# File menu
filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Export to googlesheet')
# Help menu
def About():
    print('About_menu')
    messagebox.showinfo('About','สวัสดีครับ \n สนใจติต่อ 0897513041')
    
helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=About)
helpmenu.add_command(label='Read Me')
# Donate menu
donatemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donate',menu=donatemenu)

##########################################################
Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH, expand=1)

icon_t1 = PhotoImage(file='list.png') # .subsample ใช้สำหรับย่อรูปคิดเป็นเท่า
icon_t2 = PhotoImage(file='list2.png')

Tab.add(T1, text=f'{"ค่าใช้จ่าย": ^{25}}', image=icon_t1,compound='top')
Tab.add(T2, text=f"{'ค่าใช้จ่ายทั้งหมด': ^{25}}", image=icon_t2,compound="top")

F1 = Frame(T1)
F1.pack(pady=10)

day = {'Mon':'จันทร์',
        'Tue':'อังคาร',
        'Wed':'พุธ',
        'Thu':'พฤหัสบดี',
        'Fri':'ศุกร์',
        'Sat':'เสาร์',
        'Sun':'อาทิตย์'
        }

def Save(event=None):
    expense = V_expense.get()
    price = V_price.get()
    pic = V_pic.get()

    if expense =="":
        messagebox.showwarning('Error','กรุณากรอกรายการ')
        return
    elif price == '':
        messagebox.showwarning('Error', 'กรูณากรอกราคา')
        return
    elif pic == '':
        messagebox.showwarning('Error', 'กรูณากรอกจำนวนสินค้า')

    try:
        total = int(price) * int(pic)
        today = datetime.now().strftime('%a')
        dt = datetime.now().strftime('%Y-%m-%d %H: %M: %S')
        dt = day[today] + '' + dt
        print(f"รายการ: {expense} ราคา {price} บาท จำนวน {pic} จาน รวมเป็นเงิน {total} บาท")
        text = f'รายการ: {expense} ราคา: {price} บาท \n'
        text = text + f'จำนวน: {pic} รายการ รวมทั้งหมด: {total} บาท'
        v_rerult.set(text)
        V_expense.set("")
        V_price.set("")
        V_pic.set("")
        # บันทึกข้อมูลลง CSV
        with open('savedata.csv', 'a',encoding='utf-8', newline='') as f:
            fw = csv.writer(f)
            data = [dt, expense, price, pic, total]
            fw.writerow(data)
        #ทำให้เคอเซอร์ กลับไปตำแหน่งช่องกรอกแรก
        E1.focus()
        update_table()
    except:
        print('ERROR')
        #messagebox.showerror('Error', 'คุณกรอกตัวเลขผิด')
        messagebox.showwarning('Error', 'คุณกรอกข้อความผิด')
        V_expense.set("")
        V_price.set("")
        V_pic.set("")
# กด Enter
GUI.bind('<Return>', Save) #ต้องเพิ่ม def Save(event=None): 

def Show():
    pic = V_pic.get()
    result = int(price) * int(pic)
    print(f"รายการ: {expense} ราคา {price} บาท จำนวน {pic} จาน รวมเป็นเงิน {result} บาท")

FONT1 = (None, 16)
FONT2 = (None, 14)

shopping = PhotoImage(file='shop.png')
shoppic = ttk.Label(F1, image=shopping)
shoppic.pack()

#-------------------------------------
L = ttk.Label(F1, text="รายการค่าใช้จ่าย", font=FONT1).pack()
V_expense = StringVar() # ตัวแปรสำหรับเก็บข้อมูล
E1 = ttk.Entry(F1, textvariable=V_expense, font=FONT2)
E1.pack()
#-------------------------------------
#-------------------------------------
L = ttk.Label(F1, text="ราคา(บาท)", font=FONT1).pack()
V_price = StringVar() # ตัวแปรสำหรับเก็บข้อมูล
E2 = ttk.Entry(F1, textvariable=V_price, font=FONT2)
E2.pack()
#-------------------------------------
#-------------------------------------
L = ttk.Label(F1, text="จำนวน", font=FONT1).pack()
V_pic = StringVar() # ตัวแปรสำหรับเก็บข้อมูล
E3 = ttk.Entry(F1, textvariable=V_pic, font=FONT2)
E3.pack()
#-------------------------------------

saveicon = PhotoImage(file='save.png')
B2 = ttk.Button(F1, text='Save',command=Save, image=saveicon, compound='left')
B2.pack(ipadx=5, ipady=5, pady=10)

v_rerult = StringVar()
v_rerult.set('-------------rusult----------------')
result = ttk.Label(F1, textvariable=v_rerult,font=FONT1,foreground='green')
result.pack(pady=20)

###########################TAP 2############################

def read_csv():
    with open('savedata.csv', newline='',encoding='utf-8') as f:
        fr = csv.reader(f)
        data = list(fr)
    return data

# table
L = ttk.Label(T2, text='ตารางแสดงผลลัพธ์', font=FONT1).pack(pady=20)
header = ['วัน-เวลา','รายการ','ราคา','จำนวน','รวมเงิน']
resultTable = ttk.Treeview(T2, columns=header, show='headings',height=15)
resultTable.pack()

# for i in range(len(header)):
#     resultTable.heading(header[0] ,text=header[0])

for h in header:
    resultTable.heading(h, text=h)

headerWidth = [150,170,80,80,80]
for h, w in zip(header, headerWidth):
    resultTable.column(h,width=w)


def update_table():
    resultTable.delete(*resultTable.get_children())
    data = read_csv()
    for d in data:
        resultTable.insert('',0, value=d)

update_table()

###########################TAP 2############################


GUI.bind('<Tab>', lambda x: E2.focus())
GUI.mainloop()