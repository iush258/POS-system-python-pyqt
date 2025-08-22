from config.db import get_db

db=get_db
products_collection=db["products"]


def add_products(product_data):
    products_collection.insert_one(product_data)


def get_products_by_barcode(barcode):
    return products_collection.find_one({"barcode":barcode})


def update_stock(barcode,quantity_sold):
    products_collection.update_one(
        {"barcode":barcode},
        {"$inc":{"stock": -quantity_sold}}

    )


    