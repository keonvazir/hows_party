############### APP LEVEL ##############

from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register_page$', views.register_page),
    url(r'^user_profile/(?P<user_id>\d+)$', views.user_profile),
    url(r'^reg$', views.reg),
    url(r'^add_event/$', views.add_event),
    url(r'^create_event$', views.create_event),
    url(r'^show_event/(?P<event_id>\d+)$', views.show_event), 
    url(r'^find_friend$', views.find_friend), #add the id
    url(r'^photo$', views.photo), #may want to add id
    url(r'^meet_team$', views.meet_team),
    url(r'^logout$', views.logout),
    url(r'^user_profile/(?P<event_id>\d+)/destroy$', views.remove),
    url(r'^ajax_calls/search/', views.autocompleteModel),
    url(r'^add_message$', views.add_message),
    # url(r'^show_event/(?P<user_id>\d+)/destroy$', views.remove_friend),

]