from datetime import datetime
from flask import request, Flask, json, jsonify
from flask_restful import Resource

from common.token_operation import token_required
from notes.models import Notes

app = Flask(__name__)


class CreateNotes(Resource):
    @token_required
    def post(self, *args, **kwargs):
        req_data = request.data
        data = json.loads(req_data)
        user = kwargs.get('user')
        user_id = user.id
        new_note = Notes(user_id=user_id, title=data.get('title'), description=data.get('description'), is_deleted=False,
                         is_pinned=False, is_archived=False)
        if len(new_note.title) <= 0:
            return {'msg': 'Please enter required details', 'code': 400}
        new_note.save()
        return {'msg': 'New note created successfully', 'code': 200}


class GetNotes(Resource):
    @token_required
    def get(self, *args, **kwargs):
        user = kwargs.get('user')
        user_id = user.id
        notes = Notes.objects.filter(user_id=user_id, is_deleted=False, is_archived=False)

        if not notes:
            return {'error': 'Notes info not found'}

        all_notes = [note.to_json() for note in notes.order_by('is-pinned') ]

        return {'msg': all_notes}


class UpdateNote(Resource):
    @token_required
    def put(self, *args, **kwargs):
        user = kwargs.get('user')
        user_id = user.id
        record = json.loads(request.data)

        notes = Notes.objects.get(id=record['id'])

        if not notes:
            return {'error': 'notes  not found'}

        notes.title = record['new_title']
        notes.description = record['new_description']
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
            return {'error': 'Notes info not found'}

        all_notes = [note.to_json() for note in notes]
        return {"Deleted Notes": all_notes}


class GetPinned(Resource):
    @token_required
    def get(self, *args, **kwargs):
        user = kwargs.get('user')
        user_id = user.id
        notes = Notes.objects.filter(user_id=user_id, is_pinned=True)

        if not notes:
            return {'error': 'Notes info not found'}

        all_notes = [note.to_json() for note in notes]
        return {"Pinned Notes ": all_notes}


class GetArchived(Resource):
    @token_required
    def get(self, *args, **kwargs):
        user = kwargs.get('user')
        user_id = user.id
        notes = Notes.objects.filter(user_id=user_id, is_archived=True)

        if not notes:
            return {'error': 'Notes info not found'}

        all_notes = [note.to_json() for note in notes]
        return {"Archived Notes ": all_notes}
