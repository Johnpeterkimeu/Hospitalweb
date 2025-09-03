from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Doctors


@receiver(post_save, sender=User)
def create_doctor_profile(sender, instance, created, **kwargs):
    if created and instance.is_staff:  # or use a custom flag like is_doctor
        Doctors.objects.create(user=instance, Name=instance.username)
        
@receiver(post_save, sender=Doctors)
def link_user_to_doctor(sender, instance, created, **kwargs):
    if created and not instance.user:
        try:
            # Try to find a user with the same email as the doctor
            matched_user = User.objects.get(email=instance.Email)
            instance.user = matched_user
            instance.save()
            print(f"Linked Doctor {instance.Name} to User {matched_user.username}")
        except User.DoesNotExist:
            print(f"No matching user found for doctor email {instance.Email}")


@receiver(post_save, sender=Doctors)
def create_user_for_doctor(sender, instance, created, **kwargs):
    if created and instance.user is None:
        # Create a Django User for this doctor
        user = User.objects.create_user(
            username=instance.email,
            email=instance.email,
            password=instance.password,   # ⚠️ plain text right now
            first_name=instance.name
        )
        instance.user = user
        instance.save()
