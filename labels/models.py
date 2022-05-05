from mongoengine import Document, StringField, SequenceField, IntField, ListField


class Label(Document):
    id = SequenceField(primary_key=True)
    user_id = IntField(min_value=0, nullable=False)
    label = StringField(min_length=1)

    def to_json(self):
        return{'id':self.id,
               'user_id':self.user_id,
               'label':self.label}

