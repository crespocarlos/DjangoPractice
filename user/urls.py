from django.conf.urls import include, patterns, url
import user.views

urlpatterns = [
    url(r'^home$', user.views.home, name='user_home')
]
