from django.db import models

# Camera details
class Camera(models.Model):
    name = models.CharField(max_length=200)  
    description = models.CharField(max_length=200)
    mac = models.CharField(max_length=17)
    ip = models.GenericIPAddressField()
    hostname = models.CharField(max_length=200)
    thumbnail = models.CharField(max_length=200) 
#    resolution = 
#    downsample =
#    sunrise = 
#    sunset =
#    caption1 =
#    caption2 =
#    prebuffer = 
#    prebuffer_delay = 
#    postbuffer =
#    postbuffer_delay =
#    timezone = 
#    long = 
#    lat = 
    enabled = models.BooleanField()
#    live_monitoring = models.BooleanField()
    add_date = models.DateTimeField('date added')

#class Event(models.Model):
#    image_id = foreign key to Image table
#    datetime = models.DateTimeField('event date and time')
#    trigger_type = models.CharField(max_length=200) # how this event was triggered
#    sequence = models.smallint(default=0)
#    event_id = primary key for this table
#    archive_delete = # when to delete this event (and the associated images)
#    archive_until = models.DateTimeField('event date and time')
#    thumbnail = 

class Image(models.Model):
    path = models.CharField(max_length=255)
    raw_json = models.CharField(max_length=255)
    mac = models.CharField(max_length=255)
    timestamp = models.DateTimeField
    trigger_type = models
    sequence_number = models.IntegerField()
    event_id = models.IntegerField()
    cam_id = models.ForeignKey(Camera)
    deleted = models.BooleanField()
    thumbnail_event =  

# Probably should not do user mgmt here, use Django's native user system
#class User(model.Models):
#    username = models.CharField(max_length=40)
#    surname = models.CharField(max_length=40)
#    given_name = models.CharField(max_length=40)
#    password = 
#    email = models.EmailField()

#class UserRole():
#

    
# define tags
class Tag(model.Models):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    
# supports tagging events
#class EventTags(model.Models):
#    event_id = models.ManyToManyField(Event)
#    tag_id = models.ForeignKey(Tag)

# Notify certain users depending on camera/events
#class Subscriptions(model.Models):
#    user_id = models.ForeignKey(User)
#    cam_id = models.ForeignKey(Camera)
#    window_id = window of camera where detection will send notification of motion to this user
