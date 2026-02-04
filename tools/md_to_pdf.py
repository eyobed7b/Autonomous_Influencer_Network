from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.enums import TA_LEFT
import sys


def md_to_pdf(md_path, pdf_path):
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    normal.alignment = TA_LEFT
    heading = ParagraphStyle("Heading", parent=styles["Heading1"], spaceAfter=6)
    items = []

    buffer = []

    def flush_buffer():
        if not buffer:
            return
        text = "\n".join(buffer).strip()
        if text:
            # Use Preformatted to preserve simple formatting
            items.append(Preformatted(text, normal))
            items.append(Spacer(1, 6))
        buffer.clear()

    for line in lines:
        if line.startswith("#"):
            flush_buffer()
            lvl = line.count("#", 0, line.find(" ") if " " in line else len(line))
            content = line.lstrip("# ").strip()
            items.append(Paragraph(content, heading))
            items.append(Spacer(1, 6))
        elif line.strip() == "":
            flush_buffer()
        else:
            # simple bold replacement
            l = line.replace("**", "<b>").replace("<b>", "</b>", 1) if "**" in line else line
            buffer.append(l)

    flush_buffer()
    doc.build(items)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python md_to_pdf.py <input.md> <output.pdf>")
        sys.exit(1)
    md_to_pdf(sys.argv[1], sys.argv[2])
