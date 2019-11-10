from . import views
from django.urls import path, include

urlpatterns = [
	path('getOp/',views.OptionViewSet.as_view({'get':'getAllOption'}))
]