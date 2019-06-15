from django.shortcuts import render
from web.models import Composer


def oneuser(request, cid):
    composer = Composer.objects.get(cid=cid)
    composer.two_posts = composer.posts[0:2]
    return render(request, 'oneuser.html', {'composer': composer})


def homepage(request, cid):
    composer = Composer.objects.get(cid=cid)
    composer.rest_posts = composer.posts[1:]
    return render(request, 'homepage.html', {'composer': composer})
