import pdfplumber

PDF_PATH = "neo4j_python/DATA/Books/sample_book.pdf"

START_PAGE = 0      # change later
END_PAGE = 10       # ONLY 10 pages for safety

CHUNK_WORDS = 400
OVERLAP = 50

print("🔥 WINDOW CHUNK SCRIPT STARTED")

all_text = []

with pdfplumber.open(PDF_PATH) as pdf:
    print("📄 Total pages in PDF:", len(pdf.pages))

    for i in range(START_PAGE, END_PAGE):
        page = pdf.pages[i]
        text = page.extract_text()
        if text:
            all_text.append(text)
        print(f"✅ Processed page {i}")

print("✅ Page window extraction finished")

full_text = " ".join(all_text)
print("📏 Characters extracted:", len(full_text))

words = full_text.split()
print("🧮 Words extracted:", len(words))

# ---- chunking ----
chunks = []
step = CHUNK_WORDS - OVERLAP

for i in range(0, len(words), step):
    chunk_words = words[i:i + CHUNK_WORDS]
    chunks.append(" ".join(chunk_words))

print("✅ Total chunks created:", len(chunks))

print("\n===== CHUNK 0 PREVIEW =====\n")
print(chunks[0][:500])
# ---- inspect specific chunks ----
print("\n===== AVAILABLE CHUNKS =====")
print("Total chunks:", len(chunks))

for idx in [1, 2, 3, 4, 5]:
    if idx < len(chunks):
        print(f"\n===== CHUNK {idx} PREVIEW (first 500 chars) =====\n")
        print(chunks[idx][:500])
