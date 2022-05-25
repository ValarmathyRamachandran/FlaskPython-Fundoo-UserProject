from datetime import datetime, time
import redis
from flask import request, Flask, json
from flask_restful import Resource
from flask_restful_swagger import swagger

from collaborators.models import Collaborators
from common import logger
from common.exception import EmptyError, NotExist
from common.token_operation import token_required, set_cache
from labels import models
from notes.models import Notes

app = Flask(__name__)

r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True)


class CreateNotes(Resource):
    @token_required
    def post(self, **kwargs):
        """
        :param kwargs: includes user information
        :return: notes created
        """
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
                logger.logging.info('Note created')
                return {'msg': 'New note created successfully', 'code': 200}
        except EmptyError as e:
            return e.__dict__


class GetNotes(Resource):
    @swagger.model
    @swagger.operation(notes='swagger is working')
    @token_required
    def get(self, **kwargs):
        """
        :param kwargs: user information
        :return: all notes for the user
        """

        user = kwargs.get('user')
        user_id = user.id

        key = f"{user_id}"
        value = r.get(key)
        if value:
            data_value = json.loads(value)
            return data_value
        notes = Notes.objects.filter(user_id=user_id, is_deleted=False, is_archived=False)
        try:
            if not notes:
                raise NotExist('Notes info not found', 404)
            if notes:
                notes = Notes.objects.all().order_by('-is_pinned', '-date_updated')
                res = []
                for note in notes:
                    data = note.to_json()
                    collaborators = Collaborators.objects.filter(note_id=data.get('id')).values_list('user_id')
                    data['collaborators'] = collaborators.to_json()
                    label = data.get('label')
                    _label = []
                    for l in label:
                        _label.append(l.to_json())
                        data['label'] = _label

                    res.append(data)
                    set_cache(key, data, 30)
            return {'msg': 'success', 'code': 200, 'data': res}
        except NotExist as e:
            return e.__dict__


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
        logger.logging.info('note updated')
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
        logger.logging.info('note deleted')
        return {'msg': 'notes deleted successfully', 'code': 200}


class NoteOperations(Resource):
    @token_required
    def put(self, **kwargs):
        record = json.loads(request.data)
        note = Notes.objects.get(id=record['id'])
        if not note:
            return {'error': 'Notes info not found'}

        note.is_archived = True
        note.save()
        return {'msg': 'notes archived successfully', 'code': 201}

    def post(self, **kwargs):
        record = json.loads(request.data)
        note = Notes.objects.get(id=record['id'])
        if not note:
            return {'error': 'notes not found'}

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
        ids = request.args.get('id')

        user_id = user.id
        label_data = models.Label.objects.filter(user_id=user_id, label=label).first()
        if not label_data:
            label_data = models.Label(user_id=user_id, label=label)
            label_data.save()
        try:

            note = Notes.objects.filter(user_id=user_id, id=ids).first()
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
        collaborator = body.get('collaborator')
        user = kwargs.get('user')
        user_id = user.id
        collaborator_data = Collaborators.objects.filter(user_id=user_id).first()
        if not collaborator_data:
            collaborator_data = Collaborators(user_id=user_id, collaborator=collaborator)
            collaborator_data.save()
        try:

            note = Notes.objects.filter(user_id=user_id).first()
            if not note:
                raise ('Note is not present', 'code:400')
        except Exception as e:
            return e.__dict__
        for data in note.collabortor:
            if data.collabortor == collaborator:
                return {'Error': ' Already this Collaborator was added to this note', 'code': '400'}
        note.update(push__collaborators=collaborator_data)

        return {'msg': 'Collaborator added successfully', 'code': '200'}

# class Reminder(Resource):
#     @token_required
#     def post(self, **kwargs):
#         req_data = request.data
#         body = json.loads(req_data)
#         reminder = body.get('reminder')
#         notes = Notes()
#         now = int(round(time.time() * 1000))
#         then = now + 3600000  # one hour after `now`


# class Reminder(Resource):
#     @token_required
#     def post(self, **kwargs):
#         user = kwargs.get('user')
#         user_id = user.id
#         ids = request.args.get('id')
#         reminder = request.args.get('reminder')
#         try:
#
#             note = Notes.objects.filter(user_id=user_id, id=ids).first()
#             if not note:
#                 raise ('Note is not present', 'code:400')
#         except Exception as e:
#             return e.__dict__
#
#         note.update(push__label=reminder)
#         return {'msg': 'reminder added successfully', 'code': '200'}
#
#     def get(self, **kwargs):
#         user = kwargs.get('user')
#         user_id = user.id
#         note = Notes.objects.all()
#
#         reminder = Notes.objects.filter(Q(user_id=user_id) & Q(is_deleted=False)).exclude(reminder=None)
#
#         return {'msg': reminder, 'code': 200}
