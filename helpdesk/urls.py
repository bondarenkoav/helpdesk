from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.contrib.auth import logout
from dashboard.views import close_tab, journal_events
from accounts.views import forgot_password, change_password, register_account, page_error403, page_error503, \
    update_profile, page_error423, change_cur_scompany
from accounts.views import user_profile, user_settings
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),

    url(r'^accounts/register_account/$', register_account, name="register_account"),
    url(r'^accounts/forgot_password/$', forgot_password, name="forgot_password"),
    url(r'^accounts/change_password/(?:(?P<username>\w+)&(?P<psw_sms>\w+)/)?$', change_password, name="change_password"),
    url(r'^accounts/update_profile/$', update_profile, name="update_profile"),
    url(r'^accounts/logout/$', logout, name="logout"),
    url(r'^accounts/profile/$', RedirectView.as_view(url='/')),
    url(r'^profile/$', user_profile, name='profile'),
    url(r'^settings/$', user_settings, name='settings'),
    url(r'^tasks/', include('tasks.urls', namespace='tasks')),

    url(r'^jornals/events/', journal_events, name='events'),

    url(r'^page_error403', page_error403, name="page_error403"),
    url(r'^page_error423', page_error423, name="page_error423"),
    url(r'^page_error503', page_error503, name="page_error503"),

    url(r'^close_tab/', close_tab, name='close_tab'),
    url(r'^change_scompany/', change_cur_scompany, name='change_cur_scompany'),

    url(r'^exploitation/', include('exploitation.urls', namespace='exploitation')),
    url(r'^build/', include('build.urls', namespace='build')),
    url(r'^maintenance/', include('maintenance.urls', namespace='maintenance')),
    url(r'^simmanage/', include('sim.urls', namespace='simmanage')),

    url(r'^reference_books/', include('reference_books.urls', namespace='reference_books')),
    url(r'^reports/', include('report.urls', namespace='reports')),

    # DRF
    path('api/', include('api.urls', namespace='api')),
    path('api/drf-auth/', include('rest_framework.urls')),
    # path('api/auth/', include('djoser.urls')),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),

    url(r'^', include('dashboard.urls', namespace='dashboard')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)