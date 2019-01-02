from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^categories/$', views.categories_page, name='categories-page'),
    url(r'^add-category/$', views.add_category, name='add-category-page'),
    url(r'^categories/(?P<pk>\d+)/edit-category/$', views.edit_category, name='edit-category-page'),
    url(r'^categories/(?P<pk>\d+)/delete-category/$', views.delete_category, name='delete-category'),

]
