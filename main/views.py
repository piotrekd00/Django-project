from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render

from .forms import RentForm
from .models import RentalOffice, Book, Film, CD, Rented, Item
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Create your views here.


class OfficeBaseView(View):
    model = RentalOffice
    fields = '__all__'
    success_url = reverse_lazy('rentaloffice:all')


class RentedBaseView(View):
    model = Rented
    success_url = reverse_lazy('rentaloffice:all')


class RentedCreateView(RentedBaseView, CreateView):
    form_class = RentForm

    def form_valid(self, form):
        obj = form.save(commit=False)

        obj.customer = User.objects.get(pk=self.request.user.id)
        obj.item = Item.objects.get(pk=self.kwargs['item_id'])
        obj.save()

        old_obj = Item.objects.get(pk=self.kwargs['item_id'])
        old_obj.stock -= 1
        old_obj.save()

        print(obj.item, obj.customer)
        return super().form_valid(form)


class UserRent(RentedBaseView, ListView):

    def get_queryset(self):
        return Rented.objects.filter(customer=self.request.user.id)


class RentedDeleteView(RentedBaseView, DeleteView):
    pass


class ScoreboardListView(ListView):
    template_name = 'main/scoreboard_list.html'
    context_object_name = 'scoreboard'

    def get_queryset(self):
        return User.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ScoreboardListView, self).get_context_data(**kwargs)
        context['order'] = User.objects.annotate(order_count=Count('rented')).order_by('-order_count')
        return context


class StatsView(ListView):
    template_name = 'main/stats.html'
    context_object_name = 'stats'

    def get_queryset(self):
        return Item.objects.all()

    def get_context_data(self, **kwargs):
        context = super(StatsView, self).get_context_data(**kwargs)
        context['books'] = Book.objects.values('genre').annotate(score=Count('rented')).order_by('genre')
        context['cds'] = CD.objects.values('genre').annotate(score=Count('rented')).order_by('genre')
        context['films'] = Film.objects.values('genre').annotate(score=Count('rented')).order_by('genre')
        print(context['books'], context['cds'], context['films'])
        return context


class OfficeListView(OfficeBaseView, ListView):
    pass


class OfficeDetailView(OfficeBaseView, DetailView):
    pass


class OfficeCreateView(OfficeBaseView, CreateView):
    pass


class BookBaseView(OfficeBaseView):
    model = Book


class BookDetailView(BookBaseView, DetailView):
    pass


class BookCreateView(BookBaseView, CreateView):
    pass


class BookUpdateView(BookBaseView, UpdateView):
    pass


class BookDeleteView(BookBaseView, DeleteView):
    pass


class FilmBaseView(OfficeBaseView):
    model = Film


class FilmDetailView(FilmBaseView, DetailView):
    pass


class FilmCreateView(FilmBaseView, CreateView):
    pass


class FilmUpdateView(FilmBaseView, UpdateView):
    pass


class FilmDeleteView(FilmBaseView, DeleteView):
    pass


class CDBaseView(OfficeBaseView):
    model = CD


class CDDetailView(CDBaseView, DetailView):
    pass


class CDCreateView(CDBaseView, CreateView):
    pass


class CDUpdateView(CDBaseView, UpdateView):
    pass


class CDDeleteView(CDBaseView, DeleteView):
    pass


