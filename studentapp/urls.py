from django.urls import path

from . import views


urlpatterns = [

    # =====================================================
    # HOME
    # =====================================================

    path(
        "",
        views.home,
        name="home"
    ),


    # =====================================================
    # AUTHENTICATION
    # =====================================================

    path(
        "login/",
        views.user_login,
        name="login"
    ),

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),


    # =====================================================
    # STUDENT MANAGEMENT
    # =====================================================

    # View / Search Students
    path(
        "students/",
        views.student_list,
        name="student_list"
    ),

    # Add Student
    path(
        "add/",
        views.add_student,
        name="add_student"
    ),

    # Edit Student
    path(
        "edit/<int:student_id>/",
        views.edit_student,
        name="edit_student"
    ),

    # Delete Student
    path(
        "delete/<int:student_id>/",
        views.delete_student,
        name="delete_student"
    ),

]