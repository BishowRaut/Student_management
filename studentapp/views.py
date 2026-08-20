from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from .models import Student


# =========================================================
# HOME
# =========================================================

@login_required
def home(request):
    total_students = Student.objects.count()

    context = {
        "total_students": total_students,
    }

    return render(
        request,
        "studentapp/home.html",
        context
    )


# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Automatically login after registration
            login(request, user)

            return redirect("home")

    else:
        form = UserCreationForm()

    return render(
        request,
        "studentapp/register.html",
        {
            "form": form
        }
    )


# =========================================================
# LOGIN
# =========================================================

def user_login(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect("home")

    else:
        form = AuthenticationForm()

    return render(
        request,
        "studentapp/login.html",
        {
            "form": form
        }
    )


# =========================================================
# LOGOUT
# =========================================================

@login_required
def user_logout(request):

    if request.method == "POST":

        logout(request)

        return redirect("login")

    return redirect("home")


# =========================================================
# STUDENT LIST / SEARCH
# Permission: view_student
# =========================================================

@login_required
@permission_required(
    "studentapp.view_student",
    raise_exception=True
)
def student_list(request):

    search = request.GET.get(
        "search",
        ""
    ).strip()

    if search:

        students = (
            Student.objects.filter(
                name__icontains=search
            )
            |
            Student.objects.filter(
                email__icontains=search
            )
        ).distinct()

    else:

        students = Student.objects.all()

    context = {
        "students": students,
        "search": search,
        "total_students": Student.objects.count(),
    }

    return render(
        request,
        "studentapp/students.html",
        context
    )


# =========================================================
# ADD STUDENT
# Permission: add_student
# =========================================================

@login_required
@permission_required(
    "studentapp.add_student",
    raise_exception=True
)
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

    return render(
        request,
        "studentapp/add_student.html"
    )


# =========================================================
# EDIT STUDENT
# Permission: change_student
# =========================================================

@login_required
@permission_required(
    "studentapp.change_student",
    raise_exception=True
)
def edit_student(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

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
        {
            "student": student
        }
    )


# =========================================================
# DELETE STUDENT
# Permission: delete_student
# =========================================================

@login_required
@permission_required(
    "studentapp.delete_student",
    raise_exception=True
)
def delete_student(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    if request.method == "POST":

        student.delete()

        return redirect("student_list")

    return render(
        request,
        "studentapp/delete_student.html",
        {
            "student": student
        }
    )