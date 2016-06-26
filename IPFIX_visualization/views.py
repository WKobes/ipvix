from django.shortcuts import render, get_object_or_404
from .models import *


def index(request):
    type2visuals = TypeToVisualization.objects.all()
    return render(request, 'IPFIX_visualization/showall.html', {'type2visuals': type2visuals})


def zoominont2v(request, t2vid):
    t2v = get_object_or_404(TypeToVisualization, pk=t2vid)
    if hasattr(TypeToVisualization, t2v.visual.function):
        to_execute = getattr(TypeToVisualization, t2v.visual.function)

        data = to_execute(t2v.filename)
    else:
        data = None
    return render(request, 'IPFIX_visualization/zoomint2v.html',
                  {'t2v': t2v, 'data': data, })
