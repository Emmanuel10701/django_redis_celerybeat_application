from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from stories.views import ScheduleViewSet  # Changed from story_scheduler

router = routers.DefaultRouter()
router.register(r'schedules', ScheduleViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/blogs/', include('blogs.urls')),
]