from django.shortcuts import render
from.models import book, Author, BookInstance, ganre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

def index(request): # ф-ия отображения доммашней страницы веб сайта
    # отображение количество некоторых главных объектов
    num_books = book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # отображение доступных книг
    num_instances_available = BookInstance.objects.filter(status__exact = 'a').count()
    num_authors = Author.objects.count() #МЕТОД all применен по умолчанию (почему в num_book не так не понятно)
    num_ganre = ganre.objects.count()
    num_booktitle = book.objects.filter(title__contains = 'qwerty').count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # далее следут отрисовка html шаблона   index.html с данными внутри
    return render (
        request,
        'index.html',
        context =  {'num_books':num_books,
                    'num_instances':num_instances,
                    'num_instances_available':num_instances_available,
                    'num_authors':num_authors,
                    'num_ganre':num_ganre,
                    'num_booktitle':num_booktitle,
                    'num_visits':num_visits},



    )
class BookListView(generic.ListView):
    model = book

class BookDetailView(generic.DetailView):
    model = book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author

class OdolzhenieKnigiUsera(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    def get_queryset(self):
        return BookInstance.objects.filter(borrower = self.request.user).filter(status__exact = 'o')


from django.contrib.auth.mixins import PermissionRequiredMixin

class AllKnigiForStaff(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import permission_required
from .forms import FormaZaemaKnigi

@permission_required('catalog.can_mark_returned')
def renew_form(request,pk):
    book_inst = get_object_or_404(BookInstance,pk=pk)
    #Создаем условия для типа запросов(GET или POST)
    if request.method == 'POST':
        #создаем экзмепляр этой формы и заполняем данными исходя из запроса(связывание)
        form = FormaZaemaKnigi(request.POST)
        #создаем условия проверки формы(валидность)
        if form.is_valid():
            #заполняем форму если условие верно
            book_inst.due_back = form.cleaned_data['data_zaema']
            book_inst.save()
            #выполняем переход в этой форме
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        #если запрос типа GET то создается форма по умолчанию заполненная начальными данными для конкретного поля в данном случае поля(data_zaema)
        data_prodlenia = datetime.date.today() + datetime.timedelta(weeks=3) #начальное значение
        form = FormaZaemaKnigi(initial={'data_zaema':data_prodlenia,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author
from .models import book

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death':'12/12/12',}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_death','date_of_birth']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(CreateView):
    model = book
    fields = '__all__'

class BookUpdate(UpdateView):
    model = book
    fields = ['title','author','genre']

class BookDelete(DeleteView):
    model=book
    success_url = reverse_lazy('books')
    template_name_suffix = '_delete'







# Create your views here.
