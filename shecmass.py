class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "FirstName", "LastName", "email", "Password")
        model = instructor
        ordered = True
    username = fields.String(required=True)
    password_hash = fields.String(required=True, load_only=True, data_key="password")
    email = fields.Email(required=True)
    # role = fields.String(required=True, validate=lambda n: n == 'user' or n == 'admin')
    # phone = fields.String(required=False)


