import json
import os
from typing import List, Dict, Any

CATALOG_PATH = "data/mocks/product_catalog.json"

def get_products_by_risk(max_risk_score: float) -> List[Dict[str, Any]]:
    if not os.path.exists(CATALOG_PATH):
        return []
        
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)
        
    products = catalog.get("products", [])
    suitable_products = [p for p in products if p.get("risk_score", 1.0) <= max_risk_score]
    
    return suitable_products
