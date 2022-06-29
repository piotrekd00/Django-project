from django.contrib.auth.decorators import login_required
from . import views
from django.urls import include, path

rental_patterns = ([
                      path('', views.OfficeListView.as_view(), name='all'),
                      path('rentaloffice/<int:pk>/detail', views.OfficeDetailView.as_view(),
                           name='rentaloffice_detail'),
                      path('rentaloffice/create/', login_required(views.OfficeCreateView.as_view()),
                           name='rentaloffice_create'),
], 'rentaloffice')

book_patterns = ([
                      path('book/<int:pk>/detail', views.BookDetailView.as_view(),
                           name='book_detail'),
                      path('book/create/', login_required(views.BookCreateView.as_view()),
                           name='book_create'),
                      path('book/<int:pk>/update/', login_required(views.BookUpdateView.as_view()),
                           name='book_update'),
                      path('book/<int:pk>/delete/', login_required(views.BookDeleteView.as_view()),
                           name='book_delete'),

], 'book')

film_patterns = ([
                      path('film/<int:pk>/detail', views.FilmDetailView.as_view(),
                           name='film_detail'),
                      path('film/create/', login_required(views.FilmCreateView.as_view()),
                           name='film_create'),
                      path('film/<int:pk>/update/', login_required(views.FilmUpdateView.as_view()),
                           name='film_update'),
                      path('film/<int:pk>/delete/', login_required(views.FilmDeleteView.as_view()),
                           name='film_delete'),
], 'film')

cd_patterns = ([
                      path('cd/<int:pk>/detail', views.CDDetailView.as_view(),
                           name='cd_detail'),
                      path('cd/create/', login_required(views.CDCreateView.as_view()),
                           name='cd_create'),
                      path('cd/<int:pk>/update/', login_required(views.CDUpdateView.as_view()),
                           name='cd_update'),
                      path('cd/<int:pk>/delete/', login_required(views.CDDeleteView.as_view()),
                           name='cd_delete'),
], 'cd')

rented_patterns = ([
                    path('users/<int:user_id>', views.UserRent.as_view(),
                         name='rented_list'),
                    path('rent/<int:item_id>', login_required(views.RentedCreateView.as_view()),
                         name='rented_create'),
                    path('delete/<int:pk>', login_required(views.RentedDeleteView.as_view()),
                         name='rented_delete'),
], 'rented')

scoreboard_patterns = ([
                    path('scoreboard', views.ScoreboardListView.as_view(),
                         name='scoreboard'),
                    path('stats', views.StatsView.as_view(),
                         name='stats'),
], 'scoreboard')

urlpatterns = [
    path('', include(rental_patterns)),
    path('', include(book_patterns)),
    path('', include(film_patterns)),
    path('', include(cd_patterns)),
    path('', include(rented_patterns)),
    path('', include(scoreboard_patterns)),
]
