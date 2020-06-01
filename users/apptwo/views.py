from django.shortcuts import render
from apptwo.models import User
from apptwo.forms import NewUserForm


# Create your views here.


def index(request):
    return render(request, 'apptwo/index.html')


def users(request):
    form = NewUserForm()

    if request.method == 'POST':
        form = NewUserForm(request.POST)

        if form.is_valid():
            print("valid hu")
            form.save(commit=True)
            return render(request, 'apptwo/index.html')
        else:
            print("Error!!Form is invalid")
    return render(request, 'apptwo/userinfo.html', {'form':form})


    #previous Task

    #user_list = User.objects.order_by('FirstName')

    #user_dict = {'user': user_list}
    #return render(request, 'apptwo/userinfo.html', context=user_dict)
