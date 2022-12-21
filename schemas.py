from typing import Dict, Any

from marshmallow import fields, Schema, validates_schema, ValidationError


class RequestParamsSchema(Schema):
    cmd = fields.Str(required=True)
    value = fields.Str(required=True)

    @validates_schema
    def validate_cmd_params(self, values: Dict[str, str], *args: Any, **kwargs: Any) -> Dict[str, str]:
        validate_cmd_commands = {'filter', 'sort', 'map', 'limit', 'unique'}

        if values['cmd'] not in validate_cmd_commands:
            raise ValidationError({'cmd': f'contains invalid command={values["cmd"]}'})

        return values


class RequestParamListSchema(Schema):
    queries = fields.Nested(RequestParamsSchema, many=True)
    filename = fields.Str(required=True)
