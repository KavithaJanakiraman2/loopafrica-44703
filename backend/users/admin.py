from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from .models import Doctor, Instructor, Feedback
from users.forms import UserChangeForm, UserCreationForm
from django.template.loader import render_to_string
from django.conf import settings
from modules.two_factor_authentication.twofactorauth.utils import Util
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html



User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'address', 'qualification', 'last_updated_date', 'last_updated_by', 'password_change_link')

    def save_model(self, request, obj, form, change):
        # Save the Doctor instance
        super().save_model(request, obj, form, change)

        # Check if this is a new doctor being added
        if not change:
            # Send email to the new doctor for password change
            subject = "Welcome to LoopHealth"
            email_template = 'email/password_change.txt'
            password_change_url = self.get_password_change_url(obj)
            context = {'doctor': obj, 'password_change_url': password_change_url}
            message = render_to_string(email_template, context)
            to_email = obj.user.email
            # print("Sending email to: ", to_email)
            # Send the email using Util class
            # Util.send_email({'subject': subject, 'body': message, 'to_email': to_email})
            print("Doctor mail:", to_email)  # Debugging statement to check the email address
            if to_email:
                print("Sending email to:", to_email)
                # Send the email using Util class
                Util.send_email({'subject': subject, 'body': message, 'to_email': to_email})
            else:
                print("No email address found for the doctor.")
    
    def get_password_change_url(self, obj):
        uid = urlsafe_base64_encode(force_bytes(obj.user.pk))
        token = default_token_generator.make_token(obj.user)
        return reverse('users:changepassword', kwargs={'uidb64': uid, 'token': token})

    def password_change_link(self, obj):
        change_password_url = self.get_password_change_url(obj)
        # return f'<a href="{change_password_url}">Change Password</a>'
        return format_html('<a href="{}">Change Password</a>', change_password_url)

    # password_change_link.allow_tags = True
    # password_change_link.short_description = 'Change Password Link'


class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'address', 'qualification', 'last_updated_date', 'last_updated_by')

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Feedback)