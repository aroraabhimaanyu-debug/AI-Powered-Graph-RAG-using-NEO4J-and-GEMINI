import pdfplumber

print("🔥 SCRIPT STARTED")

PDF_PATH = "neo4j_python/DATA/Books/sample_book.pdf"

with pdfplumber.open(PDF_PATH) as pdf:
    print("📄 Total pages:", len(pdf.pages))
    text = pdf.pages[0].extract_text()

print("\n===== FIRST PAGE TEXT (PREVIEW) =====\n")
print(text[:1000])
