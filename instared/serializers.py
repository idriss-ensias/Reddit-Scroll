from rest_framework import serializers
from random import randint
from instared.models import Posts, Subs, Video, Authors

class PostsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Posts
        fields = ["id", "title", "score", "post_id", "url", "date", "seen","like", "subs_id","author"]
        
class bobo(serializers.ModelSerializer):
    class Meta:
        model = Subs
        fields = ["title"]
        
class SubsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    progress = serializers.SerializerMethodField()
    numposts = serializers.SerializerMethodField()
    hits = serializers.SerializerMethodField()
    bestimage = serializers.SerializerMethodField()
    class Meta:
        model = Subs
        fields = ["id", "title","progress","numposts","hits","bestimage"]
    def get_hits(self,obj) :
        return len(Posts.objects.filter(subs_id=obj.id,like=1))+len(Video.objects.filter(subs_id=obj.id,like=1))
    def get_numposts(self,obj):
        return len(Posts.objects.filter(subs_id=obj.id))+len(Video.objects.filter(subs_id=obj.id))
    def get_progress(self,obj) :
        return len(Posts.objects.filter(subs_id=obj.id,seen=1))+len(Video.objects.filter(subs_id=obj.id,seen=1))
    def get_bestimage(self,obj):
        if(Posts.objects.filter(subs_id=obj.id).count()>0): 
            best = Posts.objects.filter(subs_id=obj.id).order_by("score")[randint(0,int(len(Posts.objects.filter(subs_id=obj.id))/10))]
        else:
            best = None
        if best == None:
            return "https://i.redd.it/grg7nc4ohm161.jpg"
        else :
            return best.url
    
class VideoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Video
        fields = ["id", "title","score","post_id","isiframe","src","height","date","seen","like","subs_id","author"]
        
class SubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subs
        fields = ["title"]
        
class FastSubSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Subs
        fields = ["id","title"]
        
class SerAuth(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = ["name"]

class Subop(serializers.Serializer):
    code = serializers.IntegerField(read_only=True)
    
class Searchnono(serializers.Serializer):
    search = serializers.CharField(read_only=True)
    
class Authser(serializers.ModelSerializer):
    id = serializers.IntegerField()
    progress = serializers.SerializerMethodField()
    numposts = serializers.SerializerMethodField()
    hits = serializers.SerializerMethodField()
    bestimage = serializers.SerializerMethodField()
    class Meta:
        model = Authors
        fields = ["id", "name","progress","numposts","hits","bestimage"]
    def get_hits(self,obj) :
        return len(Posts.objects.filter(author=obj.name,like=1))+len(Video.objects.filter(author=obj.name,like=1))
    def get_numposts(self,obj):
        return len(Posts.objects.filter(author=obj.name))+len(Video.objects.filter(author=obj.name))
    def get_progress(self,obj) :
        return len(Posts.objects.filter(author=obj.name,seen=1))+len(Video.objects.filter(author=obj.name,seen=1))
    def get_bestimage(self,obj):
        print(obj.name)
        if(Posts.objects.filter(author=obj.name).count()>0): 
            best = Posts.objects.filter(author=obj.name).order_by("score")[randint(0,int(len(Posts.objects.filter(author=obj.name))/10))]
        else:
            best = None
        if best == None:
            return "https://i.redd.it/grg7nc4ohm161.jpg"
        else :
            return best.url