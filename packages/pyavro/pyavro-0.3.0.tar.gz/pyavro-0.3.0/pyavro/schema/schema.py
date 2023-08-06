from pydantic import BaseModel, Field, validator
from typing import List
import fastavro as avro
from pyavro.util import match_regex_expr_or_error
from pyavro.field.field import AvroField


class AvroSchema(BaseModel):
    """
    Avro is used to define the data schema for a record's value. This schema describes the fields allowed in the value,
    along with their data types.

    You apply a schema to the value portion of an Oracle NoSQL Database record using Avro bindings.
    These bindings are used to serialize values before writing them, and to deserialize values after reading them.
    The usage of these bindings requires your applications to use the Avro data format, which means that each stored
    value is associated with a schema.

    Args:
        type: Identifies the JSON field type. For Avro schemas, this must always be record when it is specified at
        the schema's top level. The type record means that there will be multiple fields defined.

        namespace: This identifies the namespace in which the object lives. Essentially, this is meant to be a URI
        that has meaning to you and your organization. It is used to differentiate one schema type from
        another should they share the same name.

        name: This is the schema name which, when combined with the namespace, uniquely identifies the schema within
        the store.

        fields_: This is the actual schema definition. It defines what fields are contained in the value, and the
        data type for each field. A field can be a simple data type, such as an integer or a string, or it can
        be complex data. Note: The field is prefixed with an underscore here because it clashes with Pydantic reserved
        keywords. An alias is used here to ensure we deserialize with the right value.
    """
    type: str
    namespace: str
    name: str
    fields_: List[AvroField] = Field(..., alias="fields")

    @validator('name')
    def name_must_begin_with_letters(cls, value):
        expr = "^[A-Za-z_]"
        return match_regex_expr_or_error(value, 'name', expr)

    @validator('name')
    def name_must_only_contain(cls, value):
        expr = "[A-Za-z0-9_]"
        return match_regex_expr_or_error(value, 'name', expr)

    def parse(self):
        dict_schema = self.dict(by_alias=True)
        parsed_schema = avro.parse_schema(dict_schema, _write_hint=False)
        return parsed_schema
