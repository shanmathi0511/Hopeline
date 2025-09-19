from fpdf import FPDF

def generate_pdf(title, content, filename="output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=title, ln=True, align="C")

    pdf.multi_cell(0, 10, content)
    pdf.output(filename)
    return filename
