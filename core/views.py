from django.shortcuts import render, redirect

# Create your views here.
def landing(request):
    if request.user.is_authenticated:
        return redirect('schedule:index')
    return render(request, 'core/landing.html')