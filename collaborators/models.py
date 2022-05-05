from mongoengine import Document, SequenceField, StringField, ListField, IntField, EmailField


class Collaborators(Document):
    id = SequenceField(primary_key=True)
    email = EmailField(required=True)
    user_id = ListField(IntField(min_value=0, nullable=False))
    note_id = IntField(required=True)

    def to_json(self):
        return {'id': self.id,
                'email': self.email,
                'user_id': self.user_id,
                'note_id': self.note_id}
