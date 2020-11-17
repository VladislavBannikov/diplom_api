from celery import shared_task
from django.http import JsonResponse

from shop.models import User, ConfirmEmailToken
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


@shared_task
def new_order_task(user_id):
    """
    отправяем письмо при изменении статуса заказа
    """
    # send an e-mail to the user
    user = User.objects.get(id=user_id)

    msg = EmailMultiAlternatives(
        # title:
        f"Обновление статуса заказа",
        # message:
        'Заказ сформирован',
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [user.email]

    )
    msg.send()


@shared_task
def new_user_registered_task(user_id, **kwargs):
    """
    отправляем письмо с подтвердждением почты
    """
    # send an e-mail to the user
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)

    msg = EmailMultiAlternatives(
        # title:
        f"Password Reset Token for {token.user.email}",
        # message:
        token.key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [token.user.email]
    )
    msg.send()
    return token.key


