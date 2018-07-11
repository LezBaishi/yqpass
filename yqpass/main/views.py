from django.shortcuts import render
import json
from users.models import User

# Create your views here.
def index(request):
    # return render(request, 'main/base.html')
    return render(request, 'main/home.html')

def test(request):
    return render(request, 'main/test/validation.html')

def accounts_profile(request):
    if request.method == 'POST':
        a = json.loads(request.body)
        # print(a)
        b = User.objects.get(email=request.user.email)
        b.name = a['name']
        b.sex = a['sex']
        b.birthday = a['birthday']
        b.phone = a['phone']
        b.company = a['company']
        b.department = a['department']
        b.team_belong = a['team_belong']
        b.job_number = a['job_number']
        b.save()
    return render(request, 'main/accounts_profile.html')

def accounts_change(request):
    if request.method == 'POST':
        a = json.loads(request.body)
        # print(a)
        b = User.objects.get(email=request.user.email)
        b.name = a['name']
        b.sex = a['sex']
        b.birthday = a['birthday']
        b.phone = a['phone']
        b.company = a['company']
        b.department = a['department']
        b.team_belong = a['team_belong']
        b.job_number = a['job_number']
        b.save()
    return render(request, 'main/accounts_change.html')