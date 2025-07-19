from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_product", views.add_product, name="add_product"),
    path("get_product_data", views.get_product_data, name="get_product_data"),
    path("product/<int:product_id>", views.product_detail, name="product_detail"),
    path("chat/start/<int:product_id>", views.start_chat, name="start_chat"),
    path("chat/<int:chat_id>/", views.chat_view, name="chat_view"),
    path("chat/initiate/<int:product_id>/<int:seller_id>/<int:buyer_id>/", views.chat_view, name="chat_initiate_view"),
    path("profile/<int:user_id>", views.profile_view, name="profile_view"),
    path("messages", views.messages_view, name="messages"),
    path("edit_product/<int:product_id>", views.edit_product, name="edit_product"),
    path("delete_product/<int:product_id>", views.delete_product, name="delete_product"),
    path("mark_as_sold/<int:product_id>", views.mark_as_sold, name="mark_as_sold"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("delete_chat/<int:chat_id>", views.delete_chat, name="delete_chat"),
    path("delete_message/<int:message_id>", views.delete_message, name="delete_message"),
]