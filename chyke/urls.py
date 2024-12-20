from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('djoser.urls')),
    path('api/users/', include('users.urls')),  # Custom user-related URLs, like profile view
    path('api/events/', include('events.urls')),
    path('api/groups/', include('groups.urls')),
    path('api/', include('post.urls')),
    path('api/friends/', include('friends.urls')),
    path('api/story/', include('story.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)