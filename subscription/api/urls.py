from django.urls import path
from api.api import endpoints

app_name = 'app'

urlpatterns = [
    path('editors/', endpoints.EditorListView.as_view(), name='editor_list'),
    path('editors/<pk>', endpoints.EditorDetailView.as_view(), name='editor_detail')
]
