from django.contrib import admin
from .models import UserProfile, Challenges, DonatedAmount, ChallengesComments

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Challenges)
admin.site.register(DonatedAmount)
admin.site.register(ChallengesComments)
