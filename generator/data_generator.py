# generator/data_generator.py

"""
Orchestrates synthetic data generation + MongoDB Atlas.

Calls each faker module, inserts the results into MongoDB,
and logs what was generated. Designed to be called by GitHub Actions.

Usage:
    python -m generator.data_generator
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
from pymongo.server_api import ServerApi

from config.settings import MONGO_URI, MONGO_DB, MONGO_COLLECTIONS, generate_batch_id
from generator import faker_customers, faker_products, faker_orders

def run_pipeline():
    """Generate customers → products → orders and insert into MongoDB."""
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]

    # Generate batch_id once so all records in this run share the same ID
    batch_id = generate_batch_id()
    print(f"  Batch ID: {batch_id}\n")  # Logging is used in production and not print

    try:
        # Generate and insert customers
        customers = faker_customers.generate_customers(batch_id)
        db[MONGO_COLLECTIONS["customers"]].insert_many(customers)
        print(f"  ✓ Inserted {len(customers)} customers")

        # Generate and insert products
        products = faker_products.generate_products(batch_id)
        db[MONGO_COLLECTIONS["products"]].insert_many(products)
        print(f"  ✓ Inserted {len(products)} products")

        # Get ALL customer IDs; use the generated products list so orders align 
        all_customer_ids = db[MONGO_COLLECTIONS["customers"]].distinct("customer_id")

        # Generate and insert orders
        orders = faker_orders.generate_orders(all_customer_ids, products, batch_id)
        db[MONGO_COLLECTIONS["orders"]].insert_many(orders)
        print(f"  ✓ Inserted {len(orders)} orders")

        client.close()

    finally:
        client.close()

    print("\n✓ Data generation complete.")


if __name__ == "__main__":
    run_pipeline()