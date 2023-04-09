from django.shortcuts import render
from .parsecomm import get_data_with_selenium



def index(request):
    if request.method == 'GET':
        return render(request, 'index.html', {'user': request.user})
    if request.method == 'POST':
        commsnow = get_data_with_selenium(request.POST.get('text'))
        data = {}
        for i, comm in enumerate(commsnow):
            data[i] = {
                'content': comm[0],
                'author': comm[1],
                'date' : comm[2],
                'stars' : comm[3]
            }
        if commsnow != False:
            return render(request, 'index.html', {'user': request.user, 'comments': data})
