from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    profilepic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_validated = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_limit_reached = models.BooleanField(default=False)
    user_limit = models.IntegerField(default=5)
    current_prompt_count = models.IntegerField(default=0)
    is_prompt_disabled = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def increase_prompt_count(self):
        """Increase the current prompt count and disable prompting if limit is reached."""
        if self.current_prompt_count < self.user_limit:
            self.current_prompt_count += 1
            if self.current_prompt_count >= self.user_limit:
                self.is_prompt_disabled = True
            self.save()

    def reset_prompt_count(self):
        """Reset the current prompt count and enable prompting."""
        self.current_prompt_count = 0
        self.is_prompt_disabled = False
        self.save()


class AIThread(models.Model):
    THREAD_OBJECT_CHOICES = [
        ('thread', 'Thread'),
        ('thread.deleted', 'Deleted Thread'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ai_threads')
    thread_id = models.CharField(max_length=255, unique=True)
    object_type = models.CharField(max_length=50, choices=THREAD_OBJECT_CHOICES, default='thread')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    metadata = models.JSONField(default=dict, blank=True)
    tool_resources = models.JSONField(default=dict, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'Thread {self.thread_id} for {self.user.email}'

    def mark_as_deleted(self):
        self.is_deleted = True
        self.object_type = 'thread.deleted'
        self.save()

    class Meta:
        ordering = ['-created_at']  # Order by most recent by default
