from elasticsearch import Elasticsearch


def test_elasticsearch_connection():
    # Define the Elasticsearch URL and port
    elasticsearch_url = 'http://localhost'
    elasticsearch_port = 9200

    try:
        # Create an Elasticsearch client
        client = Elasticsearch(hosts=[{'host': elasticsearch_url, 'port': elasticsearch_port}])

        # Check the connection
        if client.ping():
            print("Successfully connected to Elasticsearch server")
            
            # Perform a simple query to verify the Elasticsearch server
            query = {
                "query": {
                    "match_all": {}
                }
            }

            # Replace 'your_index_name' with the name of your Elasticsearch index
            response = client.search(index='your_index_name', body=query)

            # Print the response
            print("Elasticsearch query results:")
            print(response)

        else:
            print("Failed to connect to Elasticsearch server")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_elasticsearch_connection()