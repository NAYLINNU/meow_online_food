from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile

#That is for create automaticually userprofile when is user created

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance,created, **kwargs):  #"created "is return True or False
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        # print('user profile is created')
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            #Create the user profile if not exit
            UserProfile.objects.create(user=instance)
            # print('Profile was not exit, but I create one')
        # print('User is Updated')
@receiver(pre_save,sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    pass
    # print(instance.username, 'This user is being saved!')
    
#post_save_connect(post_save_create_profile_receiver,sender=User)