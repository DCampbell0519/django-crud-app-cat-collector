from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner'),
)

class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('toy-detail', kwargs={ 'pk': self.id })  # Class based views need a pk

class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    toys = models.ManyToManyField(Toy)

    # Relate our cats to users
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('cat-detail', kwargs={'cat_id': self.id})

class Feeding(models.Model):
    date = models.DateField('Feeding Date')
    meal = models.CharField(
        max_length=1,
        # add the 'choices' field option
        choices=MEALS,
        # set the default value for meal to be 'B'
        default=MEALS[0][0]
        )
    
    # Create a cat_id column for each feeding in the database
    # FK (Foreign Key) Relationship on Cat
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE) # delete all feedings if we delete the cat
    
    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_meal_display()} on {self.date}"

    class Meta:
        ordering = ['-date'] # this line makes the newest feedings appear first



    
