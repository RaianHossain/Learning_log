from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect 

# Create your views here.

def register(request):
    if request.method != "POST":
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username = new_user.username, password = request.POST['password1'])
            login(request, authenticated_user)
            
            return redirect('index')
    
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)
