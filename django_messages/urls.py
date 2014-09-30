from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from .views import (inbox, outbox, compose, reply, view, delete,
                    undelete, trash)

redirect_to_inbox = RedirectView.as_view(url=reverse_lazy('messages_inbox'))

urlpatterns = patterns('',
                       url(r'^$', redirect_to_inbox,
                           name='messages_redirect'),
                       url(r'^inbox/$', inbox, name='messages_inbox'),
                       url(r'^outbox/$', outbox, name='messages_outbox'),
                       url(r'^compose/$', compose, name='messages_compose'),
                       url(r'^compose/(?P<recipient>[\w.@+-]+)/$', compose,
                           name='messages_compose_to'),
                       url(r'^reply/(?P<message_id>[\d]+)/$', reply,
                           name='messages_reply'),
                       url(r'^view/(?P<message_id>[\d]+)/$', view,
                           name='messages_detail'),
                       url(r'^delete/(?P<message_id>[\d]+)/$',
                           delete, name='messages_delete'),
                       url(r'^undelete/(?P<message_id>[\d]+)/$', undelete,
                           name='messages_undelete'),
                       url(r'^trash/$', trash, name='messages_trash')
                       )
