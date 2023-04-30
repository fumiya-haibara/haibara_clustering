import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import os

plt.rcParams['font.family'] = "MS Gothic"
os.environ["OMP_NUM_THREADS"] = "1"


class Analyze():

    def __init__(self,df):
        self.df = df
        self.color ={1: 'blue',
                    2: 'green',
                    3: 'red', 
                    4: 'cyan',
                    5: 'magenta',
                    6: 'yellow'}
            

    def cluster_analyze(self,xlabel:str,ylabel:str,cluster:int):
        """
        KMeans法を使用したクラスタリング分析
        引数 
        xlabel   x軸として利用するカラム名
        ylabel   y軸として利用するカラム名
        cluster  分類数
        """    

        # KMeansの設定
        km = KMeans(n_clusters=cluster,
                    init = 'random',
                    n_init=10,
                    random_state=1000)
        
        # KMeansを実行
        df_array = np.array(self.df[[xlabel,ylabel]])
        obj_km = km.fit_predict(df_array)
        
        fig,ax = plt.subplots()

        i = 0
        while i < cluster:            
            # 散布図
            ax.scatter(df_array[obj_km == i,0],
                    df_array[obj_km == i,1],
                    s = 50,
                    edgecolor = 'white',
                    marker='o',
                    label = '分類' + str(i+1))

            # クラスタ
            ax.plot(np.mean(df_array[obj_km == i,0]),
                    np.mean(df_array[obj_km == i,1]),
                    marker = 'x',
                    markersize = 10,
                    color = 'r')
            i+=1


        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend()
        fig.savefig('tmp.png')