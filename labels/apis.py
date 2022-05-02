from flask import request, json, session
from flask_restful import Resource

from common.token_operation import token_required
from labels.models import Label
from labels.validators import validate_add_label


def valid_delete_label(label):
    pass


class AddLabel(Resource):
    @token_required
    def post(self, **kwargs):
        """
            This API is used to Addlabel
        """
        req_data = request.data
        data = json.loads(req_data)
        user = kwargs.get('user')
        user_id = user.id
        validate_data = validate_add_label(data)

        if validate_data:
            label = Label(note_id=data.get('note_id'), label=data.get('label'), user_id=user_id)
            label.save()
            return {'msg': 'label added successfully', 'code': 201}
        return {'msg': 'Label Already exists', 'code': 409}



