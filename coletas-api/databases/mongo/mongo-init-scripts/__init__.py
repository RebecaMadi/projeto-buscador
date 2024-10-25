from pymongo import MongoClient
import os

def main():
    """Conexão com o mongo"""
    client = MongoClient("mongodb://localhost:27017/")
    banco_de_dados = client["coletas_db"]

    #Criação das coleções
    processos_primeira_instancia_tjal = banco_de_dados["processos_primeira_instancia_tjal"]
    processos_primeira_instancia_tjce = banco_de_dados["processos_primeira_instancia_tjce"]
    processos_segunda_instancia_tjal = banco_de_dados["processos_segunda_instancia_tjal"]
    processos_segunda_instancia_tjce = banco_de_dados["processos_segunda_instancia_tjce"]

    #Criação dos indices para melhorar a busca
    processos_primeira_instancia_tjal.create_index({"numero_do_processo": 1})
    processos_primeira_instancia_tjce.create_index({"numero_do_processo": 1})
    processos_segunda_instancia_tjal.create_index({"numero_do_processo": 1})
    processos_segunda_instancia_tjce.create_index({"numero_do_processo": 1})

if __name__ == "__main__":
    main()