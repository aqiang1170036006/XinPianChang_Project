from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from web.models import Post, Comment


def index(request, page=1):
    cur_page = int(page)
    posts = Post.objects.order_by('-play_counts')
    paginator = Paginator(posts, 24)
    posts = paginator.page(cur_page)

    page_num = 5
    first_page = 1
    last_page = paginator.num_pages

    display_pages = range(cur_page - page_num // 2, cur_page + page_num // 2 + 1)
    if cur_page - page_num // 2 == 1:
        display_pages = range(cur_page - 1, cur_page + page_num - 1)
    elif cur_page - page_num // 2 < 1:
        display_pages = range(cur_page, cur_page + page_num)
    elif cur_page + page_num // 2 > last_page:
        display_pages = range(cur_page - page_num, cur_page + 1)

    if cur_page == 1:
        display_pages = range(cur_page, cur_page + page_num + 1)
    display_pages = list(display_pages)
    if first_page not in display_pages:
        display_pages.insert(0, first_page)

    return render(request, 'index.html', locals())


def detail(request, pid):
    post = Post.objects.get(pid=pid)
    post.composers[0].posts
    return render(request, 'post.html', {'post': post})


def comment2dict(comment):
    data = {
        "id": comment.id,
        "resource_id": comment.pid,
        "userid": comment.cid,
        "content": comment.content,
        "addtime": comment.created_at,
        "count_approve": comment.like_counts,
        "referid": comment.referid,
        "userInfo": {
            "id": comment.cid,
            "url": "/user/%s" % comment.cid,
            "web_url": "http://test.xinpianchang.com/u%s" % comment.cid,
            "username": comment.uname,
            "avatar": comment.avatar,
            "about": "",
            "verify_description": "",
            "sex": 1,
            "count": {
                "count_followee": 0,
                "count_follower": 0,
                "count_collected": 0,
                "count_article_viewed": 0,
                "count_liked": 0
            },
            "is_administrator": False,
            "author_type": 0
        },
        "is_approved": False
    }
    if data['referid']:
        refer = Comment.objects.get(id=comment.referid)
        data["referer"] = comment2dict(refer)
    return data


def comments(request):
    pid = request.GET.get('resource_id')
    page = request.GET.get('page')
    comments = Comment.objects.filter(pid=pid)
    paginator = Paginator(comments, 10)
    comments = paginator.page(int(page))
    next_page = None
    if comments.has_next():
        next_page = "/comments?page=%s&resource_id=%s&type=article" % (comments.next_page_number(), pid)
    data = {
        "status": 0,
        "code": "_200",
        "message": "OK",
        "data": {
            "expand": "hot",
            "total": paginator.count,
            "page_size": paginator.num_pages,
            "next_page_url": next_page,
            "list": [comment2dict(comment)for comment in comments]
        }
    }
    return JsonResponse(data)


def index_php(request):
    return JsonResponse({
        "all": 0,
        "systemNum": 0,
        "replayNum": 0,
        "articleCommentNum": None,
        "topicCommentNum": None,
        "projectCommentNum": 0,
        "expCommentNum": 0,
        "selfNum": 0,
        "fans": 0,
        "inviteNum": 0,
        "atNum": 0,
        "approveNum": 0,
        "noticeNum": 0,
        "likeNum": 0,
        "ts": "/message/my/ts-notice"
    })

def ts_view(request):
    return JsonResponse({'count': 0})