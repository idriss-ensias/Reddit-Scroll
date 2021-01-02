from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.template import loader
from .models import Subs, Posts, Video, Authors, Update, redo
from .serializers import PostsSerializer, SubsSerializer, VideoSerializer, SubSerializer, FastSubSerializer, Subop, Authser, SerAuth, bobo, Searchnono
from random import randint
from django.shortcuts import render
import praw

def combo(idd):
    combo = []
    reddit = redo()
    sub = reddit.submission(id=idd)
    sub.comment_sort="best"
    sub.comments.replace_more(limit=0)
    for tlc in sub.comments.list():
        fofo = []
        fofo.append(tlc.body)
        pipi=[]
        for i in tlc.replies:
            pipi.append(i.body)
        fofo.append(pipi)
        combo.append(fofo)
    return combo
    
def terma(idd):
    reddit = redo()
    sub = reddit.submission(id=idd)
    return "https://reddit.com"+sub.permalink

def pie(arr,size):
    product = []
    if len(arr)<size:
        return [arr]
    else:
        for i in range(1,len(arr)+1):
            if i%size == 0:
                product.append([])
                for j in reversed(range(1,size+1)):
                    product[len(product)-1].append(arr[i-j])
                if (len(arr)-i<size) and i!=len(arr):
                    product.append(arr[i:len(arr)])
    return product
    
def subgrid(request):
    return render(request, 'instared/pdidi.html')
    
def authgrid(request):
    return render(request, 'instared/pdidi2.html')
    
def upo(request):
    return render(request, 'instared/oxyblan.html', {'updates':Update.objects.all().order_by('-update_date'),'subs':Subs.objects.all()})

def feed(request):
    return render(request, 'instared/ivfeed1.html',{'allp':Posts.objects.all().count(), 'allv':Video.objects.all().count(), 'seep':Posts.objects.filter(seen=1).count(),'seev':Video.objects.filter(seen=1).count(), 'subos':Subs.objects.all()})
    
def feedsub(request,sub):
    return render(request, 'instared/ivfeed3.html',{"subd":sub,"titlos":Subs.objects.get(pk=sub).title,'allp':Posts.objects.filter(subs_id=sub).count(), 'allv':Video.objects.filter(subs_id=sub).count()})
    
def feedauth(request,auth):
    return render(request, 'instared/ivfeed4.html',{"authd":auth,'allp':Posts.objects.filter(author=auth).count(), 'allv':Video.objects.filter(author=auth).count()})
    
def lookit(request,search):
    return render(request,"instared/fliflo.html",{"searchd":search})
    
def refre(request,pk):
    if request.method == "GET":
        Subs.objects.get(pk=pk).refresh()
        return HttpResponse(status=200)

def refrea(request,auth):
    if request.method == "GET":
        Authors.objects.get(name=auth).refresh()
        return HttpResponse(status=200)
        
def ups(request,tit):
    if Subs.objects.filter(title=tit).count() > 0 :
        Subs.objects.filter(title=tit)[0].try_tk()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)

@csrf_exempt
def posts_auth(request,auth,ind):
    sent = []
    alla = pie(Posts.objects.filter(author=auth).order_by("-score"),10)
    if ind<len(alla):
        sent = alla[ind]
    serializer = PostsSerializer(sent, many=True)
    return JsonResponse(serializer.data, safe=False)

def videos_auth(requests,auth,ind):
    sent = []
    vids = pie(Video.objects.filter(author=auth).order_by("-score"),1)
    if(ind<len(vids)):
        sent = vids[ind]
    serializer = VideoSerializer(sent, many=True)
    return JsonResponse(serializer.data, safe=False)
  
@csrf_exempt
def posts_sub(request,sub,ind):
    sent = []
    pots = pie(Posts.objects.filter(subs_id=sub).order_by("-score"),10)
    if(ind<len(pots)):
        sent = pots[ind]
    serializer = PostsSerializer(sent, many=True)
    return JsonResponse(serializer.data, safe=False)

def videos_sub(requests,sub,ind):
    sent = []
    vids = pie(Video.objects.filter(subs_id=sub).order_by("-score"),1)
    if(ind<len(vids)):
        sent = vids[ind]
    serializer = VideoSerializer(sent, many=True)
    return JsonResponse(serializer.data, safe=False)
    
def videos_comp(requests,sub,ind):
    vids = []
    if(Video.objects.filter(subs_id=sub).count()-ind>=4):
        vids = Video.objects.filter(subs_id=sub).order_by("-score")[ind:ind+4]
        serializer = VideoSerializer(vids, many=True)
        return JsonResponse(serializer.data, safe=False)
    if ((Video.objects.filter(subs_id=sub).count()-ind<4) and (Video.objects.filter(subs_id=sub).count()-ind>0)):
        for i in range(0,Video.objects.filter(subs_id=sub).count()-ind):
            vids.append(Video.objects.filter(subs_id=sub).order_by("-score")[i])
        serializer = VideoSerializer(vids, many=True)
        return JsonResponse(serializer.data, safe=False)
    return HttpResponse(status=404)
        
def videos_acomp(requests,auth,ind):
    vids = []
    if(Video.objects.filter(author=auth).count()-ind>=4):
        vids = Video.objects.filter(author=auth).order_by("-score")[ind:ind+4]
        serializer = VideoSerializer(vids, many=True)
        return JsonResponse(serializer.data, safe=False)
    if ((Video.objects.filter(author=auth).count()-ind<4) and (Video.objects.filter(author=auth).count()-ind>0)):
        for i in range(0,Video.objects.filter(author=auth).count()-ind):
            vids.append(Video.objects.filter(author=auth).order_by("-score")[i])
        serializer = VideoSerializer(vids, many=True)
        return JsonResponse(serializer.data, safe=False)
    return HttpResponse(status=404)

def post_det(requests,pk):
    post = Posts.objects.get(pk=pk)
    return render(requests ,"instared/sarakue.html" ,{"post":post,"permalink":terma(post.post_id),"comlist":combo(post.post_id)})
    
def vid_det(requests,pk):
    post = Video.objects.get(pk=pk)
    return render(requests ,"instared/ninakue.html" ,{"post":post,"permalink":terma(post.post_id),"comlist":combo(post.post_id)})

@csrf_exempt
def posts_list(request):
    if request.method == "POST":
        pipi = []
        data = JSONParser().parse(request)
        for i in data:
            serializer = bobo(data=i)
            if serializer.is_valid():
                pipi.append(serializer.validated_data["title"])
        posts = Subs.feepo(10,pipi)
        serializer = PostsSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
        
def posto_search(request,search):
    serializer = PostsSerializer(Posts.objects.filter(title__contains=search.replace("_"," ")), many=True)
    return JsonResponse(serializer.data, safe=False)
    
def videoo_search(request,search):
    serializer = VideoSerializer(Video.objects.filter(title__contains=search.replace("_"," ")), many=True)
    return JsonResponse(serializer.data, safe=False)
    
def subs_list(request):
    subs = Subs.objects.all()
    serializer = SubsSerializer(subs, many=True)
    return JsonResponse(serializer.data, safe=False)
    
def bus_list(request):
    subs = Subs.objects.all()
    serializer = FastSubSerializer(subs, many=True)
    return JsonResponse(serializer.data, safe=False)
    
def auth_list(request):
    auths = Authors.objects.all()
    serializer = Authser(auths, many=True)
    return JsonResponse(serializer.data, safe=False)
@csrf_exempt
def videos_list(request):
    if request.method == "POST":
        pipi = []
        data = JSONParser().parse(request)
        for i in data:
            serializer = bobo(data=i)
            if serializer.is_valid():
                pipi.append(serializer.validated_data["title"])
        videos = Subs.feevo(1,pipi)
        serializer = VideoSerializer(videos, many=True)
        return JsonResponse(serializer.data, safe=False)
@csrf_exempt
def unseep(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        for i in data:
            serializer = PostsSerializer(data=i)
            if serializer.is_valid():
                obj = Posts.objects.get(pk=int(serializer.validated_data["id"]))
                obj.seen=1
                obj.save()
            else:
                print(serializer.errors)
        return HttpResponse(status=200)
        
@csrf_exempt
def delete_videos(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        for i in data:
            serializer = VideoSerializer(data=i)
            if serializer.is_valid():
                obj = Video.objects.get(pk=int(serializer.validated_data["id"]))
                obj.seen=1
                obj.save()
            else:
                print(serializer.errors)
        return HttpResponse(status=200)

def uplouplo(request):
    if request.method == "GET":
        Subs.update_all()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)
       
@csrf_exempt
def del_p(request,pk):
    if request.method == "GET":
        Posts.objects.get(pk=pk).delete()
        return HttpResponse(status=200)
@csrf_exempt
def del_v(request,pk):
    if request.method == "GET":
        Video.objects.get(pk=pk).delete()
        return HttpResponse(status=200)
@csrf_exempt
def delsub(request,pk):
    if request.method == "GET":
        Subs.objects.get(pk=pk).delete()
        return HttpResponse(status=200)
@csrf_exempt
def delauth(request,auth):
    if request.method == "GET":
        Authors.objects.filter(name=auth)[0].delete()
        return HttpResponse(status=200)
@csrf_exempt
def like_p(request,pk):
    if request.method == "GET":
        obj = Posts.objects.get(pk=pk)
        obj.like = 1
        obj.save()
        return HttpResponse(status=200)
@csrf_exempt
def like_v(request,pk):
    if request.method == "GET":
        obj = Video.objects.get(pk=pk)
        obj.like = 1
        obj.save()
        return HttpResponse(status=200)
@csrf_exempt
def dlike_p(request,pk):
    if request.method == "GET":
        obj = Posts.objects.get(pk=pk)
        obj.like = 0
        obj.save()
        return HttpResponse(status=200)
@csrf_exempt
def dlike_v(request,pk):
    if request.method == "GET":
        obj = Video.objects.get(pk=pk)
        obj.like = 0
        obj.save()
        return HttpResponse(status=200)

@csrf_exempt
def add_sub(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = SubSerializer(data=data)
        if serializer.is_valid():
            if len(Subs.objects.filter(title__contains=serializer.validated_data["title"]))==0 :
                if Subs.sub_exists(serializer.validated_data["title"]):
                    hap = {"code" : 0}
                    ns = Subs(title=serializer.validated_data["title"])
                    ns.save()
                    ns.try_tk()
                    return JsonResponse(Subop(hap).data, status=200)
                else :
                    hap = {"code" : 1}
                    return JsonResponse(Subop(hap).data, status=200)
            else :
                hap = {"code" : 2}
                return JsonResponse(Subop(hap).data, status=200)
        else:
            hap = {"code" : 3}
            return JsonResponse(Subop(hap).data, status=200)
    else:
        return HttpResponse(status=404)
        
@csrf_exempt
def add_auth(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = SerAuth(data=data)
        if serializer.is_valid():
            if (len(Posts.objects.filter(author__contains=serializer.validated_data["name"])) + len(Video.objects.filter(author__contains=serializer.validated_data["name"])))!=0 :
                if(len(Authors.objects.filter(name__contains=serializer.validated_data["name"])) == 0): 
                    hap = {"code" : 0}
                    ns = Authors(name=serializer.validated_data["name"])
                    ns.save()
                    return JsonResponse(Subop(hap).data, status=200)
                else :
                    hap = {"code" : 2}
                    return JsonResponse(Subop(hap).data, status=200)
            else:
                hap = {"code" : 3}
                return JsonResponse(Subop(hap).data, status=200)
    else:
        return HttpResponse(status=404)
                