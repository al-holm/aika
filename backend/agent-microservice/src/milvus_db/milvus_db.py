from pymilvus import MilvusClient

class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MilvusDBClient(metaclass=SingletonMeta):

    def __init__(self):
        self.collections_dir_path = 'milvus_db/db/'
        self.client = MilvusClient(self.collections_dir_path + 'milvus_db')

        self.collections = [] 


    def create_collection(self, 
                          collection_name: str, 
                          dimension: int):
        
        if collection_name in self.collections:
            raise Exception(f"collection {collection_name} already exists")
        
        self.client.create_collection(
            collection_name=collection_name, 
            dimension=dimension
        )

        self.collections.append(collection_name)

    def insert_data(self, 
               collection_name: str, 
               data):
        
        if not collection_name in self.collections:
            raise Exception(f"collection {collection_name} doesn't exist")
         
        self.client.insert(
            collection_name=collection_name, 
            data=data
        )

    def search(self, 
               collection_name: str, 
               data, 
               limit, 
               output_fields):
        
        if not collection_name in self.collections:
            raise Exception(f"collection {collection_name} doesn't exist")
        
        results = self.client.search(
            collection_name=collection_name,
            data=data,
            limit=limit,
            output_fields=output_fields
        )

        return results