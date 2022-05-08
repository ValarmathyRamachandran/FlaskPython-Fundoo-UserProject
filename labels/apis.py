from flask import request, json
from flask_restful import Resource

from common.token_operation import token_required
from labels.models import Label
from labels.validators import validate_add_label, validate_delete_label


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
            label = Label(label=data.get('label'), user_id=user_id)
            label.save()
            return {'msg': 'label added successfully', 'code': 201}
        return {'msg': 'Label Already exists', 'code': 409}


class DeleteLabel(Resource):
    @token_required
    def delete(self, label_name, **kwargs):

        user = kwargs.get('user')
        user_id = user.id
        if validate_delete_label(label_name):
            label = Label.objects.filter(user_id=user_id, label=label_name).first()
            return {'msg': 'Label deleted successfully' + label, 'code': 200}
