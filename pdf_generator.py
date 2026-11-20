import weasyprint as wp
import os
def generate_pdf(html_string,working_dir):
    pdf_matter = wp.HTML(string=html_string).write_pdf()
    # os.chdir(working_dir)
    with open('output.pdf',"wb") as f:
        f.write(pdf_matter)
