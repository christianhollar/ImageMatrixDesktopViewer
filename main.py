import tkinter
from tkinter import *
from tkinter import filedialog
import json
from PIL import Image,ImageTk

data = []
parameters = []
parameter_names = []
parameter_length = 0
data_length = 0
wdth = 20
hght = 20
mheight = 2
mwidth = 2
basewidth = 400
data_array = []
use_array = []
nextindex = 0
current_parameters = []

def findjson():
    root = tkinter.Tk()
    root.configure(background="black")

    def click():
        global filename
        filename = filedialog.askopenfilename(master=root, initialdir='/Desktop')
        root.destroy()
        uploadjson()

    root.title("Upload Window")
    button = Button(root,text="Click to Select JSON File",width=20,command=click)
    button.pack(side=TOP)
    button.pack()
    root.mainloop()

def uploadjson():
    global filename
    global imagelist
    global parameter_names
    global parameter_length
    global data_array
    global data_length
    global data

    f = open(filename)

    try:
        data = json.load(f)
    except:
        print("Failure to load json file.")

    data_length = len(data)
    dct = data[0]['params']
    parameter_length = len(dct)

    for key in dct.keys():
        parameter_names.append(key)

    data_array = []

    for i in range(data_length):
        arr = []
        arr.append(i)
        for j in range(parameter_length):
            arr.append(data[i]['params'][parameter_names[j]])
        arr.append(data[i]['filename'])
        arr.append(0)
        arr.append(0)
        data_array.append(arr)

    input_window()

def input_window():

    global wdth
    global hght
    global parameter_length
    global parameter_names

    root = tkinter.Tk()
    entry_dict = {}

    def display():
        global mheight
        global mwidth
        global basewidth

        inputlist = [0]*parameter_length

        for i in range(parameter_length):
            inputlist[i]=entry_dict[i].get()
        if mheightentry.get() != '':
            mheight = int(mheightentry.get())
        if mwidthentry.get() != '':
            mwidth = int(mwidthentry.get())
        if bwidthentry.get()!='':
            basewidth = int(bwidthentry.get())

        root.destroy()
        imagesort(inputlist)

    root.title("Input")
    root.config(bg="#0b3d91")

    for i in range(parameter_length):
        label = Label(root,width=wdth,text=parameter_names[i])
        label.grid(row=i,column=0)
        label.config(bd=5, bg="#0b3d91",fg='white')
        entry_dict[i] = Entry(root,width=wdth)
        entry_dict[i].config(highlightbackground="#FC3D21")
        entry_dict[i].grid(row=i,column=1)

    mheightentry = Entry(root,width=wdth)
    mheightentry.grid(row=parameter_length,column=1)
    mheightentry.config(highlightbackground="#FC3D21")

    hlabel=Label(root, width=wdth,text = "Matrix Height:",bd=5, bg="#0b3d91",fg='white')
    hlabel.grid(row=parameter_length,column=0)

    mwidthentry = Entry(root,width=wdth)
    mwidthentry.config(highlightbackground="#FC3D21")
    mwidthentry.grid(row=parameter_length+1,column=1)

    wlabel = Label(root, width=wdth, text="Matrix Width:",bd=5, bg="#0b3d91",fg='white')
    wlabel.grid(row=parameter_length+1, column=0)

    bwidthentry = Entry(root, width=wdth)
    bwidthentry.config(highlightbackground="#FC3D21")
    bwidthentry.grid(row=parameter_length + 2, column=1)

    blabel = Label(root, width=wdth, text="Image Size:",bd=5, bg="#0b3d91",fg='white')
    blabel.grid(row=parameter_length + 2, column=0)

    submit = Button(root,width=20,text="Submit Parameters",bg="#FC3D21",command=display)
    submit.config(highlightbackground="#FC3D21")
    submit.grid(row=parameter_length+3,column=1)
    root.mainloop()

def imagesort(parameter_input):
    global data_array
    global parameter_length
    global data_length
    global use_array
    global current_parameters

    current_parameters = parameter_input

    use_array = [0]*parameter_length

    diff_index = parameter_length+2
    score_index = parameter_length+3

    for i in range(parameter_length):

        for j in range(data_length):
            if(parameter_input[i]==''):
                use_array[i]=1
                data_array[j][diff_index] = "null"
                continue
            input = float(parameter_input[i])
            current = float(data_array[j][i+1])
            diff = abs(input-current)
            data_array[j][diff_index]=diff

        data_array = sorted(data_array,key=lambda x:x[diff_index])
        added_value = 0

        for j in range(data_length):

            if(j>0):
                if(data_array[j-1][diff_index]!=data_array[j][diff_index]):
                    added_value = j
            data_array[j][score_index]+=added_value

    data_array=sorted(data_array,key=lambda x:x[diff_index])
    image_display()

def image_display():
    global data_array
    global filename
    global mheight
    global mwidth
    global basewidth

    matrix_height = mheight
    matrix_height = matrix_height*4
    matrix_width = mwidth
    filename = filename.replace('index.json', '')
    root = tkinter.Tk()
    root.title("Matrix Display")
    root.config(bd=10)
    root.config(background="#0b3d91")
    k = 0

    button_dict={}
    next_dict={}
    image_dict={}
    reset_label_dict = {}
    reset_entry_dict = {}
    current_label_dict = {}

    def reset():
        global mheight
        global mwidth

        inputlist = [0] * parameter_length

        for i in range(parameter_length):
            if reset_entry_dict[i].get()!='':
                inputlist[i]=int(reset_entry_dict[i].get())
            else:
                inputlist[i]=''
        root.destroy()
        imagesort(inputlist)

    def settings():
        global current_parameters
        global mheight
        global mwidth
        global basewidth

        settingslevel = tkinter.Toplevel()
        settingslevel.title("New Search")
        settingslevel.config(bg='#0B3D91')

        Label(settingslevel, text="Parameter(s)", fg='white', bg='#0B3D91', width=20).grid(column=0, row=0)
        Label(settingslevel, text="Current", fg='white', bg='#0B3D91', width=20).grid(column=1,row=0)
        Label(settingslevel, text="Input", fg='white', bg='#0B3D91', width=20).grid(column=2,row=0)

        for i in range(parameter_length):
            reset_label_dict[i] = Label(settingslevel, text=parameter_names[i] + ":",fg='white',bg='#0B3D91', width=20)
            reset_label_dict[i].grid(column=0,row=i+1)

            pvalue = current_parameters[i]
            if(pvalue == ''):
                pvalue="No Entry"
            current_label_dict[i] = Label(settingslevel, text=pvalue,fg='white',bg='#0B3D91', width=20).grid(column=1,row=i+1)

            reset_entry_dict[i] = Entry(settingslevel, width=20)
            reset_entry_dict[i].config(highlightbackground="#FC3D21")
            reset_entry_dict[i].grid(column=2, row=i+1)

        def action():
            global basewidth
            global mheight
            global mwidth

            if(bwidthentry.get()!=''):
                basewidth=int(bwidthentry.get())
            if (mheightentry.get() != ''):
                mheight = int(mheightentry.get())
            if (mwidthentry.get() != ''):
                mwidth = int(mwidthentry.get())

            return reset()

        Label(settingslevel, text="Matrix Height:", fg='white',bg='#0B3D91',width=20).grid(column=0, row=parameter_length+1)
        mheightentry = Entry(settingslevel, width=20)
        mheightentry.config(highlightbackground="#FC3D21")
        mheightentry.grid(column=2, row=parameter_length+1)

        Label(settingslevel, text=str(mheight), fg='white', bg='#0B3D91', width=20).grid(column=1, row=parameter_length + 1)

        Label(settingslevel, text="Matrix Width:", fg='white',bg='#0B3D91',width=20).grid(column=0, row=parameter_length + 2)
        mwidthentry = Entry(settingslevel, width=20)
        mwidthentry.config(highlightbackground="#FC3D21")
        mwidthentry.grid(column=2, row=parameter_length + 2)

        Label(settingslevel, text=str(mwidth), fg='white', bg='#0B3D91', width=20).grid(column=1, row=parameter_length + 2)

        Label(settingslevel, width=wdth, text="Image Size:",bg='#0B3D91',fg='white').grid(row=parameter_length + 3, column=0)
        bwidthentry = Entry(settingslevel, width=wdth)
        bwidthentry.config(highlightbackground="#FC3D21")
        bwidthentry.grid(row=parameter_length + 3, column=2)

        Label(settingslevel, text=str(basewidth), fg='white', bg='#0B3D91', width=20).grid(column=1, row=parameter_length + 3)

        Button(settingslevel, text="Submit Parameters", command=action, width=20).grid(column=2,row=parameter_length + 4)
        settingslevel.mainloop()

    def expand(k_input):
        newlevel = tkinter.Toplevel(root)
        newlevel.title('Expansion')
        def close():
            newlevel.destroy()

        basewidth = 800
        newlevel.title("Expanded")
        index = data_array[k_input][0]
        image_extension = data[index]['filename']
        imagepath = str(filename + image_extension)
        img = Image.open(imagepath)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(img)
        currentlabel = tkinter.Label(newlevel, image=test)
        currentlabel.image = test
        currentlabel.grid(row=0, column=0)
        closebutton = tkinter.Button(newlevel,text="Close",width = 20,command=close)
        closebutton.grid(row=1,column=0)

        newlevel.mainloop()

    def next(i_input, j_input):
        global basewidth
        global nextindex
        global mheight
        global mwidth
        k_input = mheight+mwidth

        index = data_array[k_input+nextindex][0]
        image_extension = data[index]['filename']
        imagepath = str(filename + image_extension)
        img = Image.open(imagepath)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(img)

        image_dict[k] = tkinter.Label(root,
                                      image=test)
        image_dict[k].image = test
        image_dict[k].grid(row=i_input, column=j_input)
        image_dict[k].config(bd = 5,bg="#0b3d91")

        nextindex=nextindex+1

    def back(i_input, j_input):
        global basewidth
        global nextindex
        global mheight
        global mwidth
        nextindex = nextindex - 1

        k_input = mheight+mwidth

        index = data_array[k_input+nextindex][0]
        image_extension = data[index]['filename']
        imagepath = str(filename + image_extension)

        img = Image.open(imagepath)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(img)

        image_dict[k] = tkinter.Label(root,image=test)
        image_dict[k].config(bd=5, bg="#0b3d91")
        image_dict[k].image = test
        image_dict[k].grid(row=i_input,column=j_input)

    for i in range(0,matrix_height,4):
        for j in range(0,matrix_width):
            index = data_array[k][0]
            image_extension =data[index]['filename']

            imagepath = str(filename+image_extension)
            img = Image.open(imagepath)
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            test = ImageTk.PhotoImage(img)

            image_dict[k] = tkinter.Label(root,
                                         image=test)
            image_dict[k].image = test
            image_dict[k].grid(row=i, column=j)
            image_dict[k].config(bd = 5,bg="#0b3d91")

            def action1(k_input = k):
                return expand(k_input)
            def action2(i_input = i,j_input = j):
                return next(i_input,j_input)
            def action3(i_input = i,j_input = j):
                return back(i_input,j_input)

            button_dict[k] = Button(root,width = 20,
                                    text = "Expand",
                                    highlightbackground='#FC3D21',
                                    command = action1)

            button_dict[k].grid(row=i+1,column=j)

            next_dict[k] = Button(root, width=20,
                                    text="Next",
                                    highlightbackground='#FC3D21',
                                    command=action2)

            next_dict[k].grid(row=i + 2, column=j)

            next_dict[k] = Button(root, width=20,
                                  text="Back",
                                  highlightbackground='#FC3D21',
                                  command=action3)

            next_dict[k].grid(row=i + 3, column=j)
            k += 1


    button_dict[k]=Button(root, width=20,
                                  text="Settings",
                                  highlightbackground='#FC3D21',
                                  command=settings)

    button_dict[k].place(relx=0.5, rely=0.0, anchor=CENTER)

    root.mainloop()

if __name__ == '__main__':
    findjson()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
