import psycopg2
import os
import logging
import json

logging.basicConfig(level=logging.INFO)

class Database:
    """ Classe para acesso ao banco de dados postgres. """
    
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=os.environ.get("POSTGRES_HOST", "postgres-env"),
                port=os.environ.get("POSTGRES_PORT", "5432"),
                database=os.environ.get("POSTGRES_DB", "lawsuit_processed"),
                user=os.environ.get("POSTGRES_USER", "postgres"),
                password=os.environ.get("POSTGRES_PASSWORD", "postgres")
            )
            self.cursor = self.conn.cursor()
            logging.info("Conectado ao banco de dados!")
        except Exception as e:
            logging.info(f"Erro ao conectar no banco de dados: {e}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logging.info("Conexão com o banco de dados fechada.")

    def select(self, id):
        try:
            self.cursor.execute("SELECT documento_json FROM lawsuits WHERE id = %s;", (id,))
            return  self.cursor.fetchone()  
        except Exception as e:
            logging.info(f"Erro ao executar a consulta: {e}")
            return None
