import pytest
from bson import ObjectId
from pipelines.parts_pipelines import (
    parts_with_providers,
    parts_statistics,
    validate_provider_usage
)
from utils.db import db

@pytest.mark.asyncio
async def test_parts_with_providers_pipeline():
    # Configuración
    test_provider = await db.providers.insert_one({
        "name": "Proveedor Test",
        "contact": "test@example.com"
    })
    
    test_part = await db.parts.insert_one({
        "name": "Parte Test",
        "provider_id": test_provider.inserted_id,
        "category": "test"
    })
    
    # Ejecución
    pipeline = parts_with_providers()
    result = await db.parts.aggregate(pipeline).to_list(None)
    
    # Validación
    assert len(result) > 0
    assert "provider_info" in result[0]
    assert result[0]["provider_info"]["name"] == "Proveedor Test"

@pytest.mark.asyncio
async def test_validate_provider_usage_pipeline():
    # Configuración
    provider = await db.providers.insert_one({"name": "Provider To Delete"})
    await db.parts.insert_many([
        {"name": "Part 1", "provider_id": provider.inserted_id},
        {"name": "Part 2", "provider_id": provider.inserted_id}
    ])
    
    # Ejecución
    pipeline = validate_provider_usage(str(provider.inserted_id))
    result = await db.parts.aggregate(pipeline).to_list(1)
    
    # Validación
    assert result[0]["total_parts"] == 2
    assert "Part 1" in result[0]["parts_list"]
