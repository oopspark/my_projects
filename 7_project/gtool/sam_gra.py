
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# --- 공통 베이스 클래스 ---
class BasePlot:
    def plot(self, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement this method.")


# --- 각 플롯별 클래스 ---
class BarPlot(BasePlot):
    def __init__(self):
        self.subjects = ['Korean', 'Math', 'English', 'Science', 'History', 'PE', 'Music']
        self.scores = np.random.randint(60, 100, size=len(self.subjects))

    def plot(self, subjects=None, scores=None, title='Scores by Subject'):
        subjects = subjects if subjects is not None else self.subjects
        scores = scores if scores is not None else self.scores
        plt.figure(figsize=(10, 6))
        bars = plt.bar(subjects, scores, color='skyblue')
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval}', ha='center', va='bottom')
        plt.title(title)
        plt.xlabel('Subjects')
        plt.ylabel('Scores')
        plt.ylim(0, 110)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

class SpiderPlot(BasePlot):
    def __init__(self):
        self.categories = ['Speed', 'Reliability', 'Comfort', 'Safety', 'Efficiency']
        self.values = np.random.randint(50, 100, size=len(self.categories))

    def plot(self, categories=None, values=None, title="Spider (Radar) Chart"):
        categories = categories if categories is not None else self.categories
        values = values if values is not None else self.values
        fig = go.Figure(
            data=go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Car A'
            )
        )
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            title=title
        )
        fig.show()

class TreemapPlot(BasePlot):
    def __init__(self):
        self.df = pd.DataFrame({
            "labels": ["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
            "parents": ["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"],
            "values": [10, 14, 12, 10, 2, 6, 6, 4, 4]
        })

    def plot(self, df=None, title='Treemap'):
        df = df if df is not None else self.df
        fig = px.treemap(df, path=['parents', 'labels'], values='values', title=title)
        fig.show()

class EventTimelinePlot(BasePlot):
    def __init__(self):
        self.df = pd.DataFrame([
            dict(Task="Job A", Start='2025-07-01', Finish='2025-07-05'),
            dict(Task="Job B", Start='2025-07-02', Finish='2025-07-07'),
            dict(Task="Job C", Start='2025-07-04', Finish='2025-07-09')
        ])

    def plot(self, df=None, title='Event Timeline'):
        df = df if df is not None else self.df
        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", title=title)
        fig.update_yaxes(autorange="reversed")
        fig.show()

class DurationPlot(BasePlot):
    def __init__(self):
        self.df = pd.DataFrame({
            'Task': ['A', 'B', 'C'],
            'Start': pd.to_datetime(['2025-07-01', '2025-07-03', '2025-07-05']),
            'End': pd.to_datetime(['2025-07-04', '2025-07-06', '2025-07-08'])
        })
        self.df['Duration'] = (self.df['End'] - self.df['Start']).dt.days

    def plot(self, df=None, title='Duration Plot'):
        df = df if df is not None else self.df
        fig = px.bar(df, x='Task', y='Duration', title=title)
        fig.show()

class SankeyPlot(BasePlot):
    def __init__(self):
        self.node_label = ["A", "B", "C", "D", "E"]
        self.node_color = ["blue"] * 5
        self.source = [0, 1, 0, 2, 3]
        self.target = [2, 3, 3, 4, 4]
        self.value = [8, 4, 2, 8, 4]

    def plot(self, node_label=None, node_color=None, source=None, target=None, value=None, title="Sankey Diagram"):
        node_label = node_label if node_label is not None else self.node_label
        node_color = node_color if node_color is not None else self.node_color
        source = source if source is not None else self.source
        target = target if target is not None else self.target
        value = value if value is not None else self.value
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=node_label,
                color=node_color
            ),
            link=dict(
                source=source,
                target=target,
                value=value
            ))])
        fig.update_layout(title_text=title, font_size=10)
        fig.show()

class NetworkPlot(BasePlot):
    def __init__(self):
        import networkx as nx
        self.G = nx.karate_club_graph()

    def plot(self, G=None, title='Network Graph (Matplotlib + NetworkX)'):
        import networkx as nx
        G = G if G is not None else self.G
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray')
        plt.title(title)
        plt.show()

class IciclePlot(BasePlot):
    def __init__(self):
        self.df = pd.DataFrame({
            "labels": ["Root", "Branch A", "Branch B", "Leaf A1", "Leaf A2", "Leaf B1", "Leaf B2"],
            "parents": ["", "Root", "Root", "Branch A", "Branch A", "Branch B", "Branch B"],
            "values": [10, 5, 5, 3, 2, 3, 2]
        })

    def plot(self, df=None, title='Icicle Chart'):
        df = df if df is not None else self.df
        fig = px.icicle(df, path=['labels'], values='values', title=title)
        fig.show()

class ParallelCoordinatesPlot(BasePlot):
    def __init__(self):
        self.df = px.data.iris()

    def plot(self, df=None, color='species_id', title='Parallel Coordinates Plot'):
        df = df if df is not None else self.df
        fig = px.parallel_coordinates(df, color=color,
                                      labels={"species_id": "Species"},
                                      color_continuous_scale=px.colors.diverging.Tealrose,
                                      color_continuous_midpoint=2)
        fig.update_layout(title=title)
        fig.show()

class SurfacePlot(BasePlot):
    def __init__(self):
        self.x = np.linspace(-5, 5, 50)
        self.y = np.linspace(-5, 5, 50)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        self.Z = np.sin(np.sqrt(self.X**2 + self.Y**2))

    def plot(self, X=None, Y=None, Z=None, title='Surface Plot'):
        X = X if X is not None else self.X
        Y = Y if Y is not None else self.Y
        Z = Z if Z is not None else self.Z
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
        fig.update_layout(title=title)
        fig.show()

class DecisionTreePlot(BasePlot):
    def __init__(self):
        from sklearn.datasets import load_iris
        from sklearn.tree import DecisionTreeClassifier
        iris = load_iris()
        self.iris = iris
        self.clf = DecisionTreeClassifier(max_depth=3)
        self.clf.fit(iris.data, iris.target)

    def plot(self, clf=None, iris=None, title='Decision Tree'):
        from sklearn.tree import plot_tree
        clf = clf if clf is not None else self.clf
        iris = iris if iris is not None else self.iris
        plt.figure(figsize=(12,8))
        plot_tree(clf, feature_names=iris.feature_names, class_names=iris.target_names,
                  filled=True, rounded=True)
        plt.title(title)
        plt.show()

class ConfusionMatrixPlot(BasePlot):
    def __init__(self):
        self.y_true = np.random.choice([0, 1], size=100)
        self.y_pred = np.random.choice([0, 1], size=100)

    def plot(self, y_true=None, y_pred=None, title='Confusion Matrix'):
        from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
        y_true = y_true if y_true is not None else self.y_true
        y_pred = y_pred if y_pred is not None else self.y_pred
        cm = confusion_matrix(y_true, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot(cmap='Blues')
        plt.title(title)
        plt.show()

class StreamGraphPlot(BasePlot):
    def __init__(self):
        self.x = np.arange(1, 11)
        self.y1 = np.random.randint(1, 10, 10)
        self.y2 = np.random.randint(1, 10, 10)
        self.y3 = np.random.randint(1, 10, 10)

    def plot(self, x=None, y1=None, y2=None, y3=None, title='Streamgraph (Stacked Area)'):
        x = x if x is not None else self.x
        y1 = y1 if y1 is not None else self.y1
        y2 = y2 if y2 is not None else self.y2
        y3 = y3 if y3 is not None else self.y3
        plt.figure(figsize=(8, 6))
        plt.stackplot(x, y1, y2, y3, colors=['#FF9999', '#9999FF', '#99FF99'], labels=['A', 'B', 'C'])
        plt.title(title)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.tight_layout()
        plt.show()
class TimeSeriesDecompositionPlot(BasePlot):
    def __init__(self):
        rng = pd.date_range('2025-01-01', periods=100)
        self.data = pd.Series(10 + 0.1*np.arange(100) + np.sin(np.linspace(0, 12*np.pi, 100)) + np.random.randn(100)*0.5, index=rng)

    def plot(self, data=None, title='Time Series Decomposition (Savitzky-Golay Smoothing)'):
        from scipy.signal import savgol_filter
        data = data if data is not None else self.data
        trend = savgol_filter(data, window_length=21, polyorder=2)
        seasonal = data - trend
        residual = data - trend - seasonal  # 이것은 거의 0이 됨

        fig, axs = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
        axs[0].plot(data, label='Original', color='black')
        axs[0].set_title('Original')
        axs[1].plot(trend, label='Trend', color='blue')
        axs[1].set_title('Trend (Smoothed)')
        axs[2].plot(seasonal, label='Seasonal (Residual)', color='orange')
        axs[2].set_title('Seasonal Component (Raw - Trend)')
        axs[3].plot(residual, label='Residual', color='red')
        axs[3].set_title('Residual')
        for ax in axs:
            ax.grid(True)
        plt.suptitle(title)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":

    TimeSeriesDecompositionPlot().plot()
