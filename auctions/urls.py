
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("product_form/",views.product_form,name="product_form"),
    path("product/<int:id>/",views.product_detail,name='product_details'),
    path("myListing/",views.myListing,name="myListing"),
    path("allcategories/",views.allcategories,name="allcategories"),
    path("category/<str:my_category>",views.categories,name="categories"),
    path("addtowatchList/<int:id>",views.addtowatchList,name="addtowatchList"),
    path("removefromwatchList/<int:id>",views.removefromwatchList,name="removefromwatchList"),
    path("viewwatchlist/",views.viewwatchList,name="viewwatchList"),
    path("addcomment/<int:id>/",views.add_comment,name="add_comment"),
    path("close_bid/<int:id>",views.close_bid,name="close_bid"),
    path("place_bid/<int:id>",views.place_bid,name="place_bid")
]




