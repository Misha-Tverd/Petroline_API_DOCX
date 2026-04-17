from __future__ import annotations

from pathlib import Path

from docxtpl import DocxTemplate



def generate_docx(template_path: Path, context: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = DocxTemplate(str(template_path))
    doc.render(context)
    doc.save(str(output_path))
