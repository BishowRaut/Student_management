from django.shortcuts import get_object_or_404, redirect, render

from .models import Student


def student_list(request):
    search = request.GET.get("search", "")

    if search:
        students = Student.objects.filter(
            name__icontains=search
        ) | Student.objects.filter(
            email__icontains=search
        )
    else:
        students = Student.objects.all()

    context = {
        "students": students,
        "search": search,
        "total_students": Student.objects.count(),
    }

    return render(request, "studentapp/student_list.html", context)


def add_student(request):
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        email = request.POST.get("email")
        address = request.POST.get("address")

        Student.objects.create(
            name=name,
            age=age,
            email=email,
            address=address,
        )

        return redirect("student_list")

    return render(request, "studentapp/add_student.html")


def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        student.name = request.POST.get("name")
        student.age = request.POST.get("age")
        student.email = request.POST.get("email")
        student.address = request.POST.get("address")

        student.save()

        return redirect("student_list")

    return render(
        request,
        "studentapp/edit_student.html",
        {"student": student},
    )


def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        student.delete()
        return redirect("student_list")

    return render(
        request,
        "studentapp/delete_student.html",
        {"student": student},
    )