import os
import subprocess
import tempfile
from pathlib import Path

from django.conf import settings


def compile_latex_to_pdf(tex_code, lang="zh"):
    lang_map = {
        "zh": {"fig": "圖", "tab": "表"},
        "en": {"fig": "Figure", "tab": "Table"},
    }
    labels = lang_map.get(lang, lang_map["zh"])

    config_path = os.path.join(
        settings.BASE_DIR, "apps/posts/templates/posts/config.tex"
    )
    with open(config_path, "r", encoding="utf-8") as f:
        config_content = f.read()

    if r"\documentclass" in tex_code:

        doc_class_end = tex_code.find("}") + 1
        full_code = (
            tex_code[:doc_class_end]
            + "\n"
            + config_content
            + "\n"
            + tex_code[doc_class_end:]
        )
    else:
        full_code = f"""\\documentclass[12pt,a4paper]{{article}}
{config_content}
\\captionsetup{{figurename={labels["fig"]}, tablename={labels["tab"]}}}
\\begin{{document}}
{tex_code}
\\end{{document}}
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        tex_file = temp_path / "document.tex"

        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(full_code)

        try:

            process = subprocess.run(
                [
                    "xelatex",
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    "document.tex",
                ],
                cwd=temp_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=40,
            )

            pdf_file = temp_path / "document.pdf"
            if pdf_file.exists():
                return pdf_file.read_bytes(), None
            else:
                return None, process.stdout.decode("utf-8", "ignore")
        except Exception as e:
            return None, str(e)
