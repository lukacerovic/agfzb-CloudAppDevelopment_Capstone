from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path('', views.index, name='index'),
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path('djangoapp/about/', views.about, name='about'),
    # path for about view

    # path for contact us view
    path('djangoapp/contact/', views.contact, name='contact'),

    # path for registration
    path('djangoapp/signup/', views.signup, name='signup'),

    # path for login
    path('login/', views.login_request, name='login'),
    
    # path for logout
    path('logout/', views.logout_request, name='logout'),

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),

    # path for add a review view
    path('dealer/<int:dealer_id>/add_review/', views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
