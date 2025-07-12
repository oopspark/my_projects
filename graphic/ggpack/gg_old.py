import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
import yaml
import matplotlib as mpl

class Gg:
    def __init__(self, data=None):
        if data is None:
            self.data = None
        elif isinstance(data, dict):
            self.data = pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            self.data = data.copy()
        elif isinstance(data, list):
            self.data = self._process_list_data(data)
        else:
            raise TypeError("data must be dict, pandas DataFrame, or list")

        self.mapping = {}
        self.geom = None
        self.theme = {}

        #geom 종류별 엔진 

        self.geom_engine_map = {
            'bar': 'matplotlib',
            'point': 'matplotlib',
            'stacked': 'matplotlib',
            'histogram': 'matplotlib',
            'line': 'matplotlib',
            'scatter': 'matplotlib',
            'box': 'matplotlib',
            'pie': 'matplotlib',
            'heat': 'matplotlib',
            'area': 'matplotlib',
            'stream': 'matplotlib',
            'confuse': 'matplotlib',
            'duration': 'matplotlib',
            'violin': 'seaborn',
            'pair': 'seaborn',
            'density': 'seaborn',
            'bubble': 'matplotlib',
            'decision': 'console',
            'decomposition': 'console',
            'event': 'console',
            'spider': 'plotly',
            'treemap': 'plotly',
            'chord': 'plotly',
            'sankey': 'plotly',
            'network': 'networkx',
            'icicle': 'plotly',
            'parallel': 'plotly',
            'surface': 'plotly',
        }
        
        self.geom_engine = None  # 그래프 엔진 저장용

    #region private _init  
    def _process_list_data(self, data):
        coord_val_pairs, ndim = self._parse_array_to_coords_and_values(data)
        coords = [coord for coord, _ in coord_val_pairs]
        values = [val for _, val in coord_val_pairs]

        coord_cols = self._generate_dim_names(ndim)
        df = pd.DataFrame(coords, columns=coord_cols)
        df['value'] = values
        return df

    def _parse_array_to_coords_and_values(self, data):
        arr = np.array(data)

        if arr.dtype == object:
            raise ValueError("입력된 리스트는 정규 다차원 배열이 아닙니다. 내부 리스트 길이가 모두 같아야 합니다.")

        coord_val_pairs = []

        for idx in np.ndindex(arr.shape):
            val = arr[idx]
            if isinstance(val, (list, tuple, np.ndarray)) and len(val) == 1:
                val = val[0]
            coord_val_pairs.append(((idx), val))

        return coord_val_pairs, len(arr.shape)

    def _generate_dim_names(self, n):
        base_names = ['x', 'y', 'z']
        if n <= 3:
            return base_names[:n]
        else:
            extra_dims = [chr(i) for i in range(ord('a'), ord('a') + n - 3)]
            return base_names + extra_dims
    #endregion

    def aes(self, **kwargs):
        self.mapping.update(kwargs)
        return self

    #region geom - 설정 공유 가능 (matplotlib + seaborn 기반)
    def geom_bar(self): 
        self.geom = 'bar'
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = {'category': ['A', 'B', 'C'], 'value': np.random.randint(5, 20, 3)}
            self.data = pd.DataFrame(example_data)
            self.mapping = {'x': 'category', 'y': 'value'}
        return self

    def geom_point(self): 
        self.geom = 'point'
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = {'x': list(range(10)), 'y': np.random.randint(0, 100, 10)}
            self.data = pd.DataFrame(example_data)
            self.mapping = {'x': 'x', 'y': 'y'}
        return self

    def geom_stacked(self): 
        self.geom = 'stacked'
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = {
                'category': ['A', 'B', 'C', 'D'],
                'value1': np.random.randint(1, 10, 4),
                'value2': np.random.randint(1, 10, 4)
            }
            self.data = pd.DataFrame(example_data)
            self.mapping = {'x': 'category', 'y1': 'value1', 'y2': 'value2'}
        return self

    def geom_histogram(self): 
        self.geom = 'histogram'
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = {'values': np.random.randn(1000)}
            self.data = pd.DataFrame(example_data)
            self.mapping = {'x': 'values'}
        return self

    def geom_line(self): 
        self.geom = 'line'
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = {'time': list(range(20)), 'value': np.cumsum(np.random.randn(20))}
            self.data = pd.DataFrame(example_data)
            self.mapping = {'x': 'time', 'y': 'value'}
        return self

    def geom_scatter(self): 
        self.geom = 'scatter'
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = {'x': np.random.rand(50), 'y': np.random.rand(50)}
            self.data = pd.DataFrame(example_data)
            self.mapping = {'x': 'x', 'y': 'y'}
        return self

    def geom_box(self): 
        self.geom = 'box'
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = {
                'A': np.random.randn(50),
                'B': np.random.randn(50) + 1,
                'C': np.random.randn(50) - 1
            }
            self.data = pd.DataFrame(example_data)
            self.mapping = {'y1': 'A', 'y2': 'B', 'y3': 'C'}
        return self

    def geom_pie(self): 
        self.geom = 'pie'
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = {'category': ['A', 'B', 'C'], 'value': np.random.randint(10, 60, 3)}
            self.data = pd.DataFrame(example_data)
            self.mapping = {'x': 'category', 'y': 'value'}
        return self

    def geom_heat(self): 
        self.geom = 'heat'
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = np.random.rand(8,8)
            self.data = self._process_list_data(example_data.tolist())
            self.mapping = {}
        return self

    def geom_area(self): 
        self.geom = 'area'
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = {'x': list(range(1, 16)), 'y': np.random.randint(10, 50, 15)}
            self.data = pd.DataFrame(example_data)
            self.mapping = {'x': 'x', 'y': 'y'}
        return self

    def geom_violin(self): 
        self.geom = 'violin'      # seaborn
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = {
                'A': np.random.randn(100),
                'B': np.random.randn(100) + 2,
                'C': np.random.randn(100) - 2
            }
            self.data = pd.DataFrame(example_data)
            self.mapping = {'y1': 'A', 'y2': 'B', 'y3': 'C'}
        return self

    def geom_pair(self): 
        self.geom = 'pair'        # seaborn
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            self.data = sns.load_dataset("iris")
            self.mapping = {}
        return self

    def geom_density(self): 
        self.geom = 'density'     # seaborn
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = {'value': np.random.randn(500)}
            self.data = pd.DataFrame(example_data)
            self.mapping = {'x': 'value'}
        return self

    def geom_stream(self): 
        self.geom = 'stream'
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = {
                'A': np.random.rand(15),
                'B': np.random.rand(15),
                'C': np.random.rand(15)
            }
            self.data = pd.DataFrame(example_data)
            self.mapping = {}
        return self

    def geom_confuse(self): 
        self.geom = 'confuse'
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = pd.DataFrame(
                np.random.randint(0, 15, (3,3)),
                columns=['Pred No', 'Pred Yes', 'Pred Maybe'],
                index=['Actual No', 'Actual Yes', 'Actual Maybe']
            )
            self.data = example_data
            self.mapping = {}
        return self

    def geom_decomposition(self): 
        self.geom = 'decomposition'
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = {
                'trend': np.random.rand(20),
                'seasonal': np.random.rand(20),
                'residual': np.random.rand(20)
            }
            self.data = pd.DataFrame(example_data)
            self.mapping = {}
        return self

    def geom_decision(self): 
        self.geom = 'decision'
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = {
                'condition': ['A > 5', 'B < 3', 'C == 7'],
                'result': ['Yes', 'No', 'Yes']
            }
            self.data = pd.DataFrame(example_data)
            self.mapping = {'condition': 'condition', 'result': 'result'}
        return self
    #endregion

    #region geom - 설정 별도 처리 필요  
    def geom_bubble(self): 
        self.geom = 'bubble'       # 가능하지만 수동 조정
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = {
                'x': np.random.rand(30),
                'y': np.random.rand(30),
                'size': np.random.rand(30) * 300
            }
            self.data = pd.DataFrame(example_data)
            self.mapping = {'x': 'x', 'y': 'y', 'size': 'size'}
        return self

    def geom_spider(self): 
        self.geom = 'spider'       # plotly
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = {'category': ['A', 'B', 'C', 'D', 'E'], 'value': np.random.randint(1, 15, 5)}
            self.data = pd.DataFrame(example_data)
            self.mapping = {'x': 'category', 'y': 'value'}
        return self

    def geom_treemap(self): 
        self.geom = 'treemap'      # plotly
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = {'labels': ['A', 'B', 'C', 'D'], 'values': np.random.randint(5, 20, 4)}
            self.data = pd.DataFrame(example_data)
            self.mapping = {'x': 'labels', 'y': 'values'}
        return self

    def geom_event(self): 
        self.geom = 'event'        # 콘솔 출력 / plotly.timeline
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = {'time': ['9:00', '10:00', '11:00'], 'event': ['Start', 'Break', 'End']}
            self.data = pd.DataFrame(example_data)
            self.mapping = {'x': 'time', 'y': 'event'}
        return self

    def geom_chord(self): 
        self.geom = 'chord'        # 미구현 or plotly
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            self.data = pd.DataFrame()
            self.mapping = {}
        return self

    def geom_sankey(self): 
        self.geom = 'sankey'       # plotly
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = pd.DataFrame({
                'nodes': ['A', 'B', 'C', 'D'],
                'source': [0, 0, 1, 2],
                'target': [1, 2, 3, 3],
                'value': np.random.randint(1, 10, 4)
            })
            self.data = example_data
            self.mapping = {'nodes': 'nodes', 'source': 'source', 'target': 'target', 'value': 'value'}
        return self

    def geom_network(self): 
        self.geom = 'network'      # networkx
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = pd.DataFrame({
                'nodes': ['A', 'B', 'C'],
                'edges': [('A','B'), ('B','C'), ('A','C')]
            })
            self.data = example_data
            self.mapping = {'nodes': 'nodes', 'edges': 'edges'}
        return self

    def geom_icicle(self): 
        self.geom = 'icicle'       # plotly
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = pd.DataFrame({
                'labels': ['A', 'B', 'C', 'D'],
                'values': np.random.randint(10, 20, 4)
            })
            self.data = example_data
            self.mapping = {'x': 'labels', 'y': 'values'}
        return self

    def geom_parallel(self): 
        self.geom = 'parallel'     # plotly or pandas
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            self.data = sns.load_dataset("iris")
            self.mapping = {'color': 'species'}
        return self

    def geom_surface(self): 
        self.geom = 'surface'      # plotly or mplot3d
        self.geom_engine = self.geom_engine_map.get(self.geom, 'unknown')
        if self.data is None:
            example_data = np.random.rand(20, 20)
            self.data = self._process_list_data(example_data.tolist())
            self.mapping = {}
        return self
    #endregion


    #region theme 
    def set_theme_from_yaml(self, theme_name, yaml_path=r'C:\Users\parkj\Documents\workspace\my_projects\7_project\ggpack\gg_theme.yml'):
        with open(yaml_path, 'r', encoding='utf-8') as f:
            theme_data = yaml.safe_load(f)
        if theme_name not in theme_data:
            raise ValueError(f"Theme '{theme_name}' not found in {yaml_path}")

        # YAML에서 앵커 병합이 이미 반영되므로 해당 테마를 그대로 복사
        self.theme = theme_data[theme_name]
        return self

    def theme_minimal(self): return self.set_theme_from_yaml("minimal")
    def theme_dark(self): return self.set_theme_from_yaml("dark")
    def theme_modern(self): return self.set_theme_from_yaml("modern")
    def theme_presentation(self): return self.set_theme_from_yaml("presentation")
    def theme_basic(self): return self.set_theme_from_yaml("basic")
    #endregion 

    def draw(self):
        self.ax = None
        # 그래프 엔진에 따른 스타일 적용 및 그리기 분기
        if self.geom_engine in ['matplotlib', 'seaborn']:
            self._apply_theme_matplotlib()
            self._apply_text_matplotlib()
            self._draw_matplotlib_based()

        elif self.geom_engine == 'plotly':
            self._draw_plotly_based()

        elif self.geom_engine == 'networkx':
            self._draw_networkx_based()

        elif self.geom_engine == 'console':
            self._draw_console_based()

        else:
            raise ValueError(f"Unknown geom engine: {self.geom_engine}")

        return self

#region private draw 
    def _parse_rgba_string(self, rgba_str):
        if isinstance(rgba_str, str) and rgba_str.startswith('rgba'):
            rgba_str = rgba_str[5:-1]  # 'rgba('와 ')' 제거
            r, g, b, a = map(float, rgba_str.split(','))
            return (r/255, g/255, b/255, a)
        return rgba_str  # 이미 튜플이거나 문자열이면 그대로


    def _apply_theme_matplotlib(self):
        theme = self.theme

        # --- 배경 ---
        bg = theme.get('background', 'white')
        bg = self._parse_rgba_string(bg) if isinstance(bg, str) else bg
        plt.figure(facecolor=bg)
        # --- 폰트 ---
        font = theme.get('font', {})
        mpl.rcParams['font.family'] = font.get('family', 'Arial')
        mpl.rcParams['font.size'] = font.get('size', 12)

        # --- 축 객체 생성 ---
        self.ax = plt.gca()

        # --- 그리드 ---
        if theme.get('grid', False):
            self.ax.grid(True, color=theme.get('grid_color', 'lightgray'))
        else:
            self.ax.grid(False)

        # --- 축 표시 여부 ---
        axis = theme.get('axis', {})
        if not axis.get('show', True):
            self.ax.axis('off')
        else:
            self.ax.axis('on')

        # --- 축 색상/굵기 ---
        for spine in self.ax.spines.values():
            spine.set_color(axis.get('color', 'black'))
            spine.set_linewidth(axis.get('linewidth', 1))

        # --- 틱 설정 ---
        self.ax.tick_params(
            axis='both',
            which='both',
            length=3 if axis.get('ticks', True) else 0,
            color=axis.get('color', 'black')
        )

        # --- 타이틀 ---
        title = theme.get('title', {})
        self._title_conf = {
            "show": title.get('show', True),
            "size": title.get('size', 14),
            "weight": title.get('weight', 'bold'),
            "color": title.get('color', 'black')
        }

        # --- 범례 ---
        legend = theme.get('legend', {})
        self._legend_conf = {
            "show": legend.get('show', True),
            "loc": legend.get('location', 'best'),
            "fontsize": legend.get('font_size', 10)
        }

        # --- bar 스타일 ---
        bar = theme.get('bar', {})
        self._bar_conf = {
            "color": bar.get('color', 'skyblue'),
            "edgecolor": bar.get('edge_color', 'black'),
            "width": bar.get('width', 0.8)
        }

        # --- line 스타일 ---
        line = theme.get('line', {})
        self._line_conf = {
            "color": line.get('color', 'blue'),
            "width": line.get('width', 2),
            "style": line.get('style', 'solid')
        }

        # --- scatter 스타일 ---
        scatter = theme.get('scatter', {})
        self._scatter_conf = {
            "alpha": scatter.get('alpha', 0.8),
            "colormap": scatter.get('colormap', 'viridis')
        }

        # --- pie 스타일 ---
        pie = theme.get('pie', {})
        self._pie_conf = {
            "autopct": pie.get('autopct', '%1.1f%%'),
            "startangle": pie.get('startangle', 90)
        }

        # --- violin ---
        violin = theme.get('violin', {})
        self._violin_conf = {
            "inner": violin.get('inner', 'box')
        }

        # --- heatmap ---
        heatmap = theme.get('heatmap', {})
        self._heatmap_conf = {
            "cmap": heatmap.get('cmap', 'coolwarm'),
            "annot": heatmap.get('annot', False)
        }

    def _apply_text_matplotlib(self):
        font = self.theme.get('font', {})
        color = font.get('color', 'black')

        # 축 레이블
        plt.xlabel(self.mapping.get('x', ''), color=color)
        plt.ylabel(self.mapping.get('y', ''), color=color)

        # 타이틀
        if hasattr(self, '_title_conf') and self._title_conf.get('show', True):
            plt.title(
                getattr(self, 'title', ''),  # self.title 없으면 빈 문자열
                fontsize=self._title_conf['size'],
                fontweight=self._title_conf['weight'],
                color=self._title_conf['color']
            )

        # 범례 (조건: show=True이고, 실제 레전드 대상이 있는 경우)
        if hasattr(self, '_legend_conf') and self._legend_conf.get('show', True):
            # `label=`로 지정된 요소가 있는 경우에만 호출
            handles, labels = plt.gca().get_legend_handles_labels()
            if labels:
                plt.legend(
                    loc=self._legend_conf['loc'],
                    fontsize=self._legend_conf['fontsize']
                )



    def _draw_matplotlib_based(self):
        geom = self.geom
        df = self.data
        mapping = self.mapping

        if geom == 'bar':
            x = df[mapping['x']]
            y = df[mapping['y']]
            conf = self._bar_conf

            plt.bar(
                x,
                y,
                color=conf['color'],
                edgecolor=conf['edgecolor'],
                width=conf['width']
            )

        elif geom == 'point':
            x = df[mapping['x']]
            y = df[mapping['y']]
            plt.scatter(x, y, color='tomato')
            plt.show()

        elif geom == 'stacked':
            x = df[mapping['x']]
            y1 = df[mapping['y1']]
            y2 = df[mapping['y2']]
            plt.bar(x, y1, color='skyblue')
            plt.bar(x, y2, bottom=y1, color='salmon')
            plt.show()

        elif geom == 'histogram':
            values = df[mapping['x']]
            plt.hist(values, bins=10, color='lightgreen', edgecolor='black')
            plt.show()

        elif geom == 'line':
            x = df[mapping['x']]
            y = df[mapping['y']]
            plt.plot(x, y, marker='o', color='blue')
            plt.show()

        elif geom == 'scatter':
            x = df[mapping['x']]
            y = df[mapping['y']]
            plt.scatter(x, y, color='purple')
            plt.show()

        elif geom == 'box':
            data_cols = [mapping[k] for k in mapping if k.startswith('y')]
            data_to_plot = [df[col] for col in data_cols]
            plt.boxplot(data_to_plot, labels=data_cols)
            plt.show()

        elif geom == 'pie':
            labels = df[mapping['x']]
            sizes = df[mapping['y']]
            plt.pie(sizes, labels=labels, autopct='%1.1f%%')
            plt.show()

        elif geom == 'heat':
            data = df.pivot(index='y', columns='x', values='value')
            sns.heatmap(data, annot=True, fmt=".2f", cmap="coolwarm")
            plt.show()

        elif geom == 'area':
            x = df[mapping['x']]
            y = df[mapping['y']]
            plt.fill_between(x, y, color='skyblue', alpha=0.4)
            plt.plot(x, y, color='Slateblue', alpha=0.6)
            plt.show()

        elif geom == 'violin':
            data_cols = [mapping[k] for k in mapping if k.startswith('y')]
            data_to_plot = [df[col] for col in data_cols]
            sns.violinplot(data=data_to_plot)
            plt.show()

        elif geom == 'pair':
            sns.pairplot(df)
            plt.show()

        elif geom == 'density':
            sns.kdeplot(df[mapping['x']], shade=True)
            plt.show()

        elif geom == 'stream':
            # 단순히 선 그래프로 예시
            for col in df.columns:
                plt.plot(df.index, df[col], label=col)
            plt.legend()
            plt.show()

        elif geom == 'confuse':
            sns.heatmap(df, annot=True, fmt="d", cmap="Blues")
            plt.show()

        elif geom == 'decomposition':
            plt.plot(df.index, df['trend'], label='Trend')
            plt.plot(df.index, df['seasonal'], label='Seasonal')
            plt.plot(df.index, df['residual'], label='Residual')
            plt.legend()
            plt.show()

        elif geom == 'decision':
            print("Decision conditions and results:")
            for idx, row in df.iterrows():
                print(f"{row[mapping['condition']]} -> {row[mapping['result']]}")
        else:
            raise NotImplementedError(f"Draw not implemented for geom {geom}")

    def _draw_plotly_based(self):
        if self.geom == 'spider':
            import plotly.express as px
            fig = px.line_polar(self.data, r=self.mapping['y'], theta=self.mapping['x'], line_close=True)
            fig.show()

        elif self.geom == 'treemap':
            import plotly.express as px
            fig = px.treemap(self.data, path=[self.mapping['x']], values=self.mapping['y'])
            fig.show()

        elif self.geom == 'sankey':
            # 간단 예시, 실제는 더 복잡함
            import plotly.graph_objects as go
            data = self.data
            fig = go.Figure(go.Sankey(
                node = dict(label = data['nodes'].tolist()),
                link = dict(
                    source = data['source'].tolist(),
                    target = data['target'].tolist(),
                    value = data['value'].tolist()
                )
            ))
            fig.show()

        elif self.geom == 'icicle':
            import plotly.express as px
            fig = px.icicle(self.data, path=[self.mapping['x']], values=self.mapping['y'])
            fig.show()

        elif self.geom == 'parallel':
            import plotly.express as px
            fig = px.parallel_coordinates(self.data, color=self.data[self.mapping.get('color', '')])
            fig.show()

        elif self.geom == 'surface':
            import plotly.graph_objects as go
            z = self.data.pivot(index='y', columns='x', values='value').values
            fig = go.Figure(data=[go.Surface(z=z)])
            fig.show()

        else:
            raise NotImplementedError(f"Plotly drawing not implemented for geom {self.geom}")

    def _draw_networkx_based(self):
        import networkx as nx
        import matplotlib.pyplot as plt

        if self.geom == 'network':
            G = nx.Graph()
            nodes = self.data['nodes'].tolist()
            edges = self.data['edges'].tolist()

            G.add_nodes_from(nodes)
            G.add_edges_from(edges)

            nx.draw(G, with_labels=True)
            plt.show()

        else:
            raise NotImplementedError(f"NetworkX drawing not implemented for geom {self.geom}")

    def _draw_console_based(self):
        if self.geom == 'decision':
            # 이미 처리됨
            pass
        elif self.geom == 'event':
            print("Event Timeline:")
            for idx, row in self.data.iterrows():
                print(f"{row[self.mapping.get('x','time')]} : {row[self.mapping.get('y','event')]}")
        else:
            raise NotImplementedError(f"Console drawing not implemented for geom {self.geom}")
#endregion

    def show(self):

        if self.geom_engine in ['matplotlib', 'seaborn', 'networkx']:
            import matplotlib.pyplot as plt
            plt.show()
        elif self.geom_engine == 'plotly':
            if hasattr(self, '_last_fig') and self._last_fig is not None:
                self._last_fig.show()

    def save(self, path):
        if self.geom_engine in ['matplotlib', 'seaborn', 'networkx']:
            import matplotlib.pyplot as plt
            plt.savefig(path, bbox_inches='tight')
        elif self.geom_engine == 'plotly':
            if hasattr(self, '_last_fig') and self._last_fig is not None:
                self._last_fig.write_image(path)



# 사용 예시
if __name__ == "__main__":
    from ggpack.gg_old import *


    # bar 그래프
    a = Gg().geom_bar().theme_presentation().draw()

    # ax = plt.gca()
    a.ax.get_xaxis().set_visible(False)  # x축만 제거
    a.ax.get_yaxis().set_visible(False)  # y축만 제거
    

    # for spine in ['top', 'bottom', 'left', 'right']:

    #     ax.spines[spine].set_visible(False)

    # ax.tick_params(left=False, bottom=False)  # y축, x축 틱만 제거


    a.show()


