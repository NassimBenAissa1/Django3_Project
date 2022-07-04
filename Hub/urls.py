from django.urls import path
from .views import homePage, list_Students, details_Student, details_Student404, StudentListView, StudentDetailView

urlpatterns = [
    path('', homePage, name="Home_Page"),
    path('listStudents', list_Students, name='Student_list'),
    path('Student/<int:id>', details_Student, name='Student_details'),
    path('Student404/<int:id>', details_Student404, name='Student_details404'),
    path('StudentListView', StudentListView.as_view(), name='Student_listView'),
    path('StudentDetail/<int:pk>', StudentDetailView.as_view(),
        name='Student_DetailView'),
]
