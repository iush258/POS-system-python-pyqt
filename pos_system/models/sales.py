from config.db import get_db
from datetime import datetime
from bson import ObjectId
from models.products import get_products_by_barcode, update_stock

db = get_db()
sales_Coll=db["sales"]

def create_sale(cashier_nm):
    sale={
        "cashier":cashier_nm,
        "items":[],
        "total":0,
        "status":"open",
        "created_at": datetime.now()
    }
    result = sales_Coll.insert_one(sale)
    return str(result.inserted_id)


def add_item_to_sale(sale_id,barcode,qty):
    product= get_products_by_barcode(barcode)
    if product is None:
            raise ValueError("Product not found in Database")
        
    if product["qty"] < qty:
         print("not Enough Stock")
    
    subtotal = product["price"]*qty
    
    sales_Coll.update_one(
        { "_id":ObjectId(sale_id)},
        {
            "$push":{
                "items":{
                    "barcode":product["barcode"],
                    "name":product["name"],
                    "price":product["price"],
                    "qty":qty,
                    "subtotal":subtotal
                }
            },
            "$inc":{"total":subtotal}
        }

    )
    update_stock(barcode,qty)

def complete_sale(sale_id):
    sales_Coll.update_one(
    {"_id":ObjectId(sale_id)},
    {
        "$set":{
            "status":"completed",
            "completed_at":datetime.now()
        }
    }
    )

