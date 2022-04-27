import datetime
from mongoengine import SequenceField, StringField, DateTimeField, Document, IntField


class Notes(Document):
    id = SequenceField(primary_key=True)
    user_id = IntField(nullable=False)
    title = StringField(max_length=100, nullable=False)
    description = StringField(max_length=500)
    date_created = DateTimeField(default=datetime.datetime.now)
    date_updated = DateTimeField(default=datetime.datetime.now)

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "date_created": str(self.date_created),
            "date_updated": str(self.date_updated)

        }
