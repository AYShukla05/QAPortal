from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings
# from .views import RegisterView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path("token", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("create-profile", views.createUser),
    path("update-profile/<str:pk>", views.updateProfile),
    path("delete-profile/<str:pk>", views.deleteProfile),
    path("profiles", views.getProfiles),
    path("profiles/<str:pk>", views.getProfile),
    path("profile", views.profile),
    path("posts", views.getPosts),
    path("posts/<str:pk>", views.getPost),
    path("create-post", views.createPost),
    path("update-post/<str:pk>", views.updatePost),
    path("delete-post/<str:pk>", views.deletePost),
    path("add-comment/<str:pk>", views.addComment),
    path("get-comments/<str:pk>", views.getComments),
    path("edit-comment/<str:pk>", views.editComment),
    path("delete-comment/<str:pk>", views.deleteComment),
    path("add-vote/<str:pk>", views.addVote),
    path("subscribe", views.subscribe),
    path("get-subscribed", views.getSubscribed),
    path("get-notifications", views.getNotifications),
    path("get-my-profile", views.getMyProfile)
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)