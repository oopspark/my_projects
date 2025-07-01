import os
import re
from typing import List, Dict, Optional

class LatexLabeler:
    def __init__(self):
        self.chapter_pattern = re.compile(r'\\chapter\{(.+?)\}')
        self.section_pattern = re.compile(r'\\section\{(.+?)\}')
        self.subsection_pattern = re.compile(r'\\subsection\{(.+?)\}')
        self.label_pattern = re.compile(r'\\label\{.*?\}')

        self.section_count = 0
        self.subsection_count = 0
        self.current_section: Optional[Dict] = None
        self.structure: Dict = {}

    def get_chapter_files(self) -> List[str]:
        files = [f for f in os.listdir('.') if re.match(r'chapter\d+\.tex$', f)]
        files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))
        print(f'[get_chapter_files] 발견된 chapter 파일 목록: {files}')
        return files

    def remove_existing_label(self, lines: List[str], idx: int) -> int:
        """
        현재 줄과 다음 줄에 \\label{...}가 있으면 모두 건너뛰도록 처리.
        """
        skip_count = 0
        for offset in range(0, 2):  # 현재 줄(idx)와 다음 줄(idx+1) 검사
            cur_idx = idx + offset
            if cur_idx < len(lines) and self.label_pattern.search(lines[cur_idx].strip()):
                skip_count += 1
            else:
                break
        return idx + skip_count if skip_count > 0 else idx + 1

    def insert_label(self, lines: List[str], idx: int, label: str, new_lines: List[str]) -> int:
        idx = self.remove_existing_label(lines, idx)
        line = lines[idx].rstrip('\n')
        if not (line.endswith('\\\\') or line.endswith('\\par')):
            new_lines.append('\\\\\n')
        new_lines.append(f'\\label{{{label}}}\n')
        print(f'[insert_label] 라벨 {label} 삽입 (파일 내 라인 인덱스: {idx})')
        return idx

    def remove_labels_from_line(self, line: str) -> str:
        return self.label_pattern.sub('', line)

    def remove_all_labels_in_file(self, filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        cleaned_lines = [self.remove_labels_from_line(line) for line in lines]

        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_lines)

        print(f'[remove_all_labels_in_file] 파일 "{filename}" 내 모든 라벨 제거 완료.')

    def process_file_and_build_dict(self, filename: str, chapter_num: int) -> Dict:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        self.structure = {'chapter': None}
        self.section_count = 0
        self.subsection_count = 0
        self.current_section = None

        idx = 0
        while idx < len(lines):
            line = lines[idx]

            chap_match = self.chapter_pattern.search(line)
            if chap_match:
                chapter_title = chap_match.group(1)
                new_lines.append(line)
                label = f'chap:chapter{chapter_num}'

                idx = self.insert_label(lines, idx, label, new_lines)

                self.structure['chapter'] = {'title': chapter_title, 'label': label, 'sections': []}
                self.section_count = 0
                idx += 1
                print(f'[process_file_and_build_dict] 챕터 발견: "{chapter_title}", 라벨: {label}')
                continue

            sec_match = self.section_pattern.search(line)
            if sec_match:
                self.section_count += 1
                self.subsection_count = 0
                new_lines.append(line)
                label = f'sec:chapter{chapter_num}_{self.section_count}'

                idx = self.insert_label(lines, idx, label, new_lines)

                self.current_section = {'title': sec_match.group(1), 'label': label, 'subsections': []}
                if self.structure['chapter']:
                    self.structure['chapter']['sections'].append(self.current_section)
                idx += 1
                print(f'[process_file_and_build_dict] 섹션 발견: "{sec_match.group(1)}", 라벨: {label}')
                continue

            subsec_match = self.subsection_pattern.search(line)
            if subsec_match:
                self.subsection_count += 1
                new_lines.append(line)
                label = f'subsec:chapter{chapter_num}_{self.section_count}_{self.subsection_count}'

                idx = self.insert_label(lines, idx, label, new_lines)

                if self.current_section:
                    self.current_section['subsections'].append({'title': subsec_match.group(1), 'label': label})
                idx += 1
                print(f'[process_file_and_build_dict] 서브섹션 발견: "{subsec_match.group(1)}", 라벨: {label}')
                continue

            new_lines.append(line)
            idx += 1

        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        print(f'[process_file_and_build_dict] 파일 "{filename}" 처리 완료. 구조: {self.structure}')
        return self.structure

    def generate_toc_tex(self, structures: List[Dict], output_file: str = 'custom_toc.tex'):
        with open(output_file, 'w', encoding='utf-8') as f:
            for chap in structures:
                chap_info = chap['chapter']
                f.write(f'\\nameref{{{chap_info["label"]}}} \\dotfill \\pageref{{{chap_info["label"]}}} \\par\n')
                for sec in chap_info['sections']:
                    f.write(f'\\hspace{{1em}}\\nameref{{{sec["label"]}}} \\dotfill \\pageref{{{sec["label"]}}} \\par\n')
                    for subsec in sec['subsections']:
                        f.write(f'\\hspace{{2em}}\\nameref{{{subsec["label"]}}} \\dotfill \\pageref{{{subsec["label"]}}} \\par\n')

        print(f'[generate_toc_tex] 목차 파일 "{output_file}" 생성 완료.')

def main():
    labeler = LatexLabeler()
    chapter_files = labeler.get_chapter_files()

    # 1) 모든 chapter 파일 라벨 제거 (리셋)
    for file in chapter_files:
        labeler.remove_all_labels_in_file(file)

    # 2) 라벨 재부여 및 구조 수집
    structures = []
    for idx, file in enumerate(chapter_files, start=1):
        struct = labeler.process_file_and_build_dict(file, idx)
        structures.append(struct)

    # 3) 목차 파일 생성
    labeler.generate_toc_tex(structures)

if __name__ == '__main__':
    main()
