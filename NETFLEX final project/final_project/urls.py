"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from renting import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #big NETFLEX logo    
	path('', views.home, name="home"),
    path('logged/<str:customer_id>', views.home_login, name="home_login"),

    #sign up page
	path('sign_up/', views.sign_up.as_view(), name="sign_up"),
    
    #log in page 
	path('login/', views.login, name="login"),

    path('store/', views.store, name="store"),  
    path('store_login/<str:customer_id>', views.store_login, name='store_login'),

    path('search/', views.search, name="Search"), 
    path('search_login/', views.search_login, name="Search_login"), 

    path('movie_detail/<str:movie_id>', views.movie_detail, name="movie_detail"),   
    path('movie_detail_login/<str:customer_id>/<str:movie_id>', views.movie_detail_login, name='movie_detail_login'),
	
	path('cart/<str:customer_id>', views.cart, name="cart"),
    path('cart/<str:customer_id>/<str:movie_id>', views.addcart, name="addcart"),
    path('cart2/<str:customer_id>/<str:movie_id>', views.addcart2, name="addcart2"),
    path('cart3/<str:customer_id>/<str:movie_id>', views.addcart3, name="addcart3"),
    path('cart4/<str:customer_id>/<str:movie_id>', views.removecart, name="removecart"),

	path('cart_submit/<str:customer_id>', views.cart_submit, name="cartsubmit"),

    path("library/<customer_id>", views.library, name="library")
]



