from decimal import Decimal
from pydantic import BaseModel , ConfigDict , Field

class ProductCreate(BaseModel):
    sku : str = Field(min_length=1,max_length=100)
    barcode :str = Field (min_length= 1, max_length=100)
    name :str = Field (min_length=1 , max_length=255)
    description : str | None = None
    unit_price : Decimal = Field (gt=0, decimal_places=2)
    tax_rate : Decimal =  Field (default=Decimal("0.00") , ge= 0 , le=100)
    category_id : int | None = None

class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = None
    unit_price: Decimal | None = Field(default=None, gt=0)
    tax_rate: Decimal | None = Field(default=None, ge=0, le=100)
    category_id: int | None = None
    is_active: bool | None = None


class ProductResponse(ProductCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
