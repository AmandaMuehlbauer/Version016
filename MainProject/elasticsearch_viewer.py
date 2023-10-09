from elasticsearch import Elasticsearch

# Create an Elasticsearch client connected to your Elasticsearch instance

# Create an Elasticsearch client connected to your Elasticsearch instance
client = Elasticsearch(
    [{'host': 'jidder-elasticsearch', 'port': 9300}],
    use_ssl=False  # Set to True if your Elasticsearch cluster uses SSL
)

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