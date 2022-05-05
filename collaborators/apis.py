import json

from flask import request
from flask_restful import Resource

from collaborators.models import Collaborators
from common.token_operation import token_required
from notes.models import Notes


class AddCollaborators(Resource):
    @token_required
    def post(self, **kwargs):
        """
            This API is used to Add multiple users
        """

        req_data = request.data
        data = json.loads(req_data)

        collaborator = Collaborators(user_id=data.get('user_id'), note_id=data.get('note_id'))
        collaborator.save()
        return {'msg': 'Collaborators added successfully', 'code': 201}
