from marshmallow import Schema, fields, validate

# Keeping this commented for simpler testing purposes...
class UserSchema(Schema):
    firstName = fields.String(required=True, validate=validate.Length(2, 15), allow_none=False)
    lastName = fields.String(required=True, validate=validate.Length(2, 15), allow_none=False)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8), allow_none=False)
    flashcards = fields.Dict(required=False, keys=fields.Str() , values=fields.Str(), load_default={}) # Key: Set ID, Value: Set Name


class flashcardsSchema(Schema):
    setName = fields.String(required=True, validate=validate.Length(1, 20), allow_none=False)
    timeStamp = fields.Time(required=False)
    setDescription = fields.String(required=True, validate=validate.Length(min=10), allow_none=False)
    terms = fields.Dict(required=True, keys=fields.Str(), values=fields.Str())
