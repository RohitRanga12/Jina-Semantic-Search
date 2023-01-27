from jina import DocumentArray, Executor, requests
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-mpnet-base-v2')


class EmbeddingExecutor(Executor):   
    @requests
    def embed(self, docs: DocumentArray, **kwargs):
        for d in docs:
            d.embedding = model.encode(d.text)


class IndexerExecutor(Executor):
    indexed_docs = DocumentArray(
        storage='sqlite', 
        config={'connection': 'example.db', 'table_name': 'mine'}  
    )

    @requests
    def index(self, docs: DocumentArray, **kwargs):
        self.indexed_docs.extend(docs)  # Index the docs into the Document Store
        self.indexed_docs.summary()


class SearchExecutor(Executor):
    indexed_docs = DocumentArray( # Obtain the indexed docs for search
        storage='sqlite', 
        config={'connection': 'example.db', 'table_name': 'mine'}  
    )

    @requests(on='/search')
    def search(self, docs: DocumentArray, **kwargs):
        docs.match(self.indexed_docs, metric='cosine', limit=30)