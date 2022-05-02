from .models import Label


def validate_add_label(data):
    label = data.get('label')
    user_id = data.get('user_id')
    label = Label.objects.filter(user_id=user_id, label=label).first()
    if label:
        return False
    return True



