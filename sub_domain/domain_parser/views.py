from django.shortcuts import render

from .forms import DataForm


def base_view(request):
    form = DataForm()
    return render(request, 'base.html', context = {'form': form })


