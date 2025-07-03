import yaml
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


class grender:

    def __init__(self, data=None, example="pre"):
        self.data_dict = None
        self.x_axis = None
        self.y_axis = None
        self.sample = None

        if data is None:
            with open("plot_sample.yml", encoding="utf-8") as f:
                self.sample = yaml.safe_load(f)

            if example == "pre":
                # 예시 데이터 사용
                self.data_dict = self.sample.get("데이터", {})
            else:
                # 파이썬_예시 코드 실행 결과를 data_dict에 저장
                self._sample_create()
            self._sample_rendering()
        else:
            # 직접 전달된 데이터 사용
            self.data_dict = data

    def _sample_create(self):
        code = self.sample.get('파이썬_예시', None)
        if code is not None:
            local_env = {}
            try:
                exec(code, {}, local_env)
                # 예시: local_env에 x, y 등이 생성되었다고 가정
                self.data_dict = {k: v for k, v in local_env.items() if not k.startswith('__')}
            except Exception as e:
                print(f"[grender] 파이썬_예시 코드 실행 실패: {e}")
                self.data_dict = {}
        else:
            print("[grender] 파이썬_예시 코드 없음")
            self.data_dict = {}

    def _sample_rendering(self):
        # 샘플 데이터가 있으면 기본 렌더링
        if self.data_dict:
            self.basicrender()
        else:
            print("[grender] 렌더링할 데이터 없음")


    def basicrender(self):
        # basic elements of graph like axis, tick etc
        plt.figure(figsize=(6, 4))
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('기본 그래프')
        plt.grid(True)
    
class bar(grender):
    def __init__(self, data=None, example="pre", x_key='x', y_key='y'):
        super().__init__(data, example)
        self.x_key = x_key
        self.y_key = y_key
        self.barrender()

    def barrender(self):
        # bar plot using self.data_dict
        if self.data_dict is None:
            print("[bar] 데이터 없음")
            return
        x = self.data_dict.get(self.x_key, None)
        y = self.data_dict.get(self.y_key, None)
        if x is not None and y is not None:
            plt.figure(figsize=(6, 4))
            plt.bar(x, y, color='skyblue')
            plt.xlabel(self.x_key)
            plt.ylabel(self.y_key)
            plt.title('Bar Plot')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.show()
        else:
            print("[bar] x/y 데이터가 부족합니다.")






