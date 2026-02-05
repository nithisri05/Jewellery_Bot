import faiss

index = faiss.read_index("data/faiss.index")
print("FAISS dimension:", index.d)
print("Total vectors :", index.ntotal)
