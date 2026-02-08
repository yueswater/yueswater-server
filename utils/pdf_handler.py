import os
import re
import subprocess

from django.conf import settings


def convert_post_to_pdf(post):
    preamble_path = os.path.join(
        settings.BASE_DIR, "apps/posts/templates/posts/pdf_preamble.tex"
    )
    work_dir = os.path.join(settings.BASE_DIR, "media/pdf_tmp")
    os.makedirs(work_dir, exist_ok=True)

    pdf_path = os.path.join(work_dir, f"{post.slug}.pdf")
    author_name = (
        f"{post.author.first_name} {post.author.last_name}".strip()
        or post.author.username
    )

    content = post.content

    def replace_admonition(match):
        ad_type = match.group(1)
        title = match.group(2)
        body = match.group(3).strip()
        body = re.sub(r"\*\*(.*?)\*\*", r"\\textbf{\1}", body)
        body = re.sub(r"`(.*?)`", r"\\texttt{\1}", body)
        return f"\n\\begin{{{ad_type}}}{{{title}}}\n{body}\n\\end{{{ad_type}}}\n"

    pattern = r":::\s*(note|warning|question|tip|info|example)\{title=\"(.*?)\"\}\s*(.*?)\s*:::"
    content = re.sub(pattern, replace_admonition, content, flags=re.DOTALL)

    def replace_simple(match):
        ad_type = match.group(1)
        body = match.group(2).strip()
        body = re.sub(r"\*\*(.*?)\*\*", r"\\textbf{\1}", body)
        body = re.sub(r"`(.*?)`", r"\\texttt{\1}", body)
        return (
            f"\n\\begin{{{ad_type}}}{{{ad_type.upper()}}}\n{body}\n\\end{{{ad_type}}}\n"
        )

    simple_pattern = r":::\s*(note|warning|question|tip|info|example)\s*(.*?)\s*:::"
    content = re.sub(simple_pattern, replace_simple, content, flags=re.DOTALL)

    cmd = [
        "pandoc",
        "-f",
        "markdown+all_symbols_escapable+raw_tex",
        "--pdf-engine=xelatex",
        "--standalone",
        "--number-sections",
        "--shift-heading-level-by=-1",
        "--top-level-division=section",
        "-V",
        "documentclass=article",
        "-H",
        preamble_path,
        "-V",
        f"title={post.title}",
        "-V",
        f"author={author_name}",
        "-V",
        f"date={post.created_at.strftime('%Y-%m-%d')}",
        "--toc",
        "-o",
        pdf_path,
    ]

    try:
        result = subprocess.run(
            cmd,
            input=content.encode("utf-8"),
            cwd=settings.BASE_DIR,
            capture_output=True,
        )

        if result.returncode != 0:
            error_msg = (
                result.stderr.decode("utf-8", errors="ignore")
                if result.stderr
                else "Conversion failed"
            )
            raise Exception(error_msg)

        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
        return pdf_data
    except Exception as e:
        raise Exception(str(e))
    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
