"""Build the personalized core-only T4 notebook; no training outputs are invented."""
import json
from pathlib import Path
import build_colab as B

root = B.REPO
B.STAGES = [(stem, kind) for stem, kind in B.STAGES if kind.startswith('core')]
nb = B.render('T4')
nb['cells'][0] = B.md('''# Lab 22 — DPO · Colab T4 · Phần bắt buộc

**Họ tên:** Bùi Tiến Cường  
**MSSV:** 2A202602539  
**Ngày chuẩn bị:** 2026-10-08

Chọn **Runtime → Change runtime type → T4 GPU**, rồi **Run all**.
Chạy NB0 → NB1 → NB2 → NB3 → NB4; không chạy bonus.
Giữ nguyên 1.000 mẫu SFT, 800/100 cặp preference và 50 câu held-out.
Dự kiến 1,5–2 giờ. Đây là notebook chuẩn bị; chỉ output thực thi mới là bằng chứng.
Cuối notebook tải ZIP kết quả; sau đó **File → Download → Download .ipynb** để giữ output.
''')
# Skip packages used exclusively by bonus notebooks or optional API judges.
pins = [s for s in B.requirements() if not s.startswith(('llama-cpp-python', 'lm-eval', 'openai', 'anthropic'))]
nb['cells'][3] = B.code('!pip install -q ' + ' '.join('"'+s+'"' for s in pins))
for cell in nb['cells']:
    src = ''.join(cell['source'])
    if cell['cell_type'] == 'code' and 'print(train_ds[0])' in src:
        cell['source'] = B.source_lines(src.replace('print(train_ds[0])', 'for i in range(min(3, len(train_ds))):\n    print(f"\\n--- Cặp {i+1} ---")\n    print(train_ds[i])'))
# Copy submission resources into the standalone Colab environment.
insert = 6
for rel in ['submission/REFLECTION.md', 'scripts/verify.py'] + ['notebooks/'+s+'.py' for s, _ in __import__('importlib').reload(B).STAGES]:
    nb['cells'].insert(insert, B.code('from pathlib import Path\nPath("'+str(Path(rel).parent).replace('\\','/')+'").mkdir(parents=True, exist_ok=True)'))
    insert += 1
    nb['cells'].insert(insert, B.code('%%writefile /content/lab22/'+rel+'\n'+(root/rel).read_text(encoding='utf-8')))
    insert += 1
nb['cells'] += [B.md('''# Nộp bài — lưu kết quả thật

Đọc 3 cặp NB2, rồi điền `submission/REFLECTION.md` bằng số liệu đã chạy.
§3 ít nhất 100 từ; §6 ít nhất 150 từ; §4 phân tích 1 ví dụ hữu ích và 1 ví dụ an toàn.
Chạy lại cell kiểm tra sau khi điền. ZIP luôn được xuất để bạn không mất kết quả nếu bài phản tư còn thiếu.
Tải thêm notebook có output bằng **File → Download → Download .ipynb**.
'''), B.code('''import subprocess
subprocess.run([sys.executable, "scripts/verify.py"], check=False)
'''), B.code('''from zipfile import ZipFile, ZIP_DEFLATED
from google.colab import files
bundle = Path("/content/Lab22_BuiTienCuong_2A202602539_results.zip")
with ZipFile(bundle, "w", ZIP_DEFLATED) as archive:
    for folder in ("submission", "data/eval", "data/pref"):
        for path in Path(folder).rglob("*"):
            if path.is_file():
                archive.write(path, str(path))
    for path in Path("adapters").rglob("*.json"):
        if "checkpoints" not in str(path):
            archive.write(path, str(path))
    path = Path("models/sft-merged/config.json")
    if path.exists():
        archive.write(path, str(path))
print(bundle)
files.download(str(bundle))
''')]
path = root/'colab/Lab22_BuiTienCuong_2A202602539_T4.ipynb'
path.write_text(json.dumps(nb, ensure_ascii=False, indent=1)+'\n', encoding='utf-8')
print(f'{path.name}: {len(nb["cells"])} cells; NB0-NB4 only')
