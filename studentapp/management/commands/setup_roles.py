from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Create and configure Admin, Teacher, and Staff roles"

    def handle(self, *args, **options):

        # Create groups
        admin_group, _ = Group.objects.get_or_create(
            name="Admin"
        )

        teacher_group, _ = Group.objects.get_or_create(
            name="Teacher"
        )

        staff_group, _ = Group.objects.get_or_create(
            name="Staff"
        )

        # Student permissions
        student_permissions = Permission.objects.filter(
            content_type__app_label="studentapp",
            content_type__model="student",
        )

        # Get individual permissions
        view_student = student_permissions.filter(
            codename="view_student"
        ).first()

        add_student = student_permissions.filter(
            codename="add_student"
        ).first()

        change_student = student_permissions.filter(
            codename="change_student"
        ).first()

        delete_student = student_permissions.filter(
            codename="delete_student"
        ).first()

        # ==========================
        # ADMIN
        # ==========================

        admin_group.permissions.set(
            [
                permission
                for permission in [
                    view_student,
                    add_student,
                    change_student,
                    delete_student,
                ]
                if permission
            ]
        )

        # ==========================
        # TEACHER
        # ==========================

        teacher_group.permissions.set(
            [
                permission
                for permission in [
                    view_student,
                    add_student,
                    change_student,
                ]
                if permission
            ]
        )

        # ==========================
        # STAFF
        # ==========================

        staff_group.permissions.set(
            [
                permission
                for permission in [
                    view_student,
                ]
                if permission
            ]
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Roles and permissions configured successfully."
            )
        )