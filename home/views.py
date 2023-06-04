from django.shortcuts import render

def home_page(request):
    return render(request, 'home/index.html')
def team_page(request):
    return render(request, 'home/team.html')
def contact_page(request):
    return render(request, 'home/contact.html')
