import os
import re
import subprocess
import tkinter as tk
import uuid
import time
import json
import copy
from os.path import join as pj

#try:
#    import _thread as thread
#except ImportError:
#    import _dummy_thread as thread
    
def say_hi():
        print("hi there, everyone!")

s1 = ''#u'\u2022' + ' '
s2 = u'\u251c' + ' '
s3 = u'\u2514' + ' '

class Dummy_class():
    def __enter__(self):
        pass
    def __exit__(self, one, two, three):
        pass

gui_lock = Dummy_class();#thread.allocate_lock()
gui_pipe = {
    '_DONE': False,
    'l_sel': None,
    'l_ref': None,
    'btn_q': []
    }

def l_on_select(event):
    widget = event.widget
    value = widget.curselection()[0]
    print(str(value))
    with gui_lock:
        gui_pipe['l_sel'] = value

class Application(tk.Frame):
    def createWidgets(self):
        self.QUIT = tk.Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = say_hi

        self.hi_there.pack({"side": "left"})

        listbox = tk.Listbox(self, width=20, height=5, font=('consolas', 10))
        listbox.bind('<<ListboxSelect>>', l_on_select)
        listbox.pack({"side": "left"})
        listbox.insert(tk.END, s1 + "Test")
        listbox.insert(tk.END, s2 + "Lorem")
        listbox.insert(tk.END, s2 + "Ipsum")
        listbox.insert(tk.END, s3 + "abcdefghijklmnopqrstuvxyzåäö-abcdefghijklmnopqrstuvxyzåäö-")
        listbox.insert(tk.END, s1 + "Sit")
        listbox.insert(tk.END, s1 + "Amet")
        print(str(listbox.delete(3)))
        listbox.insert(3, s3 + "Dolor")
        listbox.insert(20, s3 + "Grande")

        with gui_lock:
            gui_pipe['l_ref'] = listbox

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
def ident_neterr(string_in):
    if re_search('unable to access', str(string_in)):
        return True
    return False



def window_thread():
    with gui_lock:
        app = gui_pipe['w_ref']
    try:
        app.mainloop()
    except Exception as excep:
        print('-> Window exception: ' + str(excep))
    finally:
        print('-> exiting winow')
        with gui_lock:
            gui_pipe['_DONE'] = True
            try:
                root.destroy()
            except Exception as excep:
                print('-> Root destruction exception: ' + str(excep))
        print('QUIT: Window ')
        return None

class Datafile:
    db_dict = {}
    ro = {}
    db_path = ""
    decoupled = False
    def __init__(self, db_path: str, new: bool = False, db_dict: dict = {}):
        self.db_path = str(db_path)
        if len(self.db_path) == 0:
            new = True
            self.decoupled = True
        if new:
            self.db_dict = db_dict
            self.update()
        else:
            with open(self.db_path, 'r') as db_file:
                self.db_dict = json.load(db_file)
    
    def update(self):
        if self.decoupled:
            return
        with open(db_path, 'w') as db_file:
            json.dump(db_dict, db_file)
            
    def couple(self, db_path):
        self.db_path = db_path
        self.decoupled = False
        self.update()
        
    def __enter__(self):
        return self.db_dict
    
    def __exit__(self, exception_type, exception_value, traceback):
        if exception_value != None:
            raise exception_value
        self.db_dict = copy.deepcopy(self.db_dict)
        self.ro = copy.deepcopy(self.db_dict)
        self.update()
    ## Thanks to http://effbot.org/zone/python-with-statement.htm

def set_win_mode(mode, s_mode, window):
    pass

data_dir_name = 'Stargit'
data_file_name = 'data.json'
data_path = pj(data_dir_name, data_file_name)
MODE = 0
SCREEN_MODE = -1
RUNNING = True

root = tk.Tk()
app = Application(master=root)
app.mainloop()
with gui_lock:
    #gui_pipe['w_ref'] = app
    pass

#err = 1;
#if err == 0:
#    db_main = Datafile(data_path)
#    MODE = 1
#else:
#    db_main = Datafile('')

#print("DB_err: " + str(err))

#if MODE == 1:
#    if db_main.ro['has_repo']:
#        MODE = 3
#    if db_main.ro['has_remote']:
#        MODE = 2

#window_thread = thread.start_new_thread(window_func, ())
#window_func()
time.sleep(2)

#counter = 0
#while RUNNING:
#    print("MODE: " + str(MODE))
#    time.sleep(0.05)
#    with gui_lock:
#        print('l_sel: ' + str(gui_pipe['l_sel']))
#        if gui_pipe['_DONE']:
#            RUNNING = False
#    with db_main as db:
#        if MODE == 0:
#            #set_win_mode(0, SCREEN_MODE, app)
#            pass
#    if counter == 5:
#        RUNNING = False
#    counter += 1
            
    

print('QUIT: Main')
