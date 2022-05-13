import json
import argparse
from tkinter import *
from tkinter import scrolledtext 
from tkinter.ttk import Radiobutton  
from tkinter import messagebox 
from tkinter import filedialog
from tkinter import Menu  
from tkinter.ttk import Combobox


alphabet = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
alphsize = len(alphabet)
letter_num = dict(zip(alphabet, range(0,alphsize)))
vig_table = {}


    
def cycle_alphabet(i):  
    r = (alphabet*2)[i:i+alphsize:]
    return r

for i in alphabet:
    newdct = dict(zip(cycle_alphabet(0), cycle_alphabet(letter_num[i])))
    vig_table[i] = newdct

def vernam(key, s):
    key_seq = key*(len(s)//len(key)+1)
    key_seq = key_seq[0:len(s):]
    res = ''
    for i in range(0,len(s)):
        k = chr(ord(s[i])^(ord(key_seq[i])%10))
        res += k
    return res
        
def encode_caesar(n, s):
    if isinstance(n, int) == False or isinstance(s, str) == False:
        return 0
    newalph = dict(zip(cycle_alphabet(0), cycle_alphabet(n)))
    res = ''
    for i in s:
        if i.lower() not in alphabet:
            res += i
            continue
        if i.islower() == True:
            res+=(newalph[i])
        else:
            res+=(newalph[i.lower()].upper())
    return res


def decode_caesar(n, s):
    if isinstance(n, int) == False or isinstance(s, str) == False:
        return 0
    return encode_caesar(alphsize-n, s)


def encode_vigenere(key, s):
    if isinstance(key, str) == False or isinstance(s, str) == False:
        return 0
    key_seq = key*(len(s)//len(key)+1)
    key_seq = key_seq[:len(s):]
    res = ''
    tuple_text = list(zip(s, key_seq))
    for i in tuple_text:
        if i[0].lower() not in alphabet:
            res += i[0]
            continue
        if i[0].islower() == True:
            res+=(vig_table[i[1]])[i[0]]
        else:
            res+=(vig_table[i[1]])[i[0].lower()].upper()
    return res

def decode_vigenere(key, s):
    if isinstance(key, str) * isinstance(s, str) == False:
        return 0
    new_key = ''
    for i in key:
        new_key += (alphabet*2)[alphsize-letter_num[i]]
    print(new_key)
    return encode_vigenere(new_key, s)


def count_symb_freq(s):
    s1 = s
    s1 = s1.lower()
    res = {}
    for i in s1:
        if i not in alphabet:
            continue
        if i not in res:
            res[i] = 1
        else:
            res[i] += 1
    for i in res.keys():
        res[i] = float(res[i]/len(s1))
    return res


def count_2Ngram_freq(s):
    res = {}
    s1 = s
    s1 = s1.lower()
    for i in range(0, len(s1)-1):
        res[(s1[i:i+2:])] = 0
    for i in range(0, len(s1)-2):
        res[(s1[i:i+2:])] += 1
    for i in res.keys():
        res[i] = float(res[i]/(len(s1)-1))
    return res

def count_k(s, k):
    res = {}
    s1 = s
    s1 = s1.lower()
    for i in range(0, len(s1)-k):
        res[(s1[i:i+k:])] = 0
    for i in range(0, len(s1)-k):
        res[(s1[i:i+k:])] += 1
    for i in res.keys():
        res[i] = float(res[i]/(len(s1)-1))
    return res

def save_model(d_1, d_2, fp):
    json.dump([d_1, d_2], fp)


def open_model(fp):
    r1 = json.load(fp)
    return r1



def uncode_caesar_1(s, mod):
    
    results = {}
    for i in range(0, alphsize - 1):
        results[decode_caesar(i, s)] = count_symb_freq(decode_caesar(i, s))
    minnorm = 100.0
    res = ''
    for i in results.keys():
        sum_dif = 0.0
        for k in (results[i]).keys():
            if k in mod:
                sum_dif += abs((results[i])[k] - mod[k])
            else:
                sum_dif += (results[i])[k]
        if sum_dif < minnorm:
            minnorm = sum_dif
            res = i
    return res


def uncode_caesar_k(s, k, mod_base):
    for i in mod2.keys():
        mod3
    results = {}
    for i in range(0, alphsize - 1):
        results[decode_caesar(i, s)] = count_k(decode_caesar(i, s), k)
    minnorm = 100.0
    res = ''
    for i in results.keys():
        sum_dif = 0.0
        for k in (results[i]).keys():
            if k in mod:
                sum_dif += abs((results[i])[k] - mod[k])**(2)
            else:
                sum_dif += (results[i])[k]**2
        if sum_dif < minnorm:
            minnorm = sum_dif
            res = i
    return res

def uncode_caesar_2(s, mod_base):
    mod1 = mod_base[0]
    mod2 = mod_base[1]
    mod3 = {}
    for i in mod2.keys():
        if i[0] in mod1:
            mod3[i] = mod2[i]/mod1[i[0]]
   # print(mod1)
   # print(mod2)
   # print(mod3)
    results = {}
    for i in range(0, alphsize - 1):
        c1 = count_symb_freq(decode_caesar(i, s))
        c2 = count_2Ngram_freq(decode_caesar(i, s))
        c3 = {}
        for k in c2.keys():
            if k[0] in c1:
                c3[k] = c2[k]/c1[k[0]]
        results[decode_caesar(i, s)] = c3
        #print("with",i,"was created ", decode_caesar(i, s))
    minnorm = 100.0
    res = ''
    for i in results.keys():
        sum_dif = 0.0
        for k in (results[i]).keys():
            if k in mod3:
                sum_dif += abs((results[i])[k] - mod3[k])**(2)
            else:
                sum_dif += (results[i])[k]**2
        if sum_dif < minnorm:
            minnorm = sum_dif
            res = i
        #print(sum_dif,' d ', minnorm, 'variatn',i)
    return res


def button_encode(): 
    st = str(txt_field_input.get("1.0", END))
    result = 'Empty'
    if selected_type.get() == 1:
        try:
            skey = int(txt_field_key.get())
        except:
            messagebox.showerror('Ошибка', 'Неправедный ключ')
            return
        skey %= alphsize
        result = encode_caesar(skey, st)
    if selected_type.get() == 2:
        skey = str(txt_field_key.get())
        rkey = ''
        for i in skey:
            if i.lower() in alphabet:
                rkey += i.lower()
        if len(rkey) == 0:
            messagebox.showerror('Ошибка', 'Неправедный ключ')
            return
        result = encode_vigenere(rkey, st)
    if selected_type.get() == 3:
        skey = str(txt_field_key.get())
        if len(skey) == 0:
            messagebox.showerror('Ошибка', 'Неправедный ключ')
            return
        result = vernam(skey, st)
    txt_field_result.delete("1.0", END)
    txt_field_result.insert(INSERT, result)
def button_decode(): 
    st = str(txt_field_input.get("1.0", END))
    result = 'Empty'
    if selected_type.get() == 1:
        try:
            skey = int(txt_field_key.get())
        except:
            messagebox.showerror('Ошибка', 'Неправедный ключ')
            return
        skey %= alphsize
        result = decode_caesar(skey, st)
    if selected_type.get() == 2:
        skey = str(txt_field_key.get())
        rkey = ''
        for i in skey:
            if i.lower() in alphabet:
                rkey += i.lower()
        if len(rkey) == 0:
            messagebox.showerror('Ошибка', 'Неправедный ключ')
            return
        result = decode_vigenere(rkey, st)
    if selected_type.get() == 3:
        skey = str(txt_field_key.get())
        if len(skey) == 0:
            messagebox.showerror('Ошибка', 'Неправедный ключ')
            return
        result = vernam(skey, st)
    txt_field_result.delete("1.0", END)
    txt_field_result.insert(INSERT, result)

def file_open():
    txt_file = filedialog.askopenfilename()
    txt_field_input.delete("1.0", END)
    try:
        f = open(txt_file,'r',encoding = encodings_combobox.get())
    except:
        messagebox.showerror('Ошибка', 'Неверная кодировка')
        return
    try:
        txt_field_input.insert(INSERT, f.read())
    except:
        messagebox.showerror('Ошибка', 'Неверная кодировка')
    f.close()
def file_save():
    txt_file = filedialog.asksaveasfilename(initialfile = "output.txt")
    f = open(txt_file,'w',encoding=encodings_combobox.get())
    try:
        f.write(txt_field_result.get("1.0", END))
    except:
        messagebox.showerror('Ошибка', 'Неверная кодировка')
    f.close()
def train():
    txt_file = filedialog.asksaveasfilename(initialfile = "model")
    try:
        f = open(txt_file,'w',encoding = 'utf-16-le')
    except:
        messagebox.showerror('Ошибка', 'Неверная кодировка')
        return
    text_s = txt_field_input.get("1.0", END)
    d1 = count_symb_freq(text_s)
    d2 = count_k(text_s, 2)
    save_model(d1, d2, f)
    f.close()
def huck():
    text_s = txt_field_input.get("1.0", END)
    model_file = filedialog.askopenfilename()
    f = open(model_file,'r',encoding='utf-16le')
    mod = open_model(f)
    result = uncode_caesar_1(text_s, mod[0])
    txt_field_result.delete("1.0", END)
    txt_field_result.insert(INSERT, result)
    
def huck_advanced():
    text_s = txt_field_input.get("1.0", END)
    model_file = filedialog.askopenfilename()
    f = open(model_file,'r',encoding='utf-16le')
    mod = open_model(f)
    result = uncode_caesar_2(text_s, mod)
    txt_field_result.delete("1.0", END)
    txt_field_result.insert(INSERT, result)

    
mw = Tk();
mw.title("Encriptor")
mw.geometry('440x350')
lbl = Label(mw, text="Ключ")  
lbl.place(x=0,y=0)
txt_field_key = Entry(mw, width = 10)
txt_field_key.insert(INSERT,"12");
txt_field_key.place(x=50,y=0)
encode_button = Button(mw, text = "Зашифровать с ключом", command = button_encode)
encode_button.place(x=140,y=0)
decode_button = Button(mw, text = "Дешифровать с ключом", command = button_decode)
decode_button.place(x=290,y=0)
train_button = Button(mw, text = "Обучить", command = train)
train_button.place(x=140,y=25)
huck_button = Button(mw, text = "Взломать цезаря", command = huck)
huck_button.place(x=200,y=25)
huck_adv_button = Button(mw, text = "Взломать цезаря (на коротких)", command = huck_advanced)
huck_adv_button.place(x=140,y=50)


lbl1 = Label(mw, text="Текст")  
lbl1.place(x=90,y=120)
lbl2 = Label(mw, text="Результат")  
lbl2.place(x=290,y=120)

selected_type = IntVar()

type_rad1 = Radiobutton(mw, text = 'Цезарь', value = 1, variable = selected_type)
type_rad2 = Radiobutton(mw, text = 'Виженер', value = 2, variable = selected_type)
type_rad3 = Radiobutton(mw, text = 'Вернам (бинарный)', value = 3, variable = selected_type)
type_rad1.place(x=10,y=50)
type_rad2.place(x=10,y=70)
type_rad3.place(x=10,y=90)
txt_field_input = scrolledtext.ScrolledText(mw, width=20, height=10)  
txt_field_input.place(x=30,y=150)
txt_field_input.insert(INSERT, "Пример текста")
txt_field_result = scrolledtext.ScrolledText(mw, width=20, height=10)  
txt_field_result.place(x=230,y=150)

encodings_combobox = Combobox(mw, state="readonly", width = 15)
encodings_combobox['values'] = ("ANSI","UTF-16LE", "UTF-16-BE", "UTF-8")  
encodings_combobox.current(0) 
encodings_combobox.place(x=5, y = 20)

file_menu = Menu(mw)
file_menu_1 = Menu(file_menu)  
file_menu_1.add_command(label='Открыть', command = file_open)
file_menu_1.add_command(label='Сохранить', command = file_save)
file_menu.add_cascade(label='Файл', menu=file_menu_1)
mw.config(menu=file_menu)
mw.resizable(False, False)
mw.mainloop()
