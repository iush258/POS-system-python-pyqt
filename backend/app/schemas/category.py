from pydantic import BaseModel , ConfigDict , Field

class CategoryCreate(BaseModel):
    name:str = Field(
        min_length=1,
        max_length=100,
    )
    description : str | None =Field(
        default=None,
        max_length=500,
    )

class CateogruUpdate(BaseModel):
    name:str | None = Field(
        default= None,
        min_length=1,
        max_length=500,
    )

class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes= True)
    id : int
    name: str
    description :str | None

