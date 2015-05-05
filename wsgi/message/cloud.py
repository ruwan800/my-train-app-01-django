from contact.models import Contact
from advanced.cloud import send


def send_gcm_messages(thread, sender, time):
    subscriptions = Contact.objects.filter(thread=thread, favourite=True)
    recipients = [x.key for x in subscriptions]
    if sender.key in recipients:
        recipients.remove(sender.key)
    data = dict()
    data['thread'] = thread.get_reference().get_name()
    data['reference'] = thread.id
    data['sender'] = sender.name
    data['time'] = time
    send(recipients, data)