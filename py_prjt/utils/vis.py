
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import seaborn as sns

class GraphHelper(ABC):
    def __init__(self, style="whitegrid", figsize=(8, 5), font="Malgun Gothic", palette="deep"):
        self.style = style
        self.figsize = figsize
        self.font = font
        self.palette = palette
        self._set_defaults()

    def _set_defaults(self):
        plt.rcParams["font.family"] = self.font
        sns.set_style(self.style)
        sns.set_palette(self.palette)

    def init_plot(self, title="", xlabel="", ylabel=""):
        plt.figure(figsize=self.figsize)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)

    def show(self):
        plt.tight_layout()
        plt.show()

    @abstractmethod
    def plot(self, *args, **kwargs):
        """하위 클래스에서 반드시 구현해야 함"""
        pass



class BarChart(GraphHelper):
    def plot(self, data, title="막대그래프", xlabel="", ylabel=""):
        self.init_plot(title, xlabel, ylabel)
        plt.bar(data.keys(), data.values(), color="skyblue", edgecolor="black")
        self.show()


class ScatterPlot(GraphHelper):
    def plot(self, x, y, title="산점도", xlabel="", ylabel=""):
        self.init_plot(title, xlabel, ylabel)
        plt.scatter(x, y, alpha=0.7, color="orange", edgecolor="black")
        self.show()

###

import folium
from folium.plugins import MarkerCluster

def mapdf(df, lat_col='Latitude',lng_col='Longitude', popup_col=None, zoom_start=13, cluster=True):

    if df.empty:
        raise ValueError("입력된 데이터프레임이 비어 있습니다.")
    
    # 지도 중심 좌표 (첫 행 기준)
    center = [df.iloc[0][lat_col], df.iloc[0][lng_col]]
    m = folium.Map(location=center, zoom_start=zoom_start)
    
    if cluster:
        marker_cluster = MarkerCluster().add_to(m)
    
    for _, row in df.iterrows():
        location = [row[lat_col], row[lng_col]]
        popup = str(row[popup_col]) if popup_col and popup_col in df.columns else None
        
        if cluster:
            folium.Marker(location, popup=popup).add_to(marker_cluster)
        else:
            folium.Marker(location, popup=popup).add_to(m)
    
    return m


