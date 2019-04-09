from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm 
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# start new part added for test purpose
# ####################################
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
# ####################################
# end new part added for test purpose

def register(request): 
    if ( request.method ==  'POST' ): 
        form = UserRegisterForm(request.POST)
        if (form.is_valid()):
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('blog-home')
        else:
            print('not valid')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if( request.method == 'POST' ):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if( u_form.is_valid() and p_form.is_valid() ):
            u_form.save()
            p_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f'Your account has been updated {username}!')
            return redirect('profile')
        else:
            print('not valid')
    else: 
        u_form = UserUpdateForm(instance=request.user)   
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form 
    }       
    return render(request, 'users/profile.html', context)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login_api(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
    elif username:
        print(username)
        print(Token.objects.get(user=User.objects.get(username=username)))
        token = Token.objects.get(user=User.objects.get(username=username))
    return Response({'token': token.key},
                    status=HTTP_200_OK)


