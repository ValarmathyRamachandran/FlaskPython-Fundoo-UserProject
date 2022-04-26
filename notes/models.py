import datetime
from mongoengine import SequenceField, StringField, DateTimeField, Document


class Notes(Document):
    id = SequenceField(primary_key=True)
    user_id = SequenceField(nullable=False)
    title = StringField(max_length=100, nullable=False)
    description = StringField(max_length=500)
    date_created = DateTimeField(default=datetime.datetime.now)
    date_updated = DateTimeField(default=datetime.datetime.now)


def to_json(self):
    return {
        "title": self.title,
        "description": self.description,
        "date_created": self.date_created,
        "date_updated": self.date_updated
    }
