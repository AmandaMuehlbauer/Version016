from django_elasticsearch_dsl import Document, Integer, Index, fields
from apps.core.models import Post  # Adjust the import path as needed

# Define the Elasticsearch index
post_index = Index('post')

@post_index.document
class PostDocument(Document):
    title = fields.TextField(
        analyzer="snowball",
        fields={
            "raw": fields.KeywordField(),
        }
    )
    content = fields.TextField(
        analyzer="snowball",
        fields={
            "raw": fields.KeywordField(),
        }
    )
    # Serialize the relevant User information
    username = fields.TextField(attr='get_username') 
    


    def get_url(self):
        # Build the URL using pk and slug
        return f"/post/{self.instance.pk}/{self.instance.slug}/"



    class Django:
        model = Post  

    class Index:
        name = 'post'  # The name of the Elasticsearch index
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

        def get_username(self):
        # Retrieve and return the username from the related User model
            return self.instance.username  # Replace with the actual field name in User model
        










         