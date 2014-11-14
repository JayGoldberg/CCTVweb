from django.db import models

# Camera details
class Camera(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    mac = models.CharField(max_length=17,unique=True)
    ip = models.GenericIPAddressField()
    hostname = models.CharField(max_length=200)
    stream_url = models.CharField(max_length=100,default='now.jpg&push=spush0.5')
    snapshot_url = models.CharField(max_length=100,default='now.jpg')
    username = models.CharField(max_length=32,default='root')
    password = models.CharField(max_length=32,default='system')
    thumbnail = models.CharField(max_length=255)
    add_date = models.DateTimeField(auto_now_add=True)
#    resolutionx = models.PositiveSmallIntegerField()
#    resolutiony = models.PositiveSmallIntegerField()
#    downsample =  models.PositiveSmallIntegerField()
#    sunrise = models.DateTimeField()
#    sunset = models.DateTimeField()
#    caption1 = CharField(max_length=50)
#    caption2 = CharField(max_length=50)
#    prebuffer = models.PositiveSmallIntegerField()
#    prebuffer_delay = models.PositiveSmallIntegerField()
#    postbuffer = models.PositiveSmallIntegerField()
#    postbuffer_delay = models.PositiveSmallIntegerField()
#    timezone = 
#    long = models.DecimalField(max_digits=3,decimal_places=6)
#    lat = models.DecimalField(max_digits=3,decimal_places=6)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name


#class Event(models.Model):
#    image_id = models.ForeignKey('Image')
#    datetime = models.DateTimeField('event date and time')
#    trigger_type = models.CommaSeparatedIntegerField(max_length=9)
#    sequence = models.PositiveSmallIntegerField()
#    archive_delete = # when to delete this event (and the associated images)
#    archive_until = models.DateTimeField('event date and time')
#    thumbnail = 

#    def __str__(self):
#        return self.name


class Image(models.Model):
    path = models.CharField(max_length=255)
    raw_json = models.CharField(max_length=255)
    # Wanted to use MAC, but I feel like it should be pointing to primary key
    # because you could take a camera and move it, and want to restart it in a different
    # location while keeping the old image and event data
    mac = models.ForeignKey('Camera')
    timestamp = models.DateTimeField()
    trigger_type = models.CommaSeparatedIntegerField(max_length=9) # trigger that was active at time
    sequence_number = models.PositiveSmallIntegerField()
    event_id = models.IntegerField()
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    # by default, we will use the middle frame in the sequence of images in 
    thumbnail = models.CharField(max_length=255)

    def __str__(self):
        return self.path


# define tags
class Tag(models.Model):
    name = models.SlugField()
    description = models.CharField(max_length=200)
    # so that we can hide a tag
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    
# supports tag-to-image relationships
class ImageTag(models.Model):
    # images can have many tags, and many tags can be attached to many images
    image_id = models.ManyToManyField('Image')
    tag_id = models.ForeignKey('Tag')
    # not sure if this is required
    #image_is_deleted = models.ForeignKey('Image',to_field='is_deleted')
    #tag_is_deleted = models.ForeignKey('Tag',to_field='is_deleted')


# Notify certain users depending on camera/events
#class Subscriptions(model.Models):
#    user_id = models.ForeignKey(User)
#    cam_id = models.ForeignKey(Camera)
#    window_id = window of camera where detection will send notification of motion to this user

# Probably should not do user mgmt here, use Django's native user system
#class User(model.Models):
#    username = models.CharField(max_length=40)
#    surname = models.CharField(max_length=40)
#    given_name = models.CharField(max_length=40)
#    password = 
#    email = models.EmailField()

#class UserRole():
#
