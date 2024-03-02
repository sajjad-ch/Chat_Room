from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from chat.serializers import MessageSerializer
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from .forms import UserprofileForm
from django.urls import reverse
from django.views import View
from django.http import HttpRequest
from .models import UserProfile, Messages
# Create your views here.

@method_decorator(login_required, name='dispatch')
class IndexView(View):
    def get(self, request: HttpRequest):
        email = request.user.email
        id = get_user_id(email)
        friends = get_friends_list(id)
        if friends is not None:
            return render(request, 'chat/index.html', context={'friends': friends})
        else:
            return render(request, 'chat/index.html', context={'message': "You don't have any friends like me so this app is not for you."})

class HomeView(View):
    def get(self, request: HttpRequest):
        return render(request, 'chat/home.html', context={})

@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    def get(self, request: HttpRequest):
        user_profile = request.user.userprofile
        user_profile_form = UserprofileForm(instance=user_profile)
        context = {
            'user_profile_form' : user_profile_form
        }
        return render(request, 'chat/profile.html', context)

    def post(self, request: HttpRequest):
        user_profile = request.user.userprofile
        user_profile_form = UserprofileForm(request.POST, instance=user_profile)
        if user_profile_form.is_valid():
            new_email = user_profile_form.cleaned_data['email']
            if new_email != request.user.email:
                user_profile_form.add_error('email', "Don't change your email, You may never get your account back!")
                return redirect(reverse('profile'))
            user_profile.name = user_profile_form.cleaned_data['name']
            user_profile.username = user_profile_form.cleaned_data['username']
            user_profile.save()

            user = request.user
            user.first_name = user_profile_form.cleaned_data['name']
            user.username = user_profile_form.cleaned_data['username']
            user.save()
            return redirect(reverse('profile'))  # Adjust the URL name as needed
        context = {
            'user_profile_form': user_profile_form
        }
        return render(request, 'chat/profile.html', context)


def get_friends_list(id):
    try:
        user = UserProfile.objects.get(id=id)
        ids = list(user.friends_set.all())
        friends = []
        for id in ids:
            num = str(id)
            fr = UserProfile.objects.get(id=int(num))
            friends.append(fr)
            return friends
    except:
        return []

def get_user_id(email):
    use = UserProfile.objects.get(email__iexact=email)
    id = use.id
    return id


def search_friend(request: HttpRequest):
    users = list(UserProfile.objects.all())
    for user in users:
        if user.username == request.user.username:
            users.remove(user)
            break

    if request.method == "POST":
        print("SEARCHING...!!!")
        query = request.POST.get(key="search")
        user_list = []
        for user in users:
            if query in user.username or query in user.email:
                user_list.append(user)
            return render(request, 'chat/search.html', {'users': user_list})
    try:
        users = users[:10]
    except:
        users = users[:]

    id = get_user_id(request.user.email)
    friends = get_friends_list(id)
    return render(request, 'chat/search.html', {'users': users, 'friends': friends})


def add_friend(request: HttpRequest, username):
    email = request.user.email
    id = get_user_id(email)
    friend = UserProfile.objects.get(username=username)
    current_user = UserProfile.objects.get(id=id)
    print(current_user.name)
    user_friends_list = current_user.friends_set.all()
    flag = 0
    for username in user_friends_list:
        if username.friend == friend.id:
            flag = 1
            break
    if flag ==0:
        print("Friend Added...!!")
        current_user.friends_set.create(friend=friend.id)
        friend.friends_set.create(friend=id)
    return redirect("/chat/search")

def chat(request: HttpRequest, username):
    friend = UserProfile.objects.get(username=username)
    id = get_user_id(request.user.email)
    current_user = UserProfile.objects.get(id=id)
    message = Messages.objects.filter(sender_name=id, receiver_name=friend.id) | Messages.objects.filter(sender_name=friend.id, receiver_name=id)

    if request.method == "GET":
        friends = get_friends_list(id)
        context = {
            'messages': message,
            'friends': friends,
            'curr_user' : current_user,
            'friend': friends
        }
        return render(request, "chat/messages.html", context=context)


@csrf_exempt
def message_list(request: HttpRequest, sender=None, receiver=None):
    if request.method == 'GET':
        messages = Messages.objects.filter(sender_name=sender, receiver_name=receiver, seen=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.seen = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)