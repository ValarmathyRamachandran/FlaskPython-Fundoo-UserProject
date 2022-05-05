from mongoengine import Document, SequenceField, StringField, ListField, IntField, EmailField


class Collaborators(Document):
    id = SequenceField(primary_key=True)
    email = ListField(EmailField(required=True))
    user_id = ListField(IntField(min_value=0, nullable=False))
    note_id = IntField(required=True)
