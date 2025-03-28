from marshmallow import Schema, fields, validate

# Keeping this commented for simpler testing purposes...
class UserSchema(Schema):
    # username = fields.String(required=True, validate=validate.Length(3, 20), allow_none=False)
    # password = fields.String(required=True, validate=validate.Length(min=8), allow_none=False)
    # email = fields.Email(required=True)
    firstName = fields.String(required=True, validate=validate.Length(2, 15), allow_none=False)
    lastName = fields.String(required=True, validate=validate.Length(2, 15), allow_none=False)
    # studySets = fields.Dict(required=False)


class StudySetSchema(Schema):
    setName = fields.String(required=True, validate=validate.Length(1, 20), allow_none=False)
    timeStamp = fields.Time(required=False)
    setDescription = fields.String(required=True, validate=validate.Length(min=10), allow_none=False)
    terms = fields.Dict(required=True, keys=fields.Str(), values=fields.Str())