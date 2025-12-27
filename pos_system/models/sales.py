from config.db import get_db
from datetime import datetime
from bson import ObjectId

db = get_db()
sales_Coll=db["sales"]

def create_sale(cashier_nm):
    """start a new sale(bill)"""
    sale={
        "cashier":cashier_nm,
        "items":[],
        "total":0,
        "status":"open",
        "created_at": datetime.now()
    }
    result = sales_Coll.insert_one(sale)
    return str(result.inserted_id)


def add_item_to_sale(sale_id,prd,qty):
    """Add product to the current sale"""
    subtotal = product["price"]*qty

    sales_Coll.update_one(
        { "_id":ObjectId(sale_id)},
        {
            "$push":{
                "items":{"barcode":product["barcode"],
                        "name":product["name"],
                        "price":product["price"],
                        "qty":qty,
                        "subtotal":subtotal
                        }
                    },
            "$inc":{"total":subtotal}
        }

    )

def complete_sale(sale_id,payment_method="cash"):
    """Mark the sale as completed """
    sales_Coll.update_one(
    {"_id":ObjectId(sale_id)},
    {
        "$set":{
            "status":"completed",
            "payment_method":payment_method,
            "completed_at":datetime.now
        }
    }
    )

def get_sales(sale_id):
    """fetch sales details"""
    return sales_Coll.find_one({"_id":ObjectId(sale_id)})

def list_sales():
    """list all completed sales"""
    return list(sales_Coll.find())