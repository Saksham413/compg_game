from django.conf.urls import include, url
from . import views
import game
app_name='game'
urlpatterns = [
     url(r'^home/',game.views.home, name = 'home'),
     url(r'^register/$',views.register,name='register'),
     url(r'^login/$',views.user_login,name='user_login'),
     url(r'^updateScores/$',views.leaderboard,name='leaderboard'),
]