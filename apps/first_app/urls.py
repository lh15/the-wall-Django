from django.conf.urls import url
from views import *
urlpatterns = [
	url(r'^$', index, name = 'index'),
    url(r'^login$', login, name = 'login'),
    url(r'^log_out$', log_out, name = 'log_out'),
    url(r'^process$', process, name = 'process'),
    url(r'^process_login$', submit_login, name = 'process_login'),
    url(r'^process_message$', post_message, name = 'process_message'),
    url(r'^success$', success, name = 'success'),
    url(r'^wall$', wall, name = 'wall'),
    url(r'^process_comment/(?P<message_id>[^\n]+)/$', post_comment, name = 'process_comment'),
    url(r'^delete_comment/(?P<id>[^\n]+)/$', delete_comment, name = 'delete_comment'),
    url(r'^delete_message/(?P<id>[^\n]+)/$', delete_message, name = 'delete_message')
]