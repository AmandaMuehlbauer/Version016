from elasticsearch import Elasticsearch

# Create an Elasticsearch client connected to your Elasticsearch instance
client = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# Specify the index you want to query
index_name = 'post'

# Use a search query to retrieve all documents in the 'post' index
search_query = {
    "query": {
        "match_all": {}
    }
}

# Perform the search
response = client.search(index=index_name, body=search_query)

# Extract and display the documents
hits = response['hits']['hits']

for hit in hits:
    print(hit['_source'])