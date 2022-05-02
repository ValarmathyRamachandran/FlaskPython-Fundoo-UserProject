from mongoengine import Document, StringField, SequenceField, IntField


class Label(Document):
    id = SequenceField(primary_key=True)
    note_id = IntField()
    user_id = IntField(max_length=25)
    label = StringField(min_length=1, max_length=50)
