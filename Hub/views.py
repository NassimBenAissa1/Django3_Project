from pyexpat import model
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


from .models import Student

# Create your views here.
# function based views


def homePage(request):
    return HttpResponse('<h1>Welcome To ... </h1>')


def list_Students(request):
    list = Student.objects.all()
    return render(
        request,
        'Hub/list_students.html',
        {
            'students': list,
        },
    )


def details_Student(request, id):
    student = Student.objects.get(id=id)
    return render(
        request,
        'Hub/details_Student.html',
        {
            'student': student,
        }
    )


def details_Student404(request, id):
    student = get_object_or_404(Student, id=id)
    return render(
        request,
        'Hub/details_Student.html',
        {
            'student': student,
        }
    )


class StudentListView(ListView):
    model = Student
    template_name = "Hub/list_students.html"  # default: student_list
    context_object_name = "students"  # default: object_list


class StudentDetailView(DetailView):
    model = Student
    template_name = "Hub/details_Student.html"  # default: student_detail
