from django.db import models

# Create your models here.
class genre(models.Model):
    genre_id = models.CharField(max_length=10, primary_key=True)
    genre_name = models.CharField(max_length=20)
    
    class Meta:
        db_table = "genre"
        managed = False
    def __str__(self):
        return self.genre_id

class actor(models.Model):
    actor_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=20)
    gender = models.ForeignKey(genre, on_delete=models.CASCADE, db_column='gender_id')
    
    class Meta:
        db_table = "actor"
        managed = False
    def __str__(self):
        return self.actor_id

class producer(models.Model):
    producer_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=5)

    class Meta:
        db_table = "producer"
        managed = False
    def __str__(self):
        return self.producer_id

class Customer(models.Model):
    customer_id = models.CharField(max_length=10, primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=10)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=10)

    class Meta:
        db_table = "customer"
        managed = False

class Movie(models.Model):
    movie_id = models.CharField(max_length=10, primary_key=True)
    movie_name = models.CharField(max_length=100)
    title = models.CharField(max_length=1000)
    genre_id = models.ForeignKey(genre, on_delete=models.CASCADE, db_column = 'genre_id')
    copyright_date = models.DateTimeField()
    producer_id = models.ForeignKey(producer, on_delete=models.CASCADE, db_column = 'producer_id')
    price = models.FloatField()
    image = models.ImageField()
    
    class Meta:
        db_table = "movie"
        managed = False

    def __str__(self):
        return self.movie_id

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class list_of_actors(models.Model):
    actor_id = models.ForeignKey(actor, on_delete=models.CASCADE, db_column='actor_id')
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id')
    
    class Meta:
        db_table = "list_of_actors"
        unique_together = (("actor_id","movie_id"),)
        managed = False

class credit_card(models.Model):
    card_number = models.FloatField()
    check_digit = models.FloatField()
    exp_date = models.DateTimeField()
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='customer_id')

class order(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='customer_id')
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id')
    day = models.FloatField()
    
    class Meta:
        db_table = "order"
        unique_together = (("customer_id", "movie_id"),)
        managed = False





