from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from users.api import AccountRegisterResource, AccountLoginResource, AccountLogoutResource

urlpatterns = [
    url(r'^register/', csrf_exempt(AccountRegisterResource.as_list()), name='register'),
    url(r'^login/', csrf_exempt(AccountLoginResource.as_list()), name='login'),
    url(r'^logout/', csrf_exempt(AccountLogoutResource.as_list()), name='logout')
]
