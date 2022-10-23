import uuid 
from django.db import models


class Poll(models.Model):
    
    secondary_id = models.UUIDField(default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=2000)
    
    def __str__(self):
        return self.question
    
    @property 
    def total_voters(self):
        return self.votes.count()


class Option(models.Model):
    
    secondary_id = models.UUIDField(default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=1000)
    poll = models.ForeignKey(Poll, null=False, blank=False, related_name="options", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text
    
    @property 
    def vote_percentage(self):
        if not self.poll.total_voters == 0:
            return (self.votes.count() / self.poll.total_voters) * 100
        return 0
       
            
    
class AnonymousUser(models.Model):
    secondary_id = models.UUIDField(default=uuid.uuid4, editable=False)
    
    
    
class Vote(models.Model):
    
    poll = models.ForeignKey(Poll, null=False, blank=False, related_name="votes", on_delete=models.CASCADE)
    option = models.ForeignKey(Option, null=False, blank=False, related_name="votes", on_delete=models.CASCADE)
    voter = models.ForeignKey(AnonymousUser, null=False, blank=False, related_name="votes", on_delete=models.CASCADE)
    
    