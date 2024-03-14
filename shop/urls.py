from django.urls import path
from . import views

urlpatterns = [
    # path('gettoken/',CustomAuthToken.as_view()),
    path('get_products',views.getProducts),
    path("get_highlights",views.getHighlights),
    path('get_blogs',views.getBlogs),
    path('get_highlighted_products',views.getHighlightedProducts),
    path("product/<str:slug>",views.getProductBySlug),
    path("product_images/<str:slug>",views.getProductImageBySlug),
    path('product/check_product_availability/<slug:slug>',views.checkProductAvailability),
    path('give_cart_data',views.giveCartData),
    path('place_order',views.placeOrder),
    path('get_categories', views.getCategories),
    path('get_category/<str:slug>', views.getProductsByCategory),
    path('inquiry', views.contact),
    path('get_single_blog/<str:slug>',views.getBlogsBySlug),
]