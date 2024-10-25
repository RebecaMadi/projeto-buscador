from indexer.typings.database import Database
from indexer.typings.index import Index
from indexer.utils.utils import read_json_file
import logging
import json

logging.basicConfig(level=logging.INFO)

def index_lawsuits():
    db = Database()
    index = Index()

    index_json = read_json_file()

    index.create_index(index_json["settings"], index_json["mappings"])

    db.connect()

    for batch in db.select():
        index.insert_documents(batch)
    
    db.close()
    logging.info("Pipeline de indexação finalizado!")

if __name__ == "__main__":
    index_lawsuits()
