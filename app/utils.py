import os, io, re, zipfile, requests
from fpdf import FPDF

def call_agent(messages):
    url = os.getenv("AGENT_URL")
    key = os.getenv("AGENT_KEY")
    try:
        resp = requests.post(
            url,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
            json={"messages": messages},
            timeout=60
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        return content if content else "I received an empty response. Please try again."
    except Exception as e:
        return f"Agent Error: {str(e)}"

def extract_code_blocks(text):
    matches = re.findall(r"```(\w+)?\n(.*?)```", text, re.DOTALL)
    return [{"lang": m[0] or "txt", "code": m[1].strip()} for m in matches]

def build_zip(code_blocks):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, block in enumerate(code_blocks):
            ext = block['lang'] if block['lang'] else 'txt'
            zf.writestr(f"file_{i}.{ext}", block["code"])
    buf.seek(0)
    return buf

def generate_pdf(title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, title, ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Helvetica", size=11)
    # Clean markdown
    clean = re.sub(r"\*\*(.+?)\*\*", r"\1", content)
    clean = re.sub(r"#{1,6}\s+", "", clean)
    pdf.multi_cell(0, 7, clean)
    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return buf