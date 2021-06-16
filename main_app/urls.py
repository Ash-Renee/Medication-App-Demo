from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
path('', views.guest_view),
path('access', views.login),
path('verify', views.login_check),
path('dashboard', views.dashboard),
path('logout', views.logout),
path('cancel', views.cancel),
path('medication/new', views.add_med),
path('medication/create', views.create_med),
path('medication/<int:medication_id>', views.display_medication),
path('medication/<int:medication_id>/edit', views.edit_medication),
path('medication/<int:medication_id>/update', views.update_medication),
path('medication/<int:medication_id>/delete', views.delete_medication),
path('take_med', views.take_med),
path('undo_take', views.undo_take),
path('register', views.register),
]