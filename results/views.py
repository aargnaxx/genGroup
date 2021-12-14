from django.shortcuts import render

# Create your views here.


def show_results(request):
    return render(request, "results/index.html", {})
