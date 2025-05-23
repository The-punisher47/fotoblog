#<!-- filepath: d:\Desktop\fotoblog\fotoblog\fotoblog\urls.py-->

from django.contrib import admin
from django.urls import path, include
from authentification import views as auth_views
from blog import views as blog_views
from blog import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', auth_views.logout_user, name='logout'),
    path('home/', blog_views.home, name='home'),  # Page d'accueil avec un message
    path('', auth_views.LoginPageView.as_view(), name='login'),
    path('signup/', auth_views.signup_page, name='signup'),
    path('gestion/', blog_views.gestion_view, name='gestion'),  # Page GESTION avec le tableau
    path('NOTIFICATIONS/', blog_views.NOTIFICATIONS_view, name='NOTIFICATIONS'),
    path('TABLEAU_BORD/', blog_views.tableau_bord_view, name='TABLEAU_BORD'),
    path('add-jante/', blog_views.add_jante_view, name='add_jante'),
    path("ajouter-depose/<int:jante_id>/", views.ajouter_depose, name="ajouter_depose"),
    path("retirer-depose/<int:jante_id>/", views.retirer_depose, name="retirer_depose"),
    path("update-obs/<int:jante_id>/", views.update_obs, name="update_obs"),
    path('export-pdf/', views.export_table_pdf, name='export_table_pdf'),
    path('export-excel/', views.export_table_excel, name='export_table_excel'),
    path('mark-notifications-as-read/', blog_views.mark_notifications_as_read, name='mark_notifications_as_read'),
    path('check-unread-notifications/', blog_views.check_unread_notifications, name='check_unread_notifications'),
    
    path('ajouter-depose/<int:jante_id>/', views.ajouter_depose, name='ajouter_depose'),
    path('retirer-depose/<int:jante_id>/', views.retirer_depose, name='retirer_depose'),
    path('', include('blog.urls')),  # Inclure les URLs de l'application blog
    # Ajouter ces nouvelles routes

    path('profile/', blog_views.user_profile, name='user_profile'),
    path('historique/', blog_views.action_history, name='action_history'),
    path('gestion-utilisateurs/', blog_views.user_management, name='user_management'),
    path('toggle-admin/<int:user_id>/', blog_views.toggle_superuser, name='toggle_superuser'),
    
    path('notifications/count/', views.unread_notifications_count, name='notifications_count'),


]