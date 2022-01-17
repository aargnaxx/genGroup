from django.shortcuts import render
def test_vue(request):
    return render(request, 'vue_app/vue.html')