from django.shortcuts import render, redirect 
from django.contrib.auth import login, authenticate 
from . forms import SignUpForm

    
def signup(request): 
    form = SignUpForm(request.POST) 
    if form.is_valid(): 
        username = form.cleaned_data.get('username') 
        password = form.cleaned_data.get('password') 
        email = form.cleaned_data.get('email') 
        form.save() 
        user = authenticate(username=username, password=password) 
        login(request, user) 
        return redirect('/login')
    context = {     
        'form': form 
    } 
    return render(request, 'signup.html', context) 

def login_view(request):
    if request.method == 'POST':
        # Get the username and password from the POST request
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in and redirect to home page
            login(request, user)
            return redirect('/signup')
        else:
            # Return an error message if authentication fails
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        # Show the login form
        return render(request, 'login.html')
    
    
def logout(request):
    logout(request)
    return redirect('home')