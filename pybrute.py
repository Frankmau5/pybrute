import tkinter as tk
from tkinter import messagebox
import itertools
import threading
import time
import zipfile
import os

def main():
    k = knrf()
    win = k.mk_window()
    win.title("py-brute")
    win.mainloop()

class knrf:
    def __init__(self):
        self.window = tk.Tk()
        self.lock = threading.Lock()
        self.timer_count = 0
        self.timer_switch = True
        self.start_msg = """
        ━━━━━━━━━━━━━━┏┓━━━━━━━━━━┏┓━━━━━
        ━━━━━━━━━━━━━━┃┃━━━━━━━━━┏┛┗┓━━━━
        ┏━━┓┏┓━┏┓━━━━━┃┗━┓┏━┓┏┓┏┓┗┓┏┛┏━━┓
        ┃┏┓┃┃┃━┃┃┏━━━┓┃┏┓┃┃┏┛┃┃┃┃━┃┃━┃┏┓┃
        ┃┗┛┃┃┗━┛┃┗━━━┛┃┗┛┃┃┃━┃┗┛┃━┃┗┓┃┃━┫
        ┃┏━┛┗━┓┏┛━━━━━┗━━┛┗┛━┗━━┛━┗━┛┗━━┛
        ┃┃━━┏━┛┃━━━━━━━━━━━━━━━━━━━━━━━━━
        ┗┛━━┗━━┛━━━━━━━━━━━━━━━━━━━━━━━━━        

        Welcome to py-brute.
        This program is used to learn how to make a tkinter gui
        and brute force passwords.
        You can use this if you have forgotten your password for
        a zip file also.
        
        Brute force can be a very slow process (days or even weeks)
        This program does not use all your cpu cores so it will be
        slower but there is some tip to help speed this up.

        Tips to speed up the brute focre process:
        if you know the length of the password this will help alot.
        """

        zip_frame = tk.Frame()
        zip_path_lab = tk.Label(text="Zip file path:", master=zip_frame)
        self.zip_path_ent = tk.Entry(width=15, master=zip_frame)
        zip_path_lab.grid(row=0,column=0)
        self.zip_path_ent.grid(row=0,column=1)
        zip_frame.pack(fill=tk.X)

        start_frame = tk.Frame()
        start_num_lab = tk.Label(text="Start number:", master=start_frame)
        self.start_num_ent = tk.Entry(width=14, master=start_frame)
        start_num_lab.grid(row=0,column=0)
        self.start_num_ent.grid(row=0,column=1)
        start_frame.pack(fill=tk.X)

        max_frame = tk.Frame()
        max_num_lab = tk.Label(text="Max number:", master=max_frame)
        self.max_num_ent = tk.Entry(width=15, master=max_frame)
        max_num_lab.grid(row=0,column=0)
        self.max_num_ent.grid(row=0,column=1)
        max_frame.pack(fill=tk.X)

        self.output = tk.Text()
        self.output.insert("1.0","Output console")
        self.output.pack(fill=tk.X)

        self.start_btn = tk.Button(text="Run")
        self.start_btn.bind("<Button-1>",self.start_btn_handler)
        self.start_btn.pack(fill=tk.X)
        
        self.output.insert("1.0", self.start_msg )
        self.window.bind("<k>",self.msg_box)        

    def msg_box(self, event):
        messagebox.showinfo("About", "Made by knrf")

    def mk_window(self):
        return self.window


    def start_btn_handler(self,event):
        self.output.delete("1.0", tk.END)
        self.timer_switch = True
        path = self.zip_path_ent.get()
        start = self.start_num_ent.get()
        max_num = self.max_num_ent.get()

        try:
            self.start_int = int(start)
            if self.start_int == 0:
                self.print_output("Error with start number. It must be a number bigger then 0")
                return 0
            if self.start_int > 16:
                self.print_output("Error you can not have a start number bigger then 16")
                return 0
        except:
                self.print_output("Error start must be a number")
                return 0


        try:
            max_int = int(max_num)
            if max_int > 16:
                self.print_output("Error you can not have a max number bigger then 16")
                return 0
            if self.start_int > max_int:
                self.print_output("Error you can not have a start number bigger then max")
                return 0
            if max_int == 0:
                self.print_output("Error you can not have a max number of 0")
                return 0
        except:
            self.print_output("Error max must be a number")
            return 0
        try:
            with open(path,mode='rb') as bzip:
                pass
        except FileNotFoundError:
            self.print_output("Error file not found")
            return 0
       
        if not zipfile.is_zipfile(path):
            t = "{} not a zip file".format(path)
            self.print_output(t)
            return 100
        
        self.start_btn.unbind("<Button-1>")
        self.output.delete("1.0",tk.END)
        self.worker = threading.Thread(target=self.start_bf, args=(self.start_int, max_int, path))
        self.worker.name = "brute-worker"
        self.worker.daemon = True
        self.print_output("Starting brute force")
        self.worker.start()


    def print_output(self,msg):
        self.lock.acquire()
        current_text = self.output.get("1.0", tk.END)
        self.output.delete("1.0",tk.END)
        temp = current_text + " " + msg
        self.output.insert("1.0", temp)
        self.lock.release()

    def print_progress(self, msg):
        self.lock.acquire()
        cur_text = self.output.get("1.0",tk.END)
        cur_text = cur_text.replace("..... -\n","")
        cur_text = cur_text.replace("..... \ \n","")
        cur_text = cur_text.replace("..... |\n","")
        cur_text = cur_text.replace("..... / \n","")
        self.output.delete("1.0",tk.END)
        temp = cur_text + msg
        self.output.insert("1.0",temp)
        self.lock.release()
    
    def timer(self):
        if self.timer_count == 0:
            self.print_progress("..... |")
        if self.timer_count == 1:
            self.print_progress("..... / ")
        if self.timer_count == 2:
            self.print_progress("..... -")
        if self.timer_count == 3:
            self.print_progress("..... \ ")
        self.timer_count += 1
        if self.timer_count == 4:
            self.timer_count = 0
        if self.timer_switch:
            self.window.after(1200,self.timer)

    def start_bf(self, start, max_num, filepath):
        c = [1,2,3,4,5,6,7,8,9,0,'q','a','z','w','s','x','e','d','c','r','f','v','t','g','b','y','h','n','u','j','m','i','k','o','l','p','Q','A','Z','W','S','X','E','D','C','R','F','V','T','G','B','Y','H','N','N','U','J','M','I','K','O','L','P']
        
        self.window.after(1000,self.timer)
        self.myzip = zipfile.ZipFile(filepath);
        dirname, fname = os.path.split(filepath)
        self.dirname = dirname
        self.old = len(os.listdir(self.dirname))
        
        # add one to max_number so that it does the right amount of loops
        max_num += 1
        for i in range(start, max_num):
            if self.brute_force(c, i,filepath, max_num) == 0:
                break
        self.myzip.close()

    def brute_force(self,char_list, pass_len, filepath, max_num):
        self.print_output("Working on {} char passwords".format(pass_len))
        gen = itertools.product(char_list,repeat=pass_len)
        for passwd in gen:
            new_list = [str(i) for i in passwd]
            passwd_str = ''.join(new_list)
            
            try:
                self.myzip.extractall(path=self.dirname,pwd=str.encode(passwd_str))
                time.sleep(2)
                self.new = len(os.listdir(self.dirname))
                if  self.new > self.old:
                    self.clean_up()
                    t = "password is " + passwd_str
                    self.print_output(t)
                    return 0
            except zipfile.BadZipFile as badzip:
                self.error = str(badzip)
            except Exception as e:
                self.error = str(e)
                if "Bad" in self.error:
                    continue
                if "Error -3" in self.error:
                    continue
                # Do something here with the error
                print(self.error)
            
        ma = max_num - 1
        if pass_len == ma:
            self.clean_up()
        return 1

    def clean_up(self):
        self.timer_switch = False
        time.sleep(2)
        self.output.delete("1.0", tk.END)
        self.print_output("Job Done")
        self.start_btn.bind("<Button-1>",self.start_btn_handler)

if __name__ == "__main__":
    main()
