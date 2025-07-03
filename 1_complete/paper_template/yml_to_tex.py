from pathlib import Path
import yaml
import re

# ----------------- 유틸 -----------------

# YAML 중첩 경로 추출
def extract_all_paths(data: dict, prefix=""):
    paths = []
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            paths.extend(extract_all_paths(value, full_key))
        else:
            paths.append(full_key)
    return paths

# YAML 경로 기반 값 추출
def get_by_path(data: dict, path: str):
    for key in path.split('.'):
        data = data.get(key, {})
    return data if isinstance(data, str) else ""

# LaTeX 특수문자 이스케이프
def latex_escape(s: str) -> str:
    if not isinstance(s, str): return s
    return s.replace('&', r'\&').replace('%', r'\%').replace('$', r'\$') \
            .replace('#', r'\#').replace('_', r'\_').replace('{', r'\{') \
            .replace('}', r'\}').replace('~', r'\textasciitilde{}') \
            .replace('^', r'\^{}').replace('\\', r'\textbackslash{}')

# ----------------- mapping.py 처리 -----------------

def update_and_sort_mapping(yaml_path: Path, mapping_path: Path) -> bool:
    with open(yaml_path, encoding="utf-8") as f:
        yaml_data = yaml.safe_load(f)

    all_yaml_paths = extract_all_paths(yaml_data)

    # mapping.py의 mapping 리스트 파싱
    mapping_code = Path(mapping_path).read_text(encoding="utf-8")
    match = re.search(r"mapping\s*=\s*\[(.*?)\]", mapping_code, re.DOTALL)
    if not match:
        print("❌ mapping.py에서 mapping 리스트를 찾을 수 없습니다.")
        return False

    # eval 안전하게
    mapping_raw = "[" + match.group(1) + "]"
    mapping_list = eval(mapping_raw, {"__builtins__": {}})

    # dict 변환 (YAML path → LaTeX command)
    path_to_cmd = {path: cmd for path, cmd in mapping_list}

    updated_mapping = []
    missing_paths = []

    for path in all_yaml_paths:
        cmd = path_to_cmd.get(path, "")
        if not cmd:
            missing_paths.append(path)
        updated_mapping.append((path, cmd))

    # 새 mapping.py 저장
    lines = ["mapping = [\n"]
    for path, cmd in updated_mapping:
        escaped_cmd = cmd.replace('\\', '\\\\')  # escape for Python string
        lines.append(f'    ("{path}", "{escaped_cmd}"),\n')
    lines.append("]\n")
    Path(mapping_path).write_text("".join(lines), encoding="utf-8")

    if missing_paths:
        print("⚠️  다음 항목에 대한 LaTeX 명령어가 mapping.py에 정의되어 있지 않습니다.\n    값을 채운 후 다시 실행해주세요:")
        for path in missing_paths:
            print(f"    {path}")
        return False

    return True

# ----------------- LaTeX 변환 -----------------

def convert_yaml_to_latex(yaml_path: Path, output_path: Path, mapping_path: Path):
    import mapping as mp  # 최신 mapping.py 사용

    with open(yaml_path, encoding="utf-8") as f:
        yaml_data = yaml.safe_load(f)

    lines = ["%%%%%%%%%%%%% Auto-generated LaTeX Macros\n"]
    current_section = ""

    for path, cmd in mp.mapping:
        if not cmd.strip():
            continue  # 명령어 없는 항목은 생략

        top_section = path.split('.')[0]
        if top_section != current_section:
            lines.append(f"\n%%%%%%%%%%%% {top_section}\n")
            current_section = top_section

        val = latex_escape(get_by_path(yaml_data, path))
        lines.append(f"\\newcommand{{{cmd}}}{{{val}}} % {path}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(lines))

    print(f"✅ LaTeX 파일이 생성되었습니다: {output_path}")

# ----------------- main -----------------

def main():
    base = Path(r"C:\Users\parkj\Documents\workspace\my_projects\1_complete\paper_template")
    yaml_path = base / "information.yml"
    mapping_path = base / "mapping.py"
    tex_output = base / "latex/auto/information.tex"

    ok = update_and_sort_mapping(yaml_path, mapping_path)
    if not ok:
        return  # 사용자 확인 후 재실행 필요

    convert_yaml_to_latex(yaml_path, tex_output, mapping_path)

if __name__ == "__main__":
    main()
