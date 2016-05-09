from django.conf.urls import include, patterns, url
import user.views
from .views import SignUpView

urlpatterns = [
    url(r'^home$', user.views.home, name='user_home'),
    url(r'^signup$', SignUpView.as_view(), name='user_signup')
]
