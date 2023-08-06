import abc
import os.path

from PIL import Image
from PIL.ExifTags import TAGS,GPSTAGS
import magic
import exifread
import datetime,dateutil.parser

from microdaemon import abstracts,jsonlib,configurator,common,config

class Media(abc.ABC):

    def __init__(self,obj_id,fpath):
        self.object_id=obj_id
        self._fpath=fpath
        self._fmeta=fpath+".meta"
        self._fthumb=fpath+".thumb.jpeg"

        if not os.path.exists(self._fthumb):
            self._mk_thumbnail()

        self._setup_data()
        self._setup_meta()

        self.fields=[
            configurator.InputField("title",value=self.meta["title"]),
            configurator.InputField("date",value=self.meta["date"]),
        ]

    @property
    def thumbnail_path(self):
        if os.path.exists(self._fthumb):
            return self._fthumb
        return self._default_thumb

    @property
    def url(self):
        return "/%s/%s/" % (self._type,self.object_id)

    @property
    def thumbnail_url(self):
        return "/%s/%s/thumbnail.jpeg" % (self._type,self.object_id)

    def _default_meta(self):
        ret={}
        ret["title"]=os.path.basename(self._fpath)
        ret["date"]=self.data["file_ctime"]
        return ret

    def _setup_meta(self):
        self.meta=abstracts.SerializedDict(self._fmeta)
        default=self._default_meta()
        for k in default:
            if k not in self.meta:
                self.meta[k]=default[k]

    def _setup_data(self): 
        self.data={}
        self.data["mimetype"]=magic.from_file(self._fpath, mime=True)
        self.data["object_id"]=self.object_id
        statinfo = os.stat(self._fpath)
        self.data["file_size"]=statinfo.st_size
        self.data["file_mtime"]=common.to_utc(statinfo.st_mtime)
        self.data["file_ctime"]=common.to_utc(statinfo.st_ctime)

    def _mk_thumbnail(self): pass

class Video(Media):
    _default_thumb=os.path.join(config.DEFAULT_DIR,"video.png")
    _type="videos"

    def _mk_thumbnail(self): 
        pass

    def _setup_data(self):
        Media._setup_data(self)

class Music(Media):
    _default_thumb=os.path.join(config.DEFAULT_DIR,"music.png")
    _type="music"

    def _mk_thumbnail(self): 
        pass

    def _setup_data(self):
        Media._setup_data(self)
    
    def __init__(self,obj_id,fpath):
        Media.__init__(self,obj_id,fpath)

        self.fields+=[
            configurator.InputField("author",value=self.meta["author"]),
            configurator.InputField("album",value=self.meta["album"]),
        ]

    def _default_meta(self):
        ret=Media._default_meta(self)
        ret["author"]=""
        ret["album"]=""
        return ret

class Picture(Media):
    _default_thumb=os.path.join(config.DEFAULT_DIR,"picture.png")
    _type="pictures"

    def __init__(self,obj_id,fpath):
        Media.__init__(self,obj_id,fpath)

        self.fields+=[
            configurator.InputField("author",value=self.meta["author"]),
            #configurator.TextField("description",value=self.meta["description"]),
            configurator.InputField("description",value=self.meta["description"]),
            configurator.InputField("locality",value=self.meta["locality"]),
        ]

    def _default_meta(self):
        ret=Media._default_meta(self)
        if "first_date" in self.data:
            ret["date"]=self.data["first_date"]
        ret["author"]=""
        ret["description"]=""
        ret["locality"]=""
        return ret

    def _mk_thumbnail(self): 
        im = Image.open(self._fpath)
        im.thumbnail( (128,128) )
        im.save(self._fthumb, "JPEG")
        im.close()

    def _setup_data(self):
        Media._setup_data(self)
        im = Image.open(self._fpath)
        for k,val in [ 
                ("width",  im.width),
                ("height", im.height),
                ("mode",   im.mode) ,
                ("format", im.format),
                ("format_description",im.format_description) ]:
            self.data[k]=val
        if "dpi" in im.info:
            self.data["dpi"]=str(im.info["dpi"])
        im.close()

        im=open(self._fpath,"rb")
        tags=exifread.process_file(im,details=False)
        dates=[]
        for tag in tags:
            key=self._exif_label(tag)
            val=self._exif_data(key,tags[tag])
            self.data[key]=val
            if isinstance(val,datetime.datetime): dates.append(val)
        if dates:
            dates.sort()
            self.data["first_date"]=dates[0]
        im.close()

    def _exif_data(self,label,tag_val):
        L,S,ftype=exifread.tags.FIELD_TYPES[tag_val.field_type]
        ftype=ftype.lower()
        ret=str(tag_val)
        if not label[1].startswith("datetime"): return common.try_cast(ret)
        dt=dateutil.parser.parse(val)
        return common.to_utc(dt)

    def _exif_label(self,tag_label):
        t=tag_label.split()
        category=t[0].strip().lower()
        name=" ".join(t[1:]).strip().lower()
        return category+":"+name

class MediaCollection(abstracts.ListDictCollection,abc.ABC):
    _base_class=None
    fields=[ "title", "date" ]
    name=""

    def __init__(self,data_dir):
        abstracts.ListDictCollection.__init__(self)
        self._data_dir=data_dir
        for entry in os.scandir(self._data_dir):
            if not entry.is_file(): continue        
            if entry.name.endswith(".meta"): continue
            if entry.name.endswith(".thumb.jpeg"): continue
            fpath=os.path.join(self._data_dir,entry.name)
            self.append(self._base_class(entry.name,fpath))

class PictureCollection(MediaCollection):
    name="Pictures"
    _base_class=Picture
    fields=MediaCollection.fields+["author","description","locality"]

class VideoCollection(MediaCollection):
    name="Videos"
    _base_class=Video

class MusicCollection(MediaCollection):
    name="Music"
    _base_class=Music
    fields=MediaCollection.fields+["author","album"]

class Playlist(list):
    def __init__(self,fpath):
        list.__init__(self)
        self._fpath=fpath
        self._conf=jsonlib.json_load(self._fpath)
        self.object_id=self._conf["label"]
        self.title=self._conf["title"]
        [ self.append(x) for x in self._conf["list"] ]

    def __str__(self):
        return "%s: %s" % (self.object_id,self.title)

class PlaylistCollection(abstracts.ListDictCollection):
    name="Playlists"

    def __init__(self,data_dir):
        abstracts.ListDictCollection.__init__(self)
        self._data_dir=data_dir
        for entry in os.scandir(self._data_dir):
            if not entry.is_file(): continue        
            if not entry.name.endswith(".json"): continue
            fpath=os.path.join(self._data_dir,entry.name)
            self.append(Playlist(fpath))
        
