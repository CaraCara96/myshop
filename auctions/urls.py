from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("watch_list", views.watch_list, name="watch_list"),
    path("create_listing", views.create, name="create"),
    path("listing/<int:list_id>/", views.listing, name="listing"),
    path("new_bid/<int:bid_item>/", views.new_bid, name="new_bid"),
    path("new_comment/<int:comment_id>", views.new_comment, name="new_comment"),
    path("list_item/<int:watch_id>/", views.list_item, name="list_item"),
    path("remove_item/<int:rem_id>/", views.remove_item, name="remove_item"),
    path("category/<str:cat>/", views.category, name="category"),
    path("my_listing", views.my_listing, name="my_listing"),
    path("update/<int:list_id>/", views.update, name="update" ),
    path("delete/<int:list_id>/", views.delete, name="delete"),
    path("close_listing/<int:list_id>", views.close_listing, name="close_listing"),
    path("closed_listing", views.closed_listing, name="closed_listing"),
    path("bids", views.bids, name="bids")
]
