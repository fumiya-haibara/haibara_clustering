import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import numpy as np
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
            

    def cluster_analyze(self, xlabel:str, ylabel:str, cluster:int):
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
        df_array = np.array(self.df[[xlabel, ylabel]])
        obj_km = km.fit_predict(df_array)
        
        fig, ax = plt.subplots()

        i = 0
        while i < cluster:            
            # 散布図
            ax.scatter(df_array[obj_km == i, 0],
                    df_array[obj_km == i, 1],
                    s = 50,
                    edgecolor = 'white',
                    marker='o',
                    label = '分類' + str(i+1))

            # クラスタ
            ax.plot(np.mean(df_array[obj_km == i, 0]),
                    np.mean(df_array[obj_km == i, 1]),
                    marker = 'x',
                    markersize = 10,
                    color = 'r')
            i+=1


        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend()
        fig.savefig('tmp.png')
    
    def linear_regression(self, x_study:str, y_study:str,x_zissoku:str,y_zissoku:str,x_size:int,y_size:int):
        """
        1,学習用のx_study_arrayとy_study_arrayを学習させる
        2,x_arrayの実測データからy_arrayの予測をさせ、
        実際のy_arrayのデータと予測されたy_arrayの回帰を行い予測が正しければ、相関性が高いことが確認できる
        """
        lr = LinearRegression()
        x_study_array = np.array(self.df[[x_study]])
        y_study_array = np.array(self.df[[y_study]])
        x_zissoku_array = np.array(self.df[[x_zissoku]])
        y_zissoku_array = np.array(self.df[[y_zissoku]])


        # 学習
        lr.fit(x_study_array,y_study_array)

        # データセットの予測
        y_predict = lr.predict(x_zissoku_array)

        # 予測結果の描画
        fig, ax = plt.subplots()
        ax.scatter(y_predict , y_zissoku_array)
        ax.plot((0,x_size),(0,y_size),linestyle="dashed", color = self.color[3])

        ax.set_xlabel("予測データ:" + y_zissoku)
        ax.set_ylabel("実測データ:" + y_zissoku)
        ax.legend()
        fig.savefig('tmp.png')    


