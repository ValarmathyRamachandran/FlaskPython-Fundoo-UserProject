from mongoengine import Document, StringField, EmailField, BooleanField, DateTimeField, SequenceField


class Users(Document):
    id = SequenceField(primary_key=True)
    first_name = StringField(max_length=255)
    last_name = StringField(max_length=255)
    user_name = StringField(max_length=255)
    email = EmailField(unique=True, required=True)
    password = StringField()
    new_password = StringField()
    is_active = BooleanField(default=False)


def to_json(self):
    return {
        "id": self.id,
        "first_name": self.first_name,
        "last_name": self.last_name,
        "user_name": self.user_name,
        "email": self.email,
        "password": self.password,
        "is_activ": self.is_active}
