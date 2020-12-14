from django.urls import path
from .import views



urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>',views.AuthorDetailView.as_view(), name='author-detail'),
]


urlpatterns += [
    path('mybooks/', views.OdolzhenieKnigiUsera.as_view(), name='my-borrowed'),
    path(r'borrowed/', views.AllKnigiForStaff.as_view(), name='all-borrowed'),  # Added for challenge
]

urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_form, name='renew-form')
]

urlpatterns += [
    path(r'author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path(r'author/create/',views.AuthorCreate.as_view(),name='author-create'),
    path(r'author/<int:pk>/update/',views.AuthorUpdate.as_view(),name='author-update'),
]

urlpatterns += [
    path(r'book/<int:pk>/update/', views.BookUpdate.as_view(), name = 'book-update'),
    path(r'books/create/',views.BookCreate.as_view(), name = 'book-create'),
    path(r'book/<int:pk>/delete/', views.BookDelete.as_view(), name = 'book-delete'),
]