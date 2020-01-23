from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.views.generic.edit import FormView
from .forms import LogInForm, RegisterForm, CreateChallengeForm, ChallengeCommentForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, Challenges, DonatedAmount, ChallengesComments
from .forms import UserEditForm, UserProfileEditForm, UploadProofFile
from django.core import serializers


class IndexView(View):
    def get(self, request):
        return render(request, 'main/index.html')


class UserProfile(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user_pk'
    template_name = 'main/user-profile.html'
    login_url = "/account/login/"
    redirect_field_name = '/'


    def get_queryset(self):
        queryset = User.objects.filter(pk=self.kwargs['pk'])
        return queryset


# User registration and log in system
class Register(CreateView):
    form_class = RegisterForm
    template_name = 'account/register.html'
    success_url = 'main/user-profile.html'

    def form_valid(self, form):
        request = self.request
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password2')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"New {username} Account Created!")
            messages.info(request, f"{username} successfully logged in!")
            return redirect('main/user-profile.html')


class LogIn(FormView):
    form_class = LogInForm
    template_name = 'account/login.html'
    success_url = '/'

    def form_valid(self, form):
        request = self.request
        username = form.cleaned_data.get('username')
        user = form.login(request)
        if user is not None:
            login(request, user)
            messages.success(request, f"{username} successfully logged in!")
            return redirect('/')


class LogOut(View):
    def get(self, request):
        logout(request)
        messages.info(request, f"Logged out!")
        return redirect("/")


# Views that includes Challenges
class ChallengeCreate(LoginRequiredMixin, CreateView):
    template_name = 'challenge/challenge-create.html'  # Replace with your template.
    form_class = CreateChallengeForm
    success_url = reverse_lazy('main')  # Replace with your URL or reverse().
    login_url = "/account/login/"
    redirect_field_name = '/'

    def get_initial(self):
        initial = super(ChallengeCreate, self).get_initial()
        return initial

    def form_valid(self, form):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        post_form = form.save(commit=False)
        post_form.user = self.request.user
        post_form.save()
        form.save_m2m()

        messages.success(self.request, f'Challenge was successfully posted!')
        return redirect('/user-profile/'+str(self.request.user.pk))


class ChallengeDelete(LoginRequiredMixin, DeleteView):
    model = Challenges
    template_name = 'challenge/challenge-confirm-delete.html'
    login_url = "/account/login/"
    redirect_field_name = '/'

    def get_success_url(self):
        messages.success(self.request, f"Post #{self.kwargs.get('pk')} was deleted!")
        return redirect('/user-profile/'+str(self.request.user.pk))

    def get(self, request, *args, **kwargs):
        pk_ = self.kwargs.get('pk')
        challenge = get_object_or_404(Challenges, pk=pk_)
        if challenge.user.pk != self.request.user.pk:
            return redirect('/user-profile/'+str(self.request.user.pk))

        return render(request,
                      self.template_name,
                      {
                          'object': get_object_or_404(Challenges, pk=pk_)
                      })


class ChallengeView(UpdateView):
    model = Challenges
    form_class = UploadProofFile
    template_name = 'challenge/challenge-view.html'

    def get_queryset(self):
        queryset = Challenges.objects.filter(pk=self.kwargs['pk'])
        return queryset

# ----------------------------------- TESTING -------------------------------------------------
#     THIS SH*T IS F*CKING WORKS!! (o.O) (O.O) (o.O) UP/DOWN VOTES SYSTEM

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = get_object_or_404(Challenges, pk=self.kwargs['pk'])

        amount_transaction_upvotes = 0
        amount_transaction_downvotes = 0
        percent_donated_current_user = 0

        for challeng in queryset.amount_challenge.all():
            if challeng.challenge in challeng.user.user_profile.down_vote.all():
                amount_transaction_downvotes += challeng.amount
        amount_transaction_downvotes = amount_transaction_downvotes / queryset.price_goal * 100

        for challeng in queryset.amount_challenge.all():
            if challeng.challenge in challeng.user.user_profile.up_vote.all():
                amount_transaction_upvotes += challeng.amount
        amount_transaction_upvotes = amount_transaction_upvotes / queryset.price_goal * 100

        for challeng in queryset.amount_challenge.all():
            if self.request.user == challeng.user:
                percent_donated_current_user += challeng.amount
        percent_donated_current_user = percent_donated_current_user / queryset.price_goal * 100

        context['you_donated_percent'] = percent_donated_current_user
        context['upvoters_donated_percent'] = amount_transaction_upvotes
        context['downvoters_donated_percent'] = amount_transaction_downvotes
        context['challenge_comment_form'] = ChallengeCommentForm
        return context

# -------------------------------- TESTING -------------------------------------------------

    def form_valid(self, form, **kwargs):
        form = form.save(commit=False)
        form.save()
        messages.success(self.request, f'Successfully uploaded.')
        return redirect('/challenge/' + str(self.kwargs['pk']))

    def form_invalid(self, form, **kwargs):
        messages.error(self.request, f'Error to upload!')
        return redirect('/challenge/' + str(self.kwargs['pk']))


class FeedView(LoginRequiredMixin, ListView):
    model = Challenges
    template_name = 'main/feed.html'
    context_object_name = 'challenges'
    login_url = "/account/login/"
    redirect_field_name = '/'


class UserChallengeUpVoteToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        challenge_pk = self.kwargs.get('pk')
        obj = get_object_or_404(Challenges, pk=challenge_pk)

        user = self.request.user
        amount_transaction_upvotes = 0

        # Toggles obj(challenge) with given PK to current authenticated User up_votes
        if user in obj.donator.all():
            if obj in user.user_profile.up_vote.all():
                user.user_profile.up_vote.remove(obj)
                obj.donator_approved.remove(user)
            else:
                # add to user up vote
                user.user_profile.up_vote.add(obj)
                obj.donator_approved.add(user)
                # if user has down vote then remove it
                if obj in user.user_profile.down_vote.all():
                    user.user_profile.down_vote.remove(obj)
                # And Check here if donaters > 75 of all donaters_approved if they are then change the status to success or failed
                for challeng in obj.amount_challenge.all():
                    if challeng.challenge in challeng.user.user_profile.up_vote.all():
                        amount_transaction_upvotes += challeng.amount
                amount_transaction_upvotes = amount_transaction_upvotes / obj.price_goal * 100
                if amount_transaction_upvotes >= 75:
                    # Give gold to user who made the challenge
                    obj.user.user_profile.gold += obj.price_goal
                    obj.user.user_profile.save()
                    obj.status = 'Success'
                    obj.save()

        return reverse('challenge_view', kwargs={'pk': challenge_pk})


class UserChallengeDownVoteToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        challenge_pk = self.kwargs.get('pk')
        obj = get_object_or_404(Challenges, pk=challenge_pk)

        user = self.request.user
        amount_transaction_downvotes = 0

        # Toggles obj(challenge) with given PK to current authenticated User -> user_profile -> down_vote
        if user in obj.donator.all():
            if obj in user.user_profile.down_vote.all():
                user.user_profile.down_vote.remove(obj)
                obj.donator_approved.remove(user)
            else:
                user.user_profile.down_vote.add(obj)
                obj.donator_approved.add(user)
                if obj in user.user_profile.up_vote.all():
                    user.user_profile.up_vote.remove(obj)

                # And Check here if donaters > 75 of all donaters_approved if they are then change the status to success or failed
                for challeng in obj.amount_challenge.all():
                    if challeng.challenge in challeng.user.user_profile.down_vote.all():
                        amount_transaction_downvotes += challeng.amount
                amount_transaction_downvotes = amount_transaction_downvotes / obj.price_goal * 100
                if amount_transaction_downvotes >= 75:
                    obj.status = 'Failed'
                    obj.save()
                    for challeng in obj.amount_challenge.all():
                        challeng.user.user_profile.gold += challeng.amount
                        challeng.user.user_profile.save()

        return reverse('challenge_view', kwargs={'pk': challenge_pk})


class UserChallengeDonate(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        challenge_pk = self.kwargs.get('pk')
        obj = get_object_or_404(Challenges, pk=challenge_pk)
        amount = 0

        user = self.request.user

        # Check if the value fixed or other value
        if 'donation-value' in self.request.POST:
            amount = int(self.request.POST['donation-value'])
        elif self.request.POST['other-value'] != "":
            amount = int(self.request.POST['other-value'])
        if obj.price_goal - obj.price_reached <= amount:
            amount = obj.price_goal - obj.price_reached
            messages.info(self.request, f'The challenges found goal was reached!')

        # Charge and add user to donators
        if amount > 0:
            if user.user_profile.gold >= amount:
                obj.price_reached = obj.price_reached + amount
                user.user_profile.gold = user.user_profile.gold - amount
                obj.donator.add(user)
                user.user_profile.donated.add(obj)
                # Change the status of the challenge
                if obj.price_goal == obj.price_reached:
                    obj.status = "Waiting";

                # Save Data
                # create new transaction
                transactin = DonatedAmount(user=self.request.user, challenge=obj, amount=amount)

                transactin.save()
                user.user_profile.save()
                obj.save()
                messages.success(self.request, f'You\'ve donated {amount} gold.')
            else:
                messages.error(self.request, f'Not enough gold.')
        else:
            messages.error(self.request, f'Donation can\'t be $0')
        return reverse('user_profile', kwargs={'pk': obj.user.pk})


# ------------------------ COMMENTS ---------------------------------------------


class ChallengeComment(CreateView):
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Challenges, pk=self.kwargs.get('pk'))
        user = self.request.user
        comment = self.request.POST['comment']
        comment = ChallengesComments(user=user, challenge=obj, comment=comment)
        comment.save()

        commentJson = ChallengesComments.objects.filter(pk=comment.pk)
        data = serializers.serialize("json", commentJson)
        return HttpResponse(data, content_type='application/json')


class ChallengeCommentDelete(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        message_pk = self.kwargs.get('pk')
        obj = get_object_or_404(ChallengesComments, pk=message_pk)

        user = self.request.user

        # Toggles obj(user) with given PK to current authenticated User followers
        if obj.user.pk == user.pk:
            obj.delete()

        return reverse('challenge_view', kwargs={'pk': obj.challenge.pk})


# ------------------------ END COMMENTS ---------------------------------------------


class TagChallengeSearch(ListView):
    model = Challenges
    template_name = 'challenge/challenge-search.html'
    context_object_name = 'challenges'

    def get_queryset(self):
        challenges_list = Challenges.objects.all()
        tag = self.request.GET.get("tag")

        if tag:
            challenges_list = Challenges.objects.filter(tags__name__in=[tag])
        return challenges_list


# ----------------- END CHALLENGES VIEWS ---------------------------------


class UserFollowToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user_pk = self.kwargs.get('pk')
        obj = get_object_or_404(User, pk=user_pk)

        user = self.request.user

        # Toggles obj(user) with given PK to current authenticated User followers
        if obj.user_profile in user.user_profile.follows.all():
            user.user_profile.follows.remove(obj.user_profile)
            obj.user_profile.user_followers.remove(user.user_profile)
        else:
            user.user_profile.follows.add(obj.user_profile)
            obj.user_profile.user_followers.add(user.user_profile)

        return reverse('user_profile', kwargs={'pk': user_pk})


class UserFollows(ListView):
    context_object_name = 'user_pk'
    template_name = 'main/user-follow.html'

    def get_queryset(self):
        queryset = get_object_or_404(User, pk=self.kwargs['pk'])
        return queryset


class UserFollowers(DetailView):
    model = User
    context_object_name = 'user_pk'
    template_name = 'main/user-followers.html'

    def get_queryset(self):
        queryset = User.objects.filter(pk=self.kwargs['pk'])
        return queryset


class UserSearch(ListView):
    model = User
    template_name = 'main/search.html'
    context_object_name = 'user_pk'

    def get_queryset(self):
        if self.request.user:
            user_list = User.objects.all()

        query = self.request.GET.get("search")
        if query:
            user_list = self.model.objects.filter(username__icontains=query)
        return user_list


# User info edit class based view way
class EditProfile(UpdateView):
    model = User
    template_name = 'account/edit-profile.html'
    form_class = UserEditForm

    def get_context_data(self, **kwargs):
        context = super(EditProfile, self).get_context_data(**kwargs)
        context['user_form'] = UserEditForm(instance=self.request.user)
        context['profile_form'] = UserProfileEditForm(instance=self.request.user.user_profile)
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(data=self.request.POST or None, instance=self.request.user)
        profile_form = UserProfileEditForm(data=self.request.POST or None, instance=self.request.user.user_profile,
                                           files=self.request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form = user_form.save(commit=False)
            profile_form = profile_form.save(commit=False)
            user_form.save()
            profile_form.save()
            messages.success(self.request, f'{self.request.user.username}\'s profile successfully updated.')
            return redirect('/user-profile/'+str(self.request.user.pk))
        else:
            messages.error(self.request, f'Error!')
            return redirect('/user-profile/'+str(self.request.user.pk))


# ----------------- END USER VIEWS ---------------------------------



# # User info edit method way
# @login_required
# def edit_profile(request):
#     if request.method == 'POST':
#         user_form = UserEditForm(data=request.POST or None, instance=request.user)
#         profile_form = UserProfileEditForm(data=request.POST or None, instance=request.user.user_profile, files=request.FILES)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#     else:
#         user_form = UserEditForm(instance=request.user)
#         profile_form = UserProfileEditForm(instance=request.user.user_profile)
#
#     context = {
#         'user_form': user_form,
#         'profile_form': profile_form,
#     }
#     return render(request, 'account/edit-profile.html', context)
