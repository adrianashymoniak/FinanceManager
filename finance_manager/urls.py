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
    url(r'^categories/(?P<pk>\d+)/category-details/$', views.category_details, name='category-details'),
    url(r'^add-transaction/$', views.add_transaction, name='add-transaction-page'),
    url(r'^(?P<pk>\d+)/edit-transaction/$', views.edit_transaction, name='edit-transaction-page'),
    url(r'^(?P<pk>\d+)/delete-transaction/$', views.delete_transaction, name='delete-transaction'),
    url(r'^delete-all-transactions/$', views.delete_all_transactions, name='delete-all-transactions'),
    url(r'^(?P<pk>\d+)/delete-all-transaction-of-one-category/$', views.delete_all_transaction_of_one_category,
        name='delete-all-transaction-of-one-category'),

]
