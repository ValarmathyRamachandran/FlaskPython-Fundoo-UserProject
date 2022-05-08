import json

from flask import request
from flask_restful import Resource

from collaborators.models import Collaborators
from common import logger
from common.token_operation import token_required
from notes.models import Notes
from user.models import Users


class AddCollaborators(Resource):
    @token_required
    def post(self, **kwargs):
        """
            This API is used to Add multiple user id
        """

        req_data = request.data
        data = json.loads(req_data)
        email = data.get('email')
        user = kwargs.get('user')
        users = Users.objects.filter(email=email)
        if users:
            collaborator = Collaborators(user_id=data.get('user_id'), note_id=data.get('note_id'))
            collaborator.save()
            logger.logging.info('added collaborators')
            return {'msg': 'Collaborators added successfully', 'code': 201}
        return {'msg': 'user doesnot exist', 'code': 404}
