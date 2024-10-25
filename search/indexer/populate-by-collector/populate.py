import httpx
import asyncio
import logging

base_url = "http://coletasapi:8000/lawsuit"

lawsuit_numbers = [
    "0710802-55.2018.8.02.0001",
    "0709782-13.2022.8.02.0058",
    "0729685-21.2016.8.02.0001",
    "0705069-74.2019.8.02.0001",
    "0070337-91.2008.8.06.0001",
    "0000442-21.2018.8.06.0089",
    "0217496-81.2021.8.06.0001",
    "0052294-57.2021.8.06.0064"
]

async def fetch_lawsuit_data(lawsuit_number):
    params = {
        "lawsuit_number": lawsuit_number,
        "max_cache_age_seconds": 0
    }
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(base_url, params=params)
            response.raise_for_status()
            logging.info(f"Processo: {lawsuit_number} - Resposta: {response.json()}")
            
        except httpx.HTTPStatusError as e:
            logging.info(f"Erro ao buscar dados para o processo {lawsuit_number}: {e}")
        except httpx.ReadTimeout:
            logging.info(f"Tempo limite excedido para o processo {lawsuit_number}")

async def main():
    """ Faz requisições para a API de coletas para poder povoar o banco."""
    
    tasks = [fetch_lawsuit_data(number) for number in lawsuit_numbers]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
        asyncio.run(main())
