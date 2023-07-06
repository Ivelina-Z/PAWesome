from django.shortcuts import render


def donate(request):
    return render(request, 'donate.html')


def add_foster_home(request):
    return render(request, 'foster-home.html')


def view_foster_homes(request):
    return render(request, 'foster-homes-details.html')


def how_to_help(request):
    return render(request, 'how-to-help.html')
