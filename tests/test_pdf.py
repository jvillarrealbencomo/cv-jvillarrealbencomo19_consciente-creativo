from weasyprint import HTML

HTML(string="<h1>CV 2025</h1><p>Generación de PDF validada.</p>").write_pdf("test.pdf")
