from typing import List


def _escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _wrap_lines(lines: List[str], width: int = 90) -> List[str]:
    out = []
    for line in lines:
        if len(line) <= width:
            out.append(line)
            continue
        buf = line
        while len(buf) > width:
            cut = buf.rfind(" ", 0, width)
            if cut <= 0:
                cut = width
            out.append(buf[:cut])
            buf = buf[cut:].lstrip()
        if buf:
            out.append(buf)
    return out


def render_pdf_from_text(text: str) -> bytes:
    lines = _wrap_lines(text.splitlines())
    content_lines = ["BT", "/F1 12 Tf", "72 720 Td"]
    for line in lines:
        content_lines.append(f"({_escape(line)}) Tj")
        content_lines.append("T*")
    content_lines.append("ET")
    content_stream = "\n".join(content_lines).encode("utf-8")
    content_len = len(content_stream)

    objects = []
    objects.append(b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n")
    objects.append(b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n")
    objects.append(b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n")
    objects.append(b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n")
    objects.append(b"5 0 obj << /Length %d >> stream\n" % content_len + content_stream + b"\nendstream endobj\n")

    offsets = []
    pdf = b"%PDF-1.4\n"
    for obj in objects:
        offsets.append(len(pdf))
        pdf += obj
    xref_offset = len(pdf)
    pdf += b"xref\n0 6\n0000000000 65535 f \n"
    for off in offsets:
        pdf += f"{off:010d} 00000 n \n".encode("utf-8")
    pdf += b"trailer << /Size 6 /Root 1 0 R >>\n"
    pdf += b"startxref\n" + str(xref_offset).encode("utf-8") + b"\n%%EOF\n"
    return pdf
