from contact.models import Contact
from advanced.cloud import send


def send_gcm_messages(thread, sender, time):
    subscriptions = Contact.objects.filter(thread=thread, favourite=True)
    recipients = [x.user for x in subscriptions]
#    if sender in recipients:
#        recipients.remove(sender)
    data = dict()
    data['thread'] = thread.get_reference().get_name()
    data['reference'] = thread.id
    data['sender'] = sender.name
    data['time'] = time
    send(recipients, data)