import httpx
import pytest
import json

def normalize_json(data):
    if isinstance(data, dict):
        return {key: normalize_json(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [normalize_json(item) for item in data]
    elif isinstance(data, str):
        return data.strip()
    elif data is None:
        return 'null'
    return data

@pytest.mark.asyncio
async def test_lawsuit():
    """Faz uma requisição e compara com o resultado esperado"""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://coletasapi:8000/lawsuit?lawsuit_number=0710802-55.2018.8.02.0001&max_cache_age_seconds=1")
        assert response.status_code == 200
        with open("test_response.json", 'r', encoding='utf-8') as file:
            response_expected = json.load(file)
            response_expected = normalize_json(response_expected)
        response_json = normalize_json(response.json())
        assert response_expected == response_json