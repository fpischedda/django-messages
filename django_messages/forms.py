from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django_messages.models import Message
from django_messages.fields import CommaSeparatedUserField
from dashboard.models import DashboardOption


def append_signature(user, body):

    signature = ""
    try:
        signature = DashboardOption.objects.get(pk='message_signature').value
    except:
        pass

    return "{body}\n{first_name} {last_name}\n{signature}".format(
        body=body, first_name=user.first_name, last_name=user.last_name,
        signature=signature)


class ComposeForm(forms.Form):
    """
    A simple default form for private messages.
    """
    recipient = CommaSeparatedUserField(label=_(u"Recipient"),
                                        widget=forms.HiddenInput)
    subject = forms.CharField(label=_(u"Subject"), max_length=120)
    body = forms.CharField(label=_(u"Body"),
                           widget=forms.Textarea(attrs={'rows': '30',
                                                        'cols': '90'}))
    file = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        recipient_filter = kwargs.pop('recipient_filter', None)
        super(ComposeForm, self).__init__(*args, **kwargs)
        if recipient_filter is not None:
            self.fields['recipient']._recipient_filter = recipient_filter

    def save(self, sender, parent_msg=None):
        recipients = self.cleaned_data['recipient']
        subject = self.cleaned_data['subject']
        body = append_signature(sender, self.cleaned_data['body'])
        message_list = []
        for r in recipients:
            msg = Message(
                sender=sender,
                recipient=r,
                subject=subject,
                body=body,
            )
            if parent_msg is not None:
                msg.parent_msg = parent_msg
                parent_msg.replied_at = timezone.now()
                parent_msg.save()
            msg.save()
            message_list.append(msg)

        return message_list
