from models.products import add_products, get_products_by_barcode
from models.sales import create_sale, add_item_to_sale, complete_sale 

add_products(
    name="Milk",
    barcode="1111",
    price=20,
    qty=100
)

product= get_products_by_barcode("1111")
print("Product:",product)


sale_id= create_sale("Ayush")
print("Sale id:",sale_id)

add_item_to_sale(sale_id, "1111", 2)


complete_sale(sale_id)

print("sale completed succesfully")