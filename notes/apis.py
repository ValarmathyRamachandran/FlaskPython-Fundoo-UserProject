from datetime import datetime
from flask import request, Flask, json
from flask_restful import Resource

import labels
from common.token_operation import token_required
from labels import models
from labels.models import Label
from notes.models import Notes

app = Flask(__name__)


class EmptyError(Exception):
    pass


class CreateNotes(Resource):
    @token_required
    def post(self, **kwargs):
        req_data = request.data
        data = json.loads(req_data)
        user = kwargs.get('user')
        user_id = user.id

        new_note = Notes(user_id=user_id, title=data.get('title'), description=data.get('description'),
                         is_deleted=False,
                         is_pinned=False, is_archived=False)
        try:
            if not new_note.title:
                raise EmptyError("Title should not be empty", 404)
            if new_note:
                new_note.save()
                return {'msg': 'New note created successfully', 'code': 200}
        except EmptyError as e:
            return e.__dict__


class GetNotes(Resource):
    @token_required
    def get(self, *args, **kwargs):
        user = kwargs.get('user')
        user_id = user.id
        notes = Notes.objects.filter(user_id=user_id, is_deleted=False, is_archived=False)

        if not notes:
            return {'error': 'Notes info not found', 'code': 404}

        # all_notes = [note.to_json() for note in notes]
        notes = Notes.objects.all()
        print(notes)
        res = []
        for note in notes:
            data = note.to_json()
            label = data.get('label')
            _label = []
            for l in label:
                _label.append(l.to_json())
                data['label'] = _label
                res.append(data)

            return {'msg': 'success', 'code': 200, 'data': res}


class UpdateNote(Resource):
    @token_required
    def put(self, *args, **kwargs):
        user = kwargs.get('user')
        user_id = user.id
        record = json.loads(request.data)

        notes = Notes.objects.get(id=record['id'])

        if not notes:
            return {'error': 'notes  not found'}

        notes.title = record.get('new_title')
        notes.description = record.get('new_description')
        notes.date_updated = datetime.now
        notes.user_id = user_id
        notes.save()

        return {'msg': 'note was successfully updated', 'code': 200}


class DeleteNote(Resource):
    @token_required
    def delete(self, *args, **kwargs):
        # user = kwargs.get('user')
        record = json.loads(request.data)
        note = Notes.objects.get(id=record['id'])
        if not note:
            return {'error': 'notes not found'}

        note.is_deleted = True
        note.save()
        return {'msg': 'notes deleted successfully', 'code': 200}


class NoteOperations(Resource):
    @token_required
    def put(self, *args, **kwargs):
        record = json.loads(request.data)
        note = Notes.objects.get(id=record['id'])
        if not note:
            return {'error': 'Notes info not found'}
        note.is_archived = True
        note.save()
        return {'msg': 'notes archived successfully', 'code': 201}

    def post(self):
        record = json.loads(request.data)
        note = Notes.objects.get(id=record['id'])
        if not note:
            return {'error': 'Notes info not found'}
        note.is_pinned = True
        note.save()
        return {'msg': 'notes Pinned successfully', 'code': 200}


class GetTrash(Resource):
    @token_required
    def get(self, *args, **kwargs):
        user = kwargs.get('user')
        user_id = user.id
        notes = Notes.objects.filter(user_id=user_id, is_deleted=True, is_archived=False)

        if not notes:
            return {'error': 'Notes info not found', 'code': 404}

        all_notes = [note.to_json() for note in notes]
        return {'msg': all_notes, 'code': 200}


class GetPinned(Resource):
    @token_required
    def get(self, *args, **kwargs):
        user = kwargs.get('user')
        user_id = user.id
        notes = Notes.objects.filter(user_id=user_id, is_pinned=True)

        if not notes:
            return {'error': 'Notes info not found', 'code': 404}

        all_notes = [note.to_json() for note in notes]
        return {'msg': all_notes, 'code': 200}


class GetArchived(Resource):
    @token_required
    def get(self, *args, **kwargs):
        user = kwargs.get('user')
        user_id = user.id
        notes = Notes.objects.filter(user_id=user_id, is_archived=True)

        if not notes:
            return {'error': 'Notes info not found', 'code': 200}

        all_notes = [note.to_json() for note in notes]
        return {'msg': all_notes, 'code': 200}


class NoteLabel(Resource):
    @token_required
    def post(self, **kwargs):
        req_data = request.data
        body = json.loads(req_data)
        label = body.get('label')
        user = kwargs.get('user')
        user_id = user.id
        label_data = models.Label.objects.filter(user_id=user_id, label=label).first()
        if not label_data:
            label_data = models.Label(user_id=user_id, label=label)
            label_data.save()
        try:

            note = Notes.objects.filter(user_id=user_id).first()
            if not note:
                raise ('Note is not present', 'code:400')
        except Exception as e:
            return e.__dict__
        for data in note.label:
            if data.label == label:
                return {'Error': 'label already present in this note', 'code': '400'}
        note.update(push__label=label_data)

        return {'msg': 'label added successfully', 'code': '200'}

    def patch(self, **kwargs):
        req_data = request.data
        body = json.loads(req_data)
        old_label = body.get('label')
        new_label = body.get('new_label')
        user = kwargs.get('user')
        user_id = user.id

        note = Notes.objects.filter(user_id=user_id).first()
        label2 = models.Label.objects.filter(user_id=user_id, label=new_label).first()
        if not label2:
            label2 = models.Label(user_name=user_id, label=new_label)
            label2.save()
        label_list = note.label
        for item in label_list:
            if item.label == old_label:
                label_list.remove(item)
                label_list.append(label2)
                note.update(label=label_list)
                return {'msg': 'label was updated', 'code': 200}
            return {'Error': 'Label not present in given note', 'code': 400}

    def delete(self, **kwargs):
        req_data = request.data
        body = json.loads(req_data)
        label = body.get('label')
        user = kwargs.get('user')
        user_id = user.id

        note = Notes.objects.filter(user_id=user_id).first()

        list_label = note.label
        for data in list_label:
            if data.label == label:
                list_label.remove(data)
                note.update(label=list_label)
                return {'msg': 'label was removed', 'code': 200}
        return {'Error': 'label  was not found in this note', 'code': 404}


class NoteCollaborators(Resource):
    @token_required
    def post(self, **kwargs):
        req_data = request.data
        body = json.loads(req_data)
        email = body.get('email')
        user = kwargs.get('user')
        user_id = user.id
        collaborator_data = models.Collaborator.objects.filter(user_id=user_id, email=email).first()
        if not collaborator_data:
            collaborator_data = models.Collaborator(user_id=user_id, email=email)
            collaborator_data.save()
        try:

            note = Notes.objects.filter(user_id=user_id).first()
            if not note:
                raise ('Note is not present', 'code:400')
        except Exception as e:
            return e.__dict__
        for data in note.email:
            if data.email == email:
                return {'Error': ' Already this Collaborator was added to this note', 'code': '400'}
        note.update(push__collaborators=collaborator_data)

        return {'msg': 'Collaborator added successfully', 'code': '200'}
