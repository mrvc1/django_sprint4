from django.shortcuts import render
from django.views.generic import TemplateView


class AboutPage(TemplateView):
    template_name = 'pages/about.html'


class RulesPage(TemplateView):
    template_name = 'pages/rules.html'


def error_handler_403(request, exception):
    return render(request, 'pages/403csrf.html', status=403)


def error_handler_404(request, exception):
    return render(request, 'pages/404.html', status=404)


def error_handler_500(request):
    return render(request, 'pages/500.html', status=500)
