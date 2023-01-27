from jina import Flow, Document
from helper import get_docs
from executor import EmbeddingExecutor, IndexerExecutor, SearchExecutor
import sys 
from config import PORT


docs = get_docs() 

indexing_flow = Flow().add(uses=EmbeddingExecutor).add(uses=IndexerExecutor)
search_flow = Flow(protocol='grpc',port=PORT).add(uses=EmbeddingExecutor).add(uses=SearchExecutor)


def index():
    with indexing_flow:
        indexing_flow.index(inputs=docs)  # index all documents


def search():
    with search_flow:
        search_flow.block()

if __name__=='__main__':
    argument = sys.argv[1]

    if argument == "index":
        index()
    elif argument == "search":
        search()
    else:
        print("Incorrect argument!")