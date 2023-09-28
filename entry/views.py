from django.shortcuts import render
from django.views.generic import CreateView, ListView ,UpdateView , DetailView
from .models import BE,BE_line
from .forms import BEForm,LineBEFormSet
from django.urls import reverse_lazy

class BECreateView(CreateView):
    model = BE
    form_class = BEForm
    template_name = 'entry/be_form.html'
    success_url = reverse_lazy('be-list')  # Redirect URL after successful form submission
    
class BEListView(ListView):
    model = BE
    template_name = 'entry/be_list.html'
    context_object_name = 'bes'
    
class BEDetailsView(DetailView):
    model = BE
    template_name = 'entry/be_details.html'
    context_object_name = 'be'


class BEUpdateView(UpdateView):
    model = BE
    form_class = BEForm
    template_name = 'entry/be_form.html'
    success_url = '/entry/list/'  # Redirigez ici après la mise à jour

class AddLinesBEView(CreateView):
    model = BE_line
    form_class = LineBEFormSet
    template_name = 'entry/be_add_lines.html'  # Créez ce template
    success_url = reverse_lazy('be-list')  # Redirigez ici après l'ajout de lignes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['be'] = BE.objects.get(pk=self.kwargs['pk'])
        return context
