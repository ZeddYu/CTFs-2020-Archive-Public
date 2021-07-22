from django.shortcuts import render, HttpResponse
from .models import Post, Feedback
from django.http import JsonResponse
from datetime import datetime, timedelta
from os import getenv


def post_id_handler(req, id):
    if 'fetch' in req.GET:
        p = Post.objects.filter(id=id)
        if len(p) == 1:
            return JsonResponse(p.values('id', 'title', 'content', 'create_at')[0])
        else:
            return HttpResponse(status=404)
    else:
        return render(req, 'posts/post.html')


def post_list_handler(req):
    if 'fetch' in req.GET:
        post_list = Post.objects.order_by('-create_at')
        return JsonResponse(list(post_list.values('id', 'title')), safe=False)
    else:
        return render(req, 'posts/list.html')


def feedback_handler(req):
    if req.method == 'POST':
        fb = {
            'link': req.POST.get('postid', ''),
            'highlight_word': req.POST.get('highlight', ''),
            'ip': req.META.get('HTTP_X_REAL_IP', req.META.get('REMOTE_ADDR'))
        }
        last_fb = Feedback.objects.filter(ip=fb['ip']).order_by('-create_at').first()
        # check if last feedback from is ip is within one minute
        if last_fb is None or last_fb and (datetime.now() - last_fb.create_at) > timedelta(minutes=1):
            wew = Feedback(**fb)
            wew.save()
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=429)
    else:
        if 'fetch' in req.GET:
            if req.user.is_staff:
                fb = Feedback.objects.filter(is_viewed=False).order_by('create_at')[:5]
                ret = list(fb.values('link', 'highlight_word', 'ip'))
                Feedback.objects.filter(pk__in=fb.values_list('pk')).update(is_viewed=True)
                return JsonResponse(ret, safe=False)
            else:
                return HttpResponse(status=403)
        else:
            return render(req, 'posts/feedback.html')


def flag_handler(req):
    if req.user.is_staff:
        return HttpResponse(getenv('CHALLENGE_FLAG'))
    else:
        return HttpResponse(status=401)
