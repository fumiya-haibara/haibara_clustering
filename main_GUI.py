import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
from tkinter import messagebox
import Anlayze
import subprocess


class Analyze_GUI():
    xcol_list =[]
    ycol_list =[]
    df = None
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("クラスタリング分析")
        self.root.protocol('WM_DELETE_WINDOW', (lambda: 'pass')())

    # メニューバー
        self.menubar = tk.Menu(self.root)
        self.root.configure(menu = self.menubar)

    #  メニュー
        self.menu = tk.Menu(self.menubar,tearoff = 0)
        self.menubar.add_cascade(label="メニュー", menu = self.menu)

        self.menu.add_command(label = "終了", command = lambda: self.root.destroy())
        self.menu.add_command(label = "ヘルプ", command = lambda: self.help_func())

    # select file
        # ラベルフレーム
        self.select_frame = ttk.Labelframe(self.root,text = "select file",padding = 15)
        self.select_frame.grid(row = 0,column = 0, padx = 15,pady = 15,sticky=tk.W)

        # テキストボックス
        self.file_txtbox = tk.Entry(self.select_frame,width=50,state="readonly")
        self.file_txtbox.grid(row = 0,column=0 ,padx = 10)

        # ボタン
        self.sarch_button = tk.Button(self.select_frame, text = "検索",command= lambda:self.ask_filedialog())
        self.sarch_button.grid(row= 0,column = 1, padx = 10)

        self.sarch_button1 = tk.Button(self.select_frame, text = "取込",command= lambda:self.file_import())
        self.sarch_button1.grid(row= 0,column = 2, padx = 10)

    # 汎用メッセージ
    def message(self,error_level:int,text:str):
        if error_level == 1:
            messagebox.showinfo("情報",text)
        elif error_level == 2:
            messagebox.showwarning("警告",text)
        elif error_level == 3:
            messagebox.showerror("エラー",text)
    
    # メニューバー実行イベント
    def help_func(self):
        subprocess.run(["start","manual.txt"],shell=True)



    # ボタン実行イベント
    def ask_filedialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("xlsx","*.xlsx")])
        self.file_txtbox.configure(state="normal")
        self.file_txtbox.delete(0,tk.END)
        self.file_txtbox.insert(0,file_path)
        self.file_txtbox.configure(state="readonly")

    def file_import(self):
        Analyze_GUI.df = pd.read_excel(self.file_txtbox.get())
        Analyze_GUI.xcol_list= list(self.df.columns)
        Analyze_GUI.ycol_list = list(self.df.columns)

    # analyze
        # ラベルフレーム
        self.analyze_frame = ttk.Labelframe(self.root,text = "analyze",padding = 15)
        self.analyze_frame.grid(row = 1,column = 0, padx =15,pady = 15,sticky=tk.W)

        # ラベル
        self.xcol_label = ttk.Label(self.analyze_frame,text= "x軸指定列名",width= 30)
        self.xcol_label.grid(row= 0,columns =1,padx =10)

        self.ycol_label = ttk.Label(self.analyze_frame,text= "y軸指定列名",width= 30)
        self.ycol_label.grid(row= 1,columns =1,padx =10)

        self.cluster_label = ttk.Label(self.analyze_frame,text= "分類数",width= 30)
        self.cluster_label.grid(row= 2,columns =1,padx =10)

        # コンボボックス
        self.xcol_cmbbox = ttk.Combobox(self.analyze_frame, values = Analyze_GUI.xcol_list,width= 30, state="readonly")
        self.xcol_cmbbox.grid(row= 0,columns =10,padx =100)

        self.ycol_cmbbox = ttk.Combobox(self.analyze_frame, values = Analyze_GUI.ycol_list,width = 30, state="readonly")
        self.ycol_cmbbox.grid(row= 1,columns =10,padx =100)
   
        self.cluster_cmbbox = ttk.Combobox(self.analyze_frame, values = list(range(1,6)),width = 5, state="readonly")
        self.cluster_cmbbox.grid(row=2,column = 2,padx =100)

        # ボタン
        self.exec_button1 = tk.Button(self.analyze_frame, text = "実行",command=lambda: self.analyze_exec_check())
        self.exec_button1.grid(row= 2,column = 3, padx = 10)
    
    def analyze_exec_check(self):
        try:
            Analyze_GUI.df[self.xcol_cmbbox.get()]
            Analyze_GUI.df[self.ycol_cmbbox.get()]
            int(self.cluster_cmbbox.get())            
        except:
            self.message(3,"コンボボックスの値が不正です。")
            return

        try:
            Analyze_GUI.df[self.xcol_cmbbox.get()] = Analyze_GUI.df[self.xcol_cmbbox.get()].astype(float)
            Analyze_GUI.df[self.ycol_cmbbox.get()] = Analyze_GUI.df[self.ycol_cmbbox.get()].astype(float)
        except:
            self.message(3,"コンボボックスに指定をしている列名が数値型のデータ列ではありません。")
            return

        xlabel = self.xcol_cmbbox.get()
        ylabel = self.ycol_cmbbox.get()
        cluster = int(self.cluster_cmbbox.get()) 

        if messagebox.askyesno("確認", "クラスタリングを実行しますか？"):
            obj_analyze = Anlayze.Analyze(Analyze_GUI.df)
            obj_analyze.cluster_analyze(xlabel, ylabel, cluster)
            self.result_display()
        
        return

    def result_display(self):
        self.result_frame = ttk.Labelframe(self.root,text = "cluster_result",padding = 15)
        self.result_frame.grid(row = 2,column = 0, padx =15,pady = 15,sticky=tk.W)

        self.image = tk.PhotoImage(file="tmp.png")
        self.result_canvas = tk.Canvas(self.result_frame,height=500,width=600)
        self.result_canvas.grid(row=0,column=0,padx =10)

        self.result_canvas.create_image(0,0,image=self.image,anchor=tk.NW)
        return

def main():
    app = Analyze_GUI()
    app.root.mainloop()
  

if __name__ == '__main__':
    main()