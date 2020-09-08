from django.contrib.auth.models import User, Group

from .models import profile

from django.db.models.signals import post_save
from django.dispatch import receiver


# @receiver(post_save, sender=User)
def Profile_signals(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='penulis')
        instance.groups.add(group)
        profile.objects.create(
            user=instance,
            name=instance.first_name+' '+instance.last_name,
        )
        print('successssss')

# parameter pertama receiver kedua sender
post_save.connect(Profile_signals, sender=User)

# @receiver(post_save, sender=User)
# def update_profile(sender, instace, created, **kwargs):
#     if created == False:
#         instance.profile.save()
#         print('Profile updated!')

#post_save.connect(update_profile, sender=User)
