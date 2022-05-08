import datetime
from mongoengine import SequenceField, StringField, DateTimeField, Document, IntField, BooleanField, ListField, \
    ReferenceField

import notes
from labels import models


class Notes(Document):
    id = SequenceField(primary_key=True)
    user_id = IntField(max_value=50, min_value=0, nullable=False)
    title = StringField(max_length=100, nullable=False)
    description = StringField(max_length=500)
    date_created = DateTimeField(default=datetime.datetime.now)
    date_updated = DateTimeField(default=datetime.datetime.now)
    is_pinned = BooleanField(default=False)
    is_deleted = BooleanField(default=False)
    is_archived = BooleanField(default=False)
    label = ListField(ReferenceField(models.Label))

    # collaborators = ListField(ReferenceField('self', required=False))

    def to_json(self):
        notes = dict()
        notes['id'] = self.id
        notes['user_id'] = self.user_id
        notes['title'] = self.title
        notes['description'] = self.description
        notes['date_created'] = str(self.date_created)
        notes['date_updated'] = str(self.date_updated)
        notes['is_pinned'] = str(self.is_pinned)
        notes['is_deleted'] = str(self.is_deleted)
        notes['is_archived'] = str(self.is_archived)
        notes['label'] = self.label
        # notes['collaborators'] = self.collaborators
        return notes

        # "id": self.id,
    # "user_id": self.user_id,
    # "title": self.title,
    # "description": self.description,
    # "date_created": str(self.date_created),
    # "date_updated": str(self.date_updated),
    # "is_pinned": str(self.is_pinned),
    # "is_deleted": str(self.is_deleted),
    # "is_archived": str(self.is_archived),
    # "label": str(self.label)
