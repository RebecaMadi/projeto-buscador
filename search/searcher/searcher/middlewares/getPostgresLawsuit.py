from searcher.typings.database import Database
from searcher.utils.utils import format_db_response
import logging

logging.basicConfig(level=logging.INFO)

def get_lawsuit(id):
    db = Database()
    db.connect()
    db_record = db.select(id)
    formatted_response = format_db_response(db_record[0])
    db.close()
    return formatted_response
