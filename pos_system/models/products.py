from config.db import get_db

db=get_db()
products_collection=db["products"]


def add_products(name, barcode, price, qty):
    product = {
        "name": name,
        "barcode": str(barcode),
        "price": price,
        "qty": qty
    }
    products_collection.insert_one(product)


def get_products_by_barcode(barcode):
    return products_collection.find_one({"barcode":str(barcode)})
    
def update_stock(barcode,qty_sold):
    products_collection.update_one(
        {"barcode":barcode},
        {"$inc":{"stock": -qty_sold}}
    )


    