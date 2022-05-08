from mongoengine import Document, SequenceField, StringField, ListField, IntField, EmailField


class Collaborators(Document):
    id = SequenceField(primary_key=True)
    user_id = ListField(IntField(min_value=0, nullable=False))
    note_id = IntField(required=True)

    def to_json(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'note_id': self.note_id}

    # def to_json(self):
    #   collaborators = dict()
    #  collaborators['id'] = self.id
    # collaborators['email'] = self.email
    # collaborators['user_id '] = self.user_id
    # collaborators['note_id'] = self.note_id
    # return collaborators
