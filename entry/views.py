from django.shortcuts import render,get_object_or_404
from django.views.generic import CreateView, ListView ,UpdateView , DetailView
from .models import BE,BE_line,Customers
from .forms import BEForm,LineBEForm,LineBEFormSet
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        be = self.get_object()  # Get the 'be' object for this view
        total_qty = sum(line.qty * line.width * line.length / 2_000_000 for line in be.be_lines.all())

        context['total_qty'] = total_qty
        return context


class BEUpdateView(UpdateView):
    model = BE
    form_class = BEForm
    template_name = 'entry/be_form.html'
    success_url = '/entry/list/'  # Redirigez ici après la mise à jour
    
class AddLinesBEView(CreateView):
    model = BE_line
    form_class = LineBEForm
    template_name = 'entry/be_add_lines.html'  # Créez ce template
      # Redirigez ici après l'ajout de lignes
    
    def get_initial(self):
        # Get the 'pk' from the URL
        pk = self.kwargs.get('pk')
        # Use get_object_or_404 to fetch the BE instance or return a 404 if it doesn't exist
        be = get_object_or_404(BE, pk=pk)
        # Return the initial data for the form
        return {'be': be}
    
    
    
    def form_valid(self, form):
        # Save the form and get the BE instance
        self.object = form.save()
        # Get the 'pk' of the related BE instance
        pk = self.object.be.pk
        # Use reverse_lazy to generate the 'be-details' URL with the 'pk' argument
        self.success_url = reverse_lazy('be-details', kwargs={'pk': pk})
        return super().form_valid(form)
    

    # def form_valid(self, form):
    #     be_id = self.kwargs.get('pk')  # Get the 'id' parameter from the URL
    #     be = BE.objects.get(pk=be_id)
    #     form.instance.be = be
    #     return super().form_valid(form)
    
    
def add_lines_be_view(request,pk):
    be = BE.objects.get(pk=pk)
    context={'be':be}
    return render(request,template_name='entry/try.html',context=context)