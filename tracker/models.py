from django.db import models

class Click(models.Model):
    label = models.CharField(max_length=100)
    count = models.IntegerField(default=0)
    session_key = models.CharField(max_length=255)

    def increment(self):
        self.count += 1
        self.save()

    def decrement(self):
        if self.count > 0:
            self.count -= 1
            self.save()

    def __str__(self):
        return f"{self.label} ({self.count})"
