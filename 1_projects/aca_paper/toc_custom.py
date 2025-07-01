import os
import re
from typing import List, Dict


# 기본 Tex 파일 입출력 기능
class TexProcessor:
    def __init__(self):
        self.structures: List[Dict] = []

    def read_file(self, filename: str) -> str:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()

    def write_file(self, filename: str, content: str):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

    def get_chapter_files(self) -> List[str]:
        files = sorted(
            [f for f in os.listdir('.') if re.match(r'chapter\d+\.tex$', f)],
            key=lambda x: int(re.findall(r'\d+', x)[0])
        )
        return files


# 챕터/섹션/서브섹션 라벨링 및 목차 생성
class ChapterProcessor(TexProcessor):
    def __init__(self, output_file='toc_general.tex'):
        super().__init__()
        self.structures = self.process_all_chapters()
        self.generate_toc_tex(self.structures, output_file)

    def process_file_and_build_dict(self, filename: str, chapter_num: int) -> Dict:
        # 별표(*) 반드시 포함된 명령어만 인식 (별표 없는 것은 무시)
        chapter_re = re.compile(r'\\chapter\*{(.+)}')
        section_re = re.compile(r'\\section\*{(.+)}')
        subsection_re = re.compile(r'\\subsection\*{(.+)}')
        label_re = re.compile(r'\\label\{.*?\}')

        lines = self.read_file(filename).splitlines(keepends=True)
        structure = {'chapter': None}
        new_lines = []
        sec_count = subsec_count = 0
        current_section = None
        i = 0

        while i < len(lines):
            line = lines[i]

            if chapter_re.search(line):
                title = chapter_re.search(line).group(1)
                label = f'chap:chapter{chapter_num}'
                line = label_re.sub('', line).rstrip('\n')
                new_lines.append(f'{line}\\label{{{label}}}\n')
                structure['chapter'] = {'title': title, 'label': label, 'sections': []}
                i += 1
                continue

            elif section_re.search(line):
                sec_count += 1
                subsec_count = 0
                title = section_re.search(line).group(1)
                label = f'sec:chapter{chapter_num}_{sec_count}'
                line = label_re.sub('', line).rstrip('\n')
                new_lines.append(f'{line}\\label{{{label}}}\n')
                current_section = {'title': title, 'label': label, 'subsections': []}
                if structure['chapter'] is not None:
                    structure['chapter']['sections'].append(current_section)
                i += 1
                continue

            elif subsection_re.search(line):
                subsec_count += 1
                title = subsection_re.search(line).group(1)
                label = f'subsec:chapter{chapter_num}_{sec_count}_{subsec_count}'
                line = label_re.sub('', line).rstrip('\n')
                new_lines.append(f'{line}\\label{{{label}}}\n')
                if current_section is not None:
                    current_section['subsections'].append({'title': title, 'label': label})
                i += 1
                continue

            # 별표 없는 chapter, section 등은 건드리지 않음
            new_lines.append(label_re.sub('', line))
            i += 1

        self.write_file(filename, ''.join(new_lines))
        return structure

    def process_all_chapters(self) -> List[Dict]:
        result = []
        for i, filename in enumerate(self.get_chapter_files()):
            print(f'[Chapter] 처리 중: {filename}')
            result.append(self.process_file_and_build_dict(filename, i + 1))
        return result

    def generate_toc_tex(self, structures: list, output_file='toc_general.tex'):
        with open(output_file, 'w', encoding='utf-8') as f:
            for struct in structures:
                chap = struct['chapter']
                f.write(f'\\vspace{{0.8cm}} '
                        f'{{\\fontsize{{12pt}}{{\\baselineskip}} \\selectfont '
                        f'\\textbf{{\\nameref{{{chap["label"]}}} \\dotfill \\pageref{{{chap["label"]}}}}}}} \\par\n')

                for sec in chap.get('sections', []):
                    f.write(f'{{\\fontsize{{11pt}}{{\\baselineskip}} \\selectfont '
                            f'\\hspace{{2em}}\\nameref{{{sec["label"]}}} \\dotfill \\pageref{{{sec["label"]}}}}} \\par\n')

                    for sub in sec.get('subsections', []):
                        f.write(f'{{\\fontsize{{10pt}}{{\\baselineskip}} \\selectfont '
                                f'\\hspace{{4em}}\\nameref{{{sub["label"]}}} \\dotfill \\pageref{{{sub["label"]}}}}} \\par\n')


# 그림, 표 공통 라벨링 처리
class FloatProcessor(TexProcessor):
    def __init__(self, env_name: str, label_prefix: str, output_file: str):
        super().__init__()
        self.pattern_env = env_name
        self.label_prefix = label_prefix
        self.structures = self.process_all_chapters()
        self.generate_toc(self.structures, output_file)

    def process_file_and_build_dict(self, filename: str, chapter_num: int) -> Dict:
        text = self.read_file(filename)
        chapter_re = re.compile(r'\\chapter\{(.+)\}')
        chap_match = chapter_re.search(text)
        chapter_title = chap_match.group(1) if chap_match else f'chapter{chapter_num}'
        chapter_label = f'chap:chapter{chapter_num}'

        env_pattern = re.compile(
            rf'(\\begin\{{{self.pattern_env}.*?\}})(.*?)(\\end\{{{self.pattern_env}\}})', re.DOTALL)
        caption_pattern = re.compile(r'(\\caption\{(.+)\})', re.DOTALL)
        label_pattern = re.compile(r'\\label\{.*?\}')

        new_text = ''
        last_end = 0
        count = 0
        items_info = []

        for m in env_pattern.finditer(text):
            start, end = m.span()
            before = text[last_end:start]
            content = m.group(2)
            content = label_pattern.sub('', content)

            cap_match = caption_pattern.search(content)
            if cap_match:
                count += 1
                caption_text = cap_match.group(2).strip()
                item_label = f'{self.label_prefix}:chapter{chapter_num}_{count}'

                # 캡션 바로 뒤에 라벨 붙이기 (빈 줄 방지)
                caption_full = cap_match.group(1)
                caption_with_label = f'{caption_full}\\label{{{item_label}}}'
                content = content[:cap_match.start()] + caption_with_label + content[cap_match.end():]

                items_info.append({'caption': caption_text, 'label': item_label})

            new_block = m.group(1) + content + m.group(3)
            new_text += before + new_block
            last_end = end

        new_text += text[last_end:]
        self.write_file(filename, new_text)

        return {
            'chapter_title': chapter_title,
            'chapter_label': chapter_label,
            f'{self.pattern_env}s': items_info,
        }

    def process_all_chapters(self) -> List[Dict]:
        result = []
        for i, filename in enumerate(self.get_chapter_files()):
            print(f'[{self.pattern_env.capitalize()}] 처리 중: {filename}')
            result.append(self.process_file_and_build_dict(filename, i + 1))
        return result

    def generate_toc(self, structures: List[Dict], output_file: str):
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f'% 자동 생성된 {self.pattern_env} 목차\n\n')
            for struct in structures:
                for item in struct.get(f'{self.pattern_env}s', []):
                    f.write(f'\\nameref{{{item["label"]}}} \\dotfill \\pageref{{{item["label"]}}} \\par\n')


# 그림/표용 하위 클래스
class FigureProcessor(FloatProcessor):
    def __init__(self, output_file='toc_figures.tex'):
        super().__init__('figure', 'fig', output_file)


class TableProcessor(FloatProcessor):
    def __init__(self, output_file='toc_tables.tex'):
        super().__init__('table', 'tab', output_file)


# 실행 예시
def main():
    ChapterProcessor()       # toc_general.tex
    FigureProcessor()        # toc_figures.tex
    TableProcessor()         # toc_tables.tex
    print('[완료] 모든 목차 파일 생성')


if __name__ == '__main__':
    main()
