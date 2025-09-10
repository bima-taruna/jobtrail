from  typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]) :
    data:List[T]
    page:int
    page_size:int
    total:int