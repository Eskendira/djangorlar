from django.db.models(
    EmailField,
    CharField,
    BooleanField
    )

from django.contrib.auth.models import AbstractBaseUser,PermissionMixin


from apps.abstracts.models import AbstractSoftDeleteModel
from apps.auths.validators import validate_email_domain

class CustomerUser(AbstractBaseUser,PermissionMixin,AbstractSoftDeleteModel):
    EMAIL_MAX_LENGTH = 255
    USERNAME_MAX_LENGTH = 150
    PASSWORD_MAX_LENGTH = 128
    email = EmailField(
        unique=True,
        max_length=EMAIL_MAX_LENGTH,
        validators=[validate_email_domain],
        verbose_name="Email Address",
        help_text ="Enter a valid email address."
    )

    username = CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        verbose_name="Username",
        help_text="Enter a unique username."    
    )    

    is_active = BooleanField(
        default=True,
        verbose_name="Active Status",
        help_text="Designates whether this user should be treated as active."
    )

    password = CharField(
        max_length=PASSWORD_MAX_LENGTH,
        verbose_name="Password",
        help_text="Enter a secure password."
    )

    is_staff = BooleanField(
        default=False,
        verbose_name="Staff Status",
        help_text="Designates whether the user can log into this admin site."
    )

    def __str__(self):
        return self.email

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']
