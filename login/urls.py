from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
 path('', views.home, name='home'),
 path('register/', views.register, name='register'),
 path('login/', views.signin, name='login'),
 path('logout/', views.signout, name='logout'),
 path('addproduct/', views.addproduct, name='addproduct'),
 path('products/', views.viewproduct, name='viewproduct'),
 path('Products1/', views.viewproduct1, name='viewproduct1'),
 path('addcarpenter/', views.addcarpenter, name='addcarpenter'),
 path('carpenter/', views.viewcarpenter, name='viewcarpenter'),
 path('editcarpenter/<int:id>/', views.editcarpenter, name='editcarpenter'),
 path('color/', views.addcolour, name='addcolour'),
 path('viewcolor/', views.viewcolour, name='viewcolour'),
 path('addwood/', views.addwood, name='addwood'),
 path('viewwood/', views.viewwood, name='viewwood'),
 path('category/', views.addcategory, name='category'),
 path('viewcategory/', views.viewcategory, name='viewcategory'),
 path('customisedproduct/', views.customisedproduct, name='customisedproduct'),
 path('customisedorder/', views.customisedorder, name='customisedorder'),
 path('productorder/', views.productorder, name='productorder'),
 path('paymentdetails/', views.paymentdetails, name='paymentdetails'),
 path('delete/<int:user_id>/',views.delete, name='delete'),
 path('deleteproduct/<int:product_id>/',views.delete1, name='deleteproduct'),
 path('cart/', views.viewcart, name='viewcart'),
 path('checkout/', views.checkout, name='checkout'),
 path('addtocart/<int:product_id>/',views.addtocart, name='addtocart'),
 path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart')
 



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)