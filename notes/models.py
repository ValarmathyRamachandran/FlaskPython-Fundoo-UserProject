import datetime
from mongoengine import SequenceField, StringField, DateTimeField, Document, IntField, BooleanField, ListField


class Notes(Document):
    id = SequenceField(primary_key=True)
    user_id = ListField(IntField(nullable=False))
    title = StringField(max_length=100, nullable=False)
    description = StringField(max_length=500)
    date_created = DateTimeField(default=datetime.datetime.now)
    date_updated = DateTimeField(default=datetime.datetime.now)
    is_pinned = BooleanField(default=False)
    is_deleted = BooleanField(default=False)
    is_archived = BooleanField(default=False)

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "date_created": str(self.date_created),
            "date_updated": str(self.date_updated),
            "is_pinned": str(self.is_pinned),
            "is_deleted": str(self.is_deleted),
            "is_archived":str(self.is_archived)

        }
