"""Generates synthetic order records."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from datetime import datetime, timezone

# pip install faker
from faker import Faker

from config.settings import ORDERS_MIN, ORDERS_MAX, REGIONS, PAYMENT_STATUSES


# ......Source generation settings (used by generator/)................

def introduce_bad_order_data(order: dict) -> dict: 
    """Introduce common order data quality issues in a simple, explainable way."""
    if random.random() < 0.08: # 8% missing customer reference
        order["customer_id"] = None
    
    if random.random() < 0.08: # 8% missing product reference
        order["product_id"] = None
    
    if random.random() < 0.06: # 6% invalid amount values
        order["amount"] = "Nan"
    
    return order

def generate_orders(customer_ids: list[int], products: list[dict], batch_id: str) -> list[dict]:
    count = random.randint(ORDERS_MIN, ORDERS_MAX)
    orders_data = []

    for _ in range(count):
        # pick a product (dict) and read its id/price
        product = random.choice(products)
        product_id = product.get("product_id")
        try:
            product_price = float(product.get("price", 0))
        except (TypeError, ValueError):
            product_price = 0.0

        # generate quantity once and compute unit_price so both fields match
        quantity = random.randint(1, 5)
        price = round(product_price, 2)

        new_order = {
            "order_id": f"ORD{random.randint(1000, 99999)}",
            "customer_id": random.choice(customer_ids),
            "product_id": product_id,
            "price": price,
            "region": random.choice(REGIONS),
            "quantity": quantity,
            "amount": round(quantity * price, 2),
            "payment_status": random.choice(PAYMENT_STATUSES),
            "batch_id": batch_id,
            "created_at": datetime.now(timezone.utc),
        }

        bad_order_data = introduce_bad_order_data(new_order)
        orders_data.append(bad_order_data)

    return orders_data

# print(generate_orders([f"CUST{random.randint(10000, 99999)}" for _ in range(20)],
#                     [f"PROD{random.randint(10000, 99999)}" for _ in range(10)],
#                     "batch_001"))


            