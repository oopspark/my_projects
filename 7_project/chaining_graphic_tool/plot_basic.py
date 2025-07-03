import matplotlib.pyplot as plt

class BasePlotStyle:
    def __init__(self, figsize=(10, 6), bg_color='white', grid=True, title=None):
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.set_background(bg_color)
        self.set_grid(grid)
        self.set_axes_style()
        if title:
            self.set_title(title)

    def set_background(self, color='white'):
        """Figure와 Axes 배경색 설정"""
        self.fig.patch.set_facecolor(color)
        self.ax.set_facecolor(color)

    def set_grid(self, show=True, linestyle='--', alpha=0.7):
        """격자선 스타일 설정"""
        self.ax.grid(show, linestyle=linestyle, alpha=alpha)

    def set_axes_style(self):
        """축 선, 눈금 등 스타일 통일"""
        self.ax.tick_params(axis='both', which='major', labelsize=10)
        for spine in self.ax.spines.values():
            spine.set_color('gray')
            spine.set_linewidth(1)

    def set_title(self, title, fontsize=14):
        """그래프 제목 설정"""
        self.ax.set_title(title, fontsize=fontsize)

    def save(self, path='plot.png', dpi=300):
        """그래프 저장"""
        self.fig.savefig(path, dpi=dpi, bbox_inches='tight')

    def show(self):
        """화면에 출력"""
        plt.tight_layout()
        plt.show()

    # ----------------------------
    # ▶ 향후 확장 가능한 설정 함수 목록
    # ----------------------------

    # def set_legend(self, location='best', fontsize=10):
    #     """범례 표시"""
    #     self.ax.legend(loc=location, fontsize=fontsize)

    # def set_axis_labels(self, xlabel='', ylabel='', fontsize=12):
    #     """축 레이블 설정"""
    #     self.ax.set_xlabel(xlabel, fontsize=fontsize)
    #     self.ax.set_ylabel(ylabel, fontsize=fontsize)

    # def set_tick_labels(self, xticks=None, yticks=None, rotation=0):
    #     """눈금값 직접 지정 또는 회전"""
    #     if xticks:
    #         self.ax.set_xticklabels(xticks, rotation=rotation)
    #     if yticks:
    #         self.ax.set_yticklabels(yticks)

    # def set_xlim(self, left=None, right=None):
    #     """x축 범위 설정"""
    #     self.ax.set_xlim(left, right)

    # def set_ylim(self, bottom=None, top=None):
    #     """y축 범위 설정"""
    #     self.ax.set_ylim(bottom, top)

    # def add_annotation(self, text, xy, xytext, arrowprops=None, fontsize=10):
    #     """주석 텍스트 추가"""
    #     self.ax.annotate(text, xy=xy, xytext=xytext,
    #                      arrowprops=arrowprops, fontsize=fontsize)

    # def set_aspect_ratio(self, ratio='auto'):
    #     """그래프 비율 조정 ('equal', 'auto')"""
    #     self.ax.set_aspect(ratio)

    # def add_hline(self, y, color='gray', linestyle='--', alpha=0.7):
    #     """수평선 추가"""
    #     self.ax.axhline(y=y, color=color, linestyle=linestyle, alpha=alpha)

    # def add_vline(self, x, color='gray', linestyle='--', alpha=0.7):
    #     """수직선 추가"""
    #     self.ax.axvline(x=x, color=color, linestyle=linestyle, alpha=alpha)

    # def set_xticks(self, ticks):
    #     """x축 눈금 위치 지정"""
    #     self.ax.set_xticks(ticks)

    # def set_yticks(self, ticks):
    #     """y축 눈금 위치 지정"""
    #     self.ax.set_yticks(ticks)

    # def remove_spines(self, spines=('top', 'right')):
    #     """지정한 축선 숨기기"""
    #     for spine in spines:
    #         self.ax.spines[spine].set_visible(False)

    # def set_figure_size(self, width, height):
    #     """전체 Figure 크기 동적 조정"""
    #     self.fig.set_size_inches(width, height)

    # def enable_interactive_mode(self):
    #     """마우스 줌, 회전 등을 위한 인터랙티브 모드"""
    #     plt.ion()

    # def disable_interactive_mode(self):
    #     """인터랙티브 모드 비활성화"""
    #     plt.ioff()
