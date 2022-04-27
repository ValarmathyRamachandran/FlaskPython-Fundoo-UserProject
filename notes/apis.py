from pkgutil import get_data

from flask import request, Flask, json, jsonify
from flask_restful import Resource

from common.token_operation import token_required
from notes.models import Notes

app = Flask(__name__)


class CreateNotes(Resource):

    def post(self):
        req_data = request.data
        data = json.loads(req_data)
        new_note = Notes(title=data['title'], description=data['description'])
        new_note.save()
        return {'msg': 'New note created successfully'}


class GetNotes(Resource):
    @token_required
    def get(self, *args, **kwargs):
        #user = kwargs.get('user')
        #user_id = user.id
        #print(user_id)

        notes = Notes.objects()

        if not notes:
            return {'error': 'Notes info not found'}
        else:
            all_notes = [note.to_json() for note in notes]
            return {"Notes-info": all_notes}


class UpdateNote(Resource):
    @token_required
    def put(self, *args, **kwargs):
        user = kwargs.get('user')
        user_id = user.id
        print(user_id)
        record = json.loads(request.data)
        notes = Notes.objects(title=record['title'])
        if not notes:
            return {'error': 'notes  not found'}
        else:
            notes.update(title=record['new_title'], description=record['description'])
            return {'msg': 'note was successfully updated', 'code': 200}


class DeleteNote(Resource):
    @token_required
    def delete(self, *args, **kwargs):
        record = json.loads(request.data)
        notes = Notes.objects(title=record['title'])
        if not notes:
            return {'error': 'notes not found'}
        else:
            notes.delete()
        return {'msg': 'notes deleted successfully', 'code': 200}
