from jina import Client
from docarray import Document
from config import PORT
from jina.types.request.data import Response

"""
Select protocol from 'grpc', 'http', or 'websocket'; default is 'grpc'.
Select asyncio True of False; default is False.
Select host address to connect to.
Returns a GRPCClient instance.
"""
c = Client(
    protocol='grpc', asyncio=False, host=f'0.0.0.0:{PORT}'
)  

def print_matches(resp: Response):  # the callback function invoked when task is done
    for id, d in enumerate(resp[0].matches[0:10]):  # print top-10 matches
        print(str(id+1) + ')\n')
        print(d.text)
        print("\n***************\n")

while True:
    query = input("Please enter your query term: ")
    response = c.post(on='/search', inputs=Document(text=query))
    print_matches(response)

