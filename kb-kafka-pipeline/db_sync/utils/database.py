import psycopg2
from psycopg2 import sql
from datetime import datetime
import json
import logging
import os

class DatabaseManager:

    """Classe para gerenciar operações de banco de dados. """

    def __init__(self): 

        """ Inicializa a conexão com o banco de dados. """

        self.conn = self.connect_db()
        self.create_database()
        self.create_table()

    def create_database(self):

        """ Cria o banco de dados de lawsuits processados, se não existir. """ 

        with psycopg2.connect(
            host=os.environ.get("POSTGRES_HOST", "postgres-env"),
            port=os.environ.get("POSTGRES_PORT", "5432"),
            database="postgres",
            user=os.environ.get("POSTGRES_USER", "postgres"),
            password=os.environ.get("POSTGRES_PASSWORD", "postgres")
        ) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'lawsuit_processed'")
                exists = cursor.fetchone()
                if not exists:
                    cursor.execute('CREATE DATABASE "lawsuit_processed"')
                    logging.info("Banco de dados 'lawsuit_processed' criado com sucesso.")
                else:
                    logging.info("Banco de dados 'lawsuit_processed' já existe.")

    def connect_db(self):

        """ Conecta ao banco de dados Postgres. """
        return psycopg2.connect(
            host=os.environ.get("POSTGRES_HOST", "postgres-env"),
            port=os.environ.get("POSTGRES_PORT", "5432"),
            database=os.environ.get("POSTGRES_DB", "lawsuit_processed"),
            user=os.environ.get("POSTGRES_USER", "postgres"),
            password=os.environ.get("POSTGRES_PASSWORD", "postgres")
        )

    def create_table(self):

        """ Cria a tabela de lawsuits se não existir. """

        create_table_query = """
        CREATE TABLE IF NOT EXISTS lawsuits (
            id SERIAL PRIMARY KEY,
            number VARCHAR(255),
            court VARCHAR(255),
            nature VARCHAR(255),
            kind VARCHAR(255),
            subject VARCHAR(255),
            sensitive_kind VARCHAR(255),
            distribution_date TIMESTAMP,
            judge_name VARCHAR(255),
            value NUMERIC,
            justice_secret BOOLEAN,
            court_instance INTEGER,
            related_people JSONB,
            represented_person_lawyers JSONB,
            activities JSONB,
            documento_json JSONB
        );
        """
        with self.conn.cursor() as cur:
            cur.execute(create_table_query)
            self.conn.commit()
            logging.info("Tabela 'lawsuits' criada com sucesso.")


    async def insert_data(self, data):
        """Insere dados na tabela de lawsuits."""
        query = """
            INSERT INTO lawsuits (
                number, court, nature, kind, subject, sensitive_kind, 
                distribution_date, judge_name, value, justice_secret, 
                court_instance, related_people, represented_person_lawyers, 
                activities, documento_json
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.get('number'),
                data['court']['rawValue'],
                data.get('nature') if data.get('nature') is not None else None,
                data.get('kind') if data.get('kind') is not None else None,
                data.get('subject') if data.get('subject') is not None else None,
                data.get('sensitiveKind') if data.get('sensitiveKind') is not None else None,
                datetime.fromtimestamp(data.get('distributionDate')) if data.get('distributionDate') else None,
                data.get('judgeName') if data.get('judgeName') is not None else None,
                data.get('value') if data.get('value') is "null" else None,
                data.get('justiceSecret') if data.get('justiceSecret') is not None else None,
                data.get('courtInstance') if data.get('courtInstance') is not None else None,
                json.dumps(data.get('relatedPeople')) if data.get('relatedPeople') else None,
                json.dumps(data.get('representedPersonLawyers')) if data.get('representedPersonLawyers') else None,
                json.dumps(data.get('activities')) if data.get('activities') else None,
                json.dumps(data)
            ))
            self.conn.commit()
        return True