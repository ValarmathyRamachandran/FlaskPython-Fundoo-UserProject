import datetime
from mongoengine import SequenceField, StringField, DateTimeField, Document
from wtforms import IntegerField


class Notes(Document):
    id = SequenceField(primary_key=True)
    user_id = IntegerField(nullable=False)
    title = StringField(max_length=100, nullable=False)
    description = StringField(max_length=500)
    date_created = DateTimeField(default=datetime.datetime.now)
    date_updated = DateTimeField(default=datetime.datetime.now)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date_created": str(self.date_created)

        }
