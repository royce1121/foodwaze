from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        r'^$',
        views.StartPageView.as_view(),
        name='start_page'
    ),
    url(
        r'^restaurants/$',
        views.RestaurantListView.as_view(),
        name='restau_list'
    ),
    url(
        r'^restaurants/action/$',
        views.CRUDRestaurantView.as_view(),
        name='restau_action'
    ),
    url(
        r'^restaurants/~ajax/$',
        views.RestaurantDataAjax.as_view(),
        name='map_ajax_click'
    ),
    url(
        r'^restaurants/update-menu/$',
        views.RestaurantMenuView.as_view(),
        name='menu_view',
    ),
    url(
        r'^restaurants/update-menu/(?P<pk>\d+)/$',
        views.RestaurantMenuView.as_view(),
        name='menu_view',
    ),
    url(
        r'^restaurants/menu-list/(?P<pk>\d+)/$',
        views.MenuListView.as_view(),
        name='menu_list_view',
    ),
    url(
        r'^restaurants/menu-list/(?P<pk>\d+)/(?P<add_visitor>[\w-]+)/$',
        views.MenuListView.as_view(),
        name='menu_list_view',
    ),
    url(
        r'^restaurants/statistics/$',
        views.StatisticsView.as_view(),
        name='statistics',
    ),
]