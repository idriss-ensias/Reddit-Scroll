from django.db import models
import praw
from random import randint
from datetime import datetime
from bs4 import BeautifulSoup

def redo():
    reddit = praw.Reddit(
        client_id="XXXXXXXXXXXXXXXXX",
        client_secret="XXXXXXXXXXXXXXXXX",
        user_agent="XXXXXXXXXXXXXXXXXXXX",
        username="XXXXXXXXXXXXXX",
        password="XXXXXXXXXXXXXXXXX*"
        )
    return reddit

class Subs(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title
    def unsee(self):
        for i in Posts.objects.filter(subs=self):
            i.seen = 0
            i.save()
    @staticmethod
    def refresh():
        for i in Subs.objects.all():
            i.unsee()
    @staticmethod
    def sub_exists(title):
        reddit = redo()
        try : 
            if len(reddit.subreddits.search_by_name(title,True,True))>0:
                return True
        except :
            return False
    @staticmethod
    def update_all():
        for i in Subs.objects.all():
            i.try_tk()
    def clean(self):
        ptitles = []
        for i in Posts.objects.filter(subs=self):
            ptitles.append(i.title)
        ptitles = list(dict.fromkeys(ptitles))
        for i in ptitles:
            if Posts.objects.filter(title=i).count()>1:
                a = Posts.objects.filter(title=i).count()
                for j in range(1,a):
                    Posts.objects.filter(title=i)[1].delete()
        vtitles = []
        for i in Video.objects.filter(subs=self):
            vtitles.append(i.title)
        vtitles = list(dict.fromkeys(vtitles))
        for i in vtitles:
            if Video.objects.filter(title=i).count()>1:
                a = Video.objects.filter(title=i).count()
                for j in range(1,a):
                    Video.objects.filter(title=i)[1].delete()
    @staticmethod
    def clean_all():
        for i in Subs.objects.all():
            i.clean()
    def try_tk(self):
        num = 0
        reddit = redo()
        try:
            subreddit = reddit.subreddit(self.title)
            for submission in subreddit.new(limit=600):
                if len(Posts.objects.filter(title=submission.title))==0 and len(Video.objects.filter(title=submission.title))==0:
                    if len(Posts.objects.filter(url=submission.url))==0 :
                        if len(Posts.objects.filter(post_id=submission.id))==0 and len(Video.objects.filter(post_id=submission.id))==0:
                            if submission.url.endswith('jpg') or submission.url.endswith('jpeg') or submission.url.endswith('png'):
                                nt = submission.title.replace("'","''").replace('"','""')
                                if submission.author == None:
                                    aut = "0623415564"
                                else:
                                    aut = submission.author.name
                                Posts(title=submission.title,url=submission.url,score=submission.score,subs=self,post_id=submission.id,author=aut).save()
                                num = num + 1
                            if submission.media != None:
                                tn = submission.title.replace("'","''").replace('"','""')
                                if submission.author == None:
                                    auh = "0623415564"
                                else:
                                    auh = submission.author.name
                                if "type" in submission.media:
                                    if submission.media["type"] != "reddit_video":
                                        ifr = submission.media["oembed"]["html"].replace("\n","")
                                        soup = BeautifulSoup(ifr)
                                        if soup.iframe != None:
                                            del soup.iframe["style"]
                                            del soup.iframe["class"]
                                            del soup.iframe["width"]
                                            soup.iframe["width"]="100%"
                                            if soup.iframe["height"] == "100%":
                                                soup.iframe["height"] = "400"
                                            else:
                                                if int(soup.iframe["height"]) > 600:
                                                    soup.iframe["height"] = 600
                                            ht = soup.iframe["height"]
                                            ifr = str(soup)
                                            Video(title=tn,score=submission.score,isiframe=1,src=ifr,author=auh,height=ht,subs=self,post_id=submission.id).save()
                                            num = num + 1
        except:
            print("wayli")
        Update(subs=self,posts_retreived=num).save()
    @staticmethod
    def ranking():
        finpass = []
        ranks = dict()
        for i in Subs.objects.all():
            ranks[i.title] = Posts.objects.filter(subs=i,like=1).count()+Video.objects.filter(subs=i,like=1).count()
            finpass.append(Posts.objects.filter(subs=i,like=1).count()+Video.objects.filter(subs=i,like=1).count()) 
        finpass = sorted(list(dict.fromkeys(finpass)))
        for i in Subs.objects.all():
            if ranks[i.title] in finpass:
                ranks[i.title] = finpass.index(ranks[i.title])
            else:
                ranks[i.title] = 0
        sorank = []
        for i in Subs.objects.all():
            for j in range(0,ranks[i.title]+1):
                sorank.append(i.title)
        return sorank
    @staticmethod
    def lerank():
        thrank = []
        for i in Subs.objects.all():
            thrank.append(Posts.objects.filter(subs=i).count()+Video.objects.filter(subs=i).count())
        egrank = sorted(list(dict.fromkeys(thrank)))
        lerank = dict()
        for i in Subs.objects.all():
            if Posts.objects.filter(subs=i).count()+Video.objects.filter(subs=i).count() in egrank:
                lerank[i.title] = egrank.index(Posts.objects.filter(subs=i).count()+Video.objects.filter(subs=i).count())
            else:
                lerank[i.title] = 0
        rankso = []
        for i in Subs.objects.all():
            for j in range(0,lerank[i.title]+1):
                rankso.append(i.title)
        return rankso+Subs.ranking()
    def randop(self,fikano):
        if (Posts.objects.filter(subs=self,seen=0).count() > 0) and (self.title in fikano):
            if Posts.objects.filter(subs=self,seen=0).count()>10:
                return Posts.objects.filter(subs=self,seen=0).order_by("-score")[:10][randint(0,9)]
            else:
                return Posts.objects.filter(subs=self,seen=0).order_by("-score")[randint(0,Posts.objects.filter(subs=self,seen=0).count()-1)]
        else:
            return None
    def randov(self,fikano):
        if (Video.objects.filter(subs=self,seen=0).count() > 0) and (self.title in fikano):
            if Video.objects.filter(subs=self,seen=0).count()>10:
                return Video.objects.filter(subs=self,seen=0).order_by("-score")[:10][randint(0,9)]
            else:
                return Video.objects.filter(subs=self,seen=0).order_by("-score")[randint(0,Video.objects.filter(subs=self,seen=0).count()-1)]
        else:
            return None
    @staticmethod
    def ninio(liko):
        coco = 0
        for i in liko:
            coco = coco + Posts.objects.filter(subs__title=i).count()
        return coco
    @staticmethod
    def feepo(num,pipo):
        rk = Subs.lerank()
        foop = []
        tots = Subs.ninio(pipo)
        while((len(foop)<num)and(len(foop)<tots)):
            eli = rk[randint(0,len(rk)-1)]
            alp = Subs.objects.filter(title=eli)[0].randop(pipo)
            if alp != None:
                if alp not in foop:
                    foop.append(alp)
        return foop
    @staticmethod
    def feevo(num,pipo):
        rk = Subs.lerank()
        foov = []
        tots = Subs.ninio(pipo)
        while((len(foov)<num)and(len(foov)<tots)):
            eli = rk[randint(0,len(rk)-1)]
            alp = Subs.objects.filter(title=eli)[0].randov(pipo)
            if alp != None:
                if alp not in foov:
                    foov.append(alp)
        return foov
    def refresh(self):
        for i in Posts.objects.filter(subs=self):
            i.seen = 0
            i.save()
        for i in Video.objects.filter(subs=self):
            i.seen = 0
            i.save()
class Posts(models.Model):
    subs = models.ForeignKey(Subs, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    score = models.IntegerField()
    post_id = models.CharField(max_length=200)
    url = models.CharField(max_length=1000)
    author = models.CharField(max_length=1000)
    date = models.DateField(default=datetime.today().strftime('%Y-%m-%d'))
    seen = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    @staticmethod
    def zearch(search):
        return Posts.objects.filter(title__icontains=search)

class Video(models.Model):
    subs = models.ForeignKey(Subs, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    score = models.IntegerField()
    post_id = models.CharField(max_length=1000)
    isiframe = models.IntegerField()
    src = models.TextField()
    height = models.IntegerField()
    author = models.CharField(max_length=1000)
    date = models.DateField(default=datetime.today().strftime('%Y-%m-%d'))
    seen = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    @staticmethod
    def zearch(search):
        return Video.objects.filter(title__icontains=search)

class Authors(models.Model):
    name = models.CharField(max_length=200)
    def refresh(self):
        for i in Posts.objects.filter(author=self.name):
            i.seen = 0;
            i.save()
        for i in Video.objects.filter(author=self.name):
            i.seen = 0;
            i.save()

class Update(models.Model):
    subs = models.ForeignKey(Subs, on_delete=models.CASCADE)
    update_date = models.DateField(default=datetime.today().strftime('%Y-%m-%d'))
    posts_retreived = models.IntegerField(default=0)
    