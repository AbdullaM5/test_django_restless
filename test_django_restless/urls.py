from django.conf.urls import url, include

urlpatterns = [
    url(r'account/', include('users.urls'))
]
