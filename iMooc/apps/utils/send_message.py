from operation.models import UserMessage


def send_message(user, msg):
    UserMessage.objects.create(
        user=user.id,
        message=msg
    )
