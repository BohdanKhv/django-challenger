from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from taggit.managers import TaggableManager


# Users Profile DB
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    about = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=15, default='', blank=True)
    profile_photo = models.ImageField(default='default-ava.jpg')
    gold = models.IntegerField(blank=True, default=0)
    follows = models.ManyToManyField('self', related_name='follow', symmetrical=False, blank=True)
    user_followers = models.ManyToManyField('self', related_name='followers', symmetrical=False, blank=True)
    up_vote = models.ManyToManyField('Challenges', related_name='up_vote', blank=True)
    down_vote = models.ManyToManyField('Challenges', related_name='down_vote', blank=True)
    donated = models.ManyToManyField('Challenges', related_name='donated', blank=True)

    def __str__(self):
        return '%s - %s  - %s ' % (self.user.email, self.user, self.gold)

    class Meta:
        verbose_name_plural = 'Users Profile'


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


# Users challenges DB
class Challenges(models.Model):
    user = models.ForeignKey(User, related_name='user_challenge', on_delete=models.CASCADE, blank=True, default=None)
    about = models.TextField(max_length=500, blank=False)
    price_goal = models.IntegerField(blank=False)
    price_reached = models.IntegerField(blank=True, default=0)
    tags = TaggableManager(blank=True)
    published = models.DateTimeField(default=timezone.now, blank=True)
    proof_img = models.ImageField(blank=False, default='default.png')
    proof_video = models.FileField(upload_to='', null=True, blank=True, verbose_name="")
    donator = models.ManyToManyField(User, related_name='donator', blank=True)
    donator_approved = models.ManyToManyField(User, related_name='donator_approved', blank=True)
    status = models.CharField(max_length=20, blank=False, default='Active')

    def __str__(self):
        return '%s - %s ' % (self.pk, self.user)

    class Meta:
        verbose_name_plural = 'Challenges'
        ordering = ['-published']


class DonatedAmount(models.Model):
    user = models.ForeignKey(User, related_name='amount_user', on_delete=models.CASCADE, default=None)
    challenge = models.ForeignKey(Challenges, related_name='amount_challenge', on_delete=models.CASCADE, default=None)
    amount = models.IntegerField()

    def __str__(self):
        return '%s - %s - %s ' % (self.pk, self.user, self.amount)

    class Meta:
        verbose_name_plural = 'Donated Amount Transaction'


class ChallengesComments(models.Model):
    user = models.ForeignKey(User, related_name='comment_user', on_delete=models.CASCADE, default=None)
    challenge = models.ForeignKey(Challenges, related_name='comment_challenge', on_delete=models.CASCADE, default=None)
    comment = models.TextField(max_length=500, blank=False)
    published = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return '%s - %s ' % (self.user, self.challenge)

    class Meta:
        verbose_name_plural = 'Challenges Comments'
        ordering = ['published']
