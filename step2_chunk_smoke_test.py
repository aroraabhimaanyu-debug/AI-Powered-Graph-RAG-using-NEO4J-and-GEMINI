import pdfplumber

PDF_PATH = "neo4j_python/DATA/Books/sample_book.pdf"

CHUNK_WORDS = 400
OVERLAP = 50

print("🔥 CHUNK SCRIPT STARTED")

# ---- extract full text ----
all_text = []

with pdfplumber.open(PDF_PATH) as pdf:
    print("📄 Pages:", len(pdf.pages))
    for idx, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            all_text.append(text)
        if idx == 0:
            print("📃 First page extract preview:")
            print((text or "")[:300])

print("✅ Pages loop finished")

full_text = " ".join(all_text)
print("📏 Total characters extracted:", len(full_text))

words = full_text.split()
print("🧮 Total words:", len(words))

# ---- chunking ----
chunks = []
step = CHUNK_WORDS - OVERLAP

for i in range(0, len(words), step):
    chunk_words = words[i:i + CHUNK_WORDS]
    chunks.append(" ".join(chunk_words))

print("✅ Total chunks created:", len(chunks))

if len(chunks) > 0:
    print("\n===== CHUNK 0 (FIRST 500 CHARS) =====\n")
    print(chunks[0][:500])
else:
    print("❌ NO CHUNKS CREATED")




