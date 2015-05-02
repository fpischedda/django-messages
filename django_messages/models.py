import os
from django.conf import settings
from django.db import models
#from django.db.models import signals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class MessageManager(models.Manager):

    def inbox_for(self, user):
        """
        Returns all messages that were received by the given user and are not
        marked as deleted.
        """
        return self.filter(
            recipient=user,
            recipient_deleted_at__isnull=True,
        )

    def outbox_for(self, user):
        """
        Returns all messages that were sent by the given user and are not
        marked as deleted.
        """
        return self.filter(
            sender=user,
            sender_deleted_at__isnull=True,
        )

    def trash_for(self, user):
        """
        Returns all messages that were either received or sent by the given
        user and are marked as deleted.
        """
        return self.filter(
            recipient=user,
            recipient_deleted_at__isnull=False,
        ) | self.filter(
            sender=user,
            sender_deleted_at__isnull=False,
        )


@python_2_unicode_compatible
class Message(models.Model):
    """
    A private message from user to user
    """
    subject = models.CharField(_("Subject"), max_length=120)
    body = models.TextField(_("Body"))
    sender = models.ForeignKey(AUTH_USER_MODEL, related_name='sent_messages',
                               verbose_name=_("Sender"))
    recipient = models.ForeignKey(AUTH_USER_MODEL,
                                  related_name='received_messages',
                                  verbose_name=_("Recipient"))
    parent_msg = models.ForeignKey('self', related_name='next_messages',
                                   null=True, blank=True,
                                   verbose_name=_("Parent message"))
    sent_at = models.DateTimeField(_("sent at"), auto_now_add=True)
    read_at = models.DateTimeField(_("read at"), null=True, blank=True)
    replied_at = models.DateTimeField(_("replied at"), null=True, blank=True)
    sender_deleted_at = models.DateTimeField(_("Sender deleted at"),
                                             null=True, blank=True)
    recipient_deleted_at = models.DateTimeField(_("Recipient deleted at"),
                                                null=True, blank=True)

    objects = MessageManager()

    def is_unread(self):
        """returns whether the recipient has read the message or not"""
        if self.read_at is not None:
            return False
        return True

    def replied(self):
        """returns whether the recipient has written a reply to this message"""
        if self.replied_at is not None:
            return True
        return False

    def has_attachments(self):
        """returns true if message has attachments"""
        if self.message_attachment.all().count() > 0:
            return True
        else:
            return False

    def attachments(self):
        """returns the list of attachments of this message"""
        return self.message_attachment.all()

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return ('messages_detail', [self.id])
    get_absolute_url = models.permalink(get_absolute_url)

    class Meta:
        ordering = ['-sent_at']
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")


def attachment_filename(instance, filename):
    return "{attachment_dir}/{message_id}/{filename}".format(
        attachment_dir=settings.ATTACHMENT_DIR,
        message_id=instance.message.id,
        filename=filename)


class MessageAttachment(models.Model):

    message = models.ForeignKey(Message, related_name='message_attachment')
    content = models.FileField(upload_to=attachment_filename)

    def filename(self):
        return os.path.basename(self.content.name)


def inbox_count_for(user):
    """
    returns the number of unread messages for the given user but does not
    mark them seen
    """
    return Message.objects.filter(recipient=user, read_at__isnull=True,
                                  recipient_deleted_at__isnull=True).count()
#
# fallback for email notification if django-notification could not be found
#if "notification" not in settings.INSTALLED_APPS:
#    from django_messages.utils import new_message_email
#    signals.post_save.connect(new_message_email, sender=Message)
