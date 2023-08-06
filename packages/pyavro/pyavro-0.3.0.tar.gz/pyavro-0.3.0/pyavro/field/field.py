from pydantic import BaseModel, root_validator
from enum import Enum
from typing import Optional, List, Union, Any
import funcy as fn


class AvroFieldTypes(str, Enum):
    str = 'string'
    null = None
    int = 'int'
    float = 'float'
    bytes = 'bytes'
    long = 'long'
    double = 'double'

    @classmethod
    def list(cls) -> List[str]:
        return list(AvroFieldTypes.__members__.keys())


class AvroField(BaseModel):
    name: str
    type: Union[str, List[str]]
    default: Optional[Any]

    @staticmethod
    def check_for_null_in_list(vals):
        if (vals[0] != 'null') or (any(vals[1:]) == "null"):
            raise ValueError("The first index of AvroField(type) must be 'null' if field is nullable")

    @root_validator()
    def type_must_start_with_null_if_nullable(cls, values):
        default = fn.get_in(values, ["default"])
        _type = fn.get_in(values, ["type"])
        if default is None:
            if isinstance(_type, list):
                cls.check_for_null_in_list(_type)
        return values
