import json
import datetime
import webbrowser

from renting.models import * 
from django import forms
from django.db import connection
from django.views.generic import View
from django.shortcuts import render

from django.http import HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.
#Render big NETFLEX logo
def home(request):
    return render(request, 'home.html')

def home_login(request, customer_id):
	context = {'customer_id': customer_id}
	return render(request, 'home_login.html', context)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

#Render sign up page
@method_decorator(csrf_exempt, name='dispatch')
class sign_up(View):

	def get(self, request):
		return render(request, 'sign_up.html')

	def post(self, request):

		request.POST = request.POST.copy()

		sql = """SELECT MAX(customer_id) FROM customer"""

		with connection.cursor() as cursor:
			cursor.execute(sql)
			row = cursor.fetchall()

			if row[0]:
				i = row[0][0]
				next_customer_id = str(int(i) +1)
				
			else:
				next_customer_id = "1001"

		request.POST['customer_id'] = next_customer_id
		request.POST['first_name'] = request.POST['first_name']
		request.POST['last_name'] = request.POST['last_name']
		request.POST['phone_number'] = request.POST['phone_number']
		request.POST['email'] = request.POST['email']
		request.POST['password'] = request.POST['password']
		form = CustomerForm(request.POST)

		if form.is_valid():
			form.save()
			return store_login(request, next_customer_id)

		else:
			return render(request, 'sign_up.html')

#Render log in page 
def login(request):

	if request.method == 'GET':

		return render(request, 'login.html')

	if request.method == 'POST':

		if Customer.objects.filter(email=request.POST['email'], password=request.POST['password']).exists():
			customer = Customer.objects.filter(email=request.POST['email'], password=request.POST['password']).values()			
			customer_id = customer[0]['customer_id']
			#print(customer_id)

		else:
			context = {'msg': 'Invalid email or password'}
			return render(request, 'login.html', context)

	return store_login(request, customer_id)

#Render the list of movie avaiable in the website for non log in
def store(request):

	movies = Movie.objects.all()
	context = {'movies':movies}

	return render(request, 'store.html', context)

#filter search and genre for non log in
def search(request):

	if request.method == 'GET':

		keyword = request.GET['keyword']
		movie_genre = request.GET['movie_genre']

		if keyword != '' and movie_genre != '00':	
			movies = Movie.objects.filter(movie_name__contains=keyword,genre_id=movie_genre)
			context = {'movies':movies}

		elif keyword != ''and movie_genre == '00':	
			movies = Movie.objects.filter(movie_name__contains=keyword)
			context = {'movies':movies}

		elif keyword == ''and movie_genre != '00':	
			movies = Movie.objects.filter(genre_id=movie_genre)
			context = {'movies':movies}

		else :
			movies = Movie.objects.all()
			context = {'movies':movies}

		return render(request, 'store.html', context)

#filter search and genre for log in
def search_login(request):

	if request.method == 'GET':

		keyword = request.GET['keyword']
		movie_genre = request.GET['movie_genre']
		customer_id = request.GET['customer_id']

		if keyword != '' and movie_genre != '00':	
			movies = Movie.objects.filter(movie_name__contains=keyword,genre_id=movie_genre)
			context = {'movies':movies,'customer_id':customer_id}

		elif keyword != ''and movie_genre == '00':	
			movies = Movie.objects.filter(movie_name__contains=keyword)
			context = {'movies':movies,'customer_id':customer_id}

		elif keyword == ''and movie_genre != '00':	
			movies = Movie.objects.filter(genre_id=movie_genre)
			context = {'movies':movies,'customer_id':customer_id}

		else :
			movies = Movie.objects.all()
			context = {'movies':movies,'customer_id':customer_id}

		return render(request, 'store_login.html', context)

#Render movie_detail for non log in 
def movie_detail(request, movie_id):

	if request.method == 'GET':

		sql= """SELECT m.movie_name as "movie_name", m.title as "title", m.image as "image", 
		m.price as "price", g.genre_name as "genre_name", p.name as "producer_name"
		FROM movie m JOIN genre g ON m.genre_id = g.genre_id
		JOIN producer p ON m.producer_id = p.producer_id WHERE movie_id = '{}' """.format(movie_id)

		with connection.cursor() as cursor:
			cursor.execute(sql)
			listtype_movie = dictfetchall(cursor)
			movie_id = listtype_movie[0]
			#print(movie)
	
	context = {'movie_id':movie_id}	
	return render(request, 'movie_detail.html', context)

#Render the list of movie avaiable in the website for log in 
def store_login(request, customer_id):

	#movies = Movie.objects.all()
	sql = """SELECT * FROM "movie" """
	with connection.cursor() as cursor:
		cursor.execute(sql)
		movies = dictfetchall(cursor)
		#print(movies)
	context = {'movies':movies,'customer_id':customer_id}

	return render(request, 'store_login.html', context)

#Render movie_detail for log in 
def movie_detail_login(request, customer_id, movie_id):

	if request.method == 'GET':

		sql= """SELECT m.movie_name as "movie_name", m.movie_id as "movie_id", title as "title", m.image as "image", 
		m.price as "price", g.genre_name as "genre_name", p.name as "producer_name"
		FROM movie m JOIN genre g ON m.genre_id = g.genre_id
		JOIN producer p ON m.producer_id = p.producer_id WHERE movie_id = '{}' """.format(movie_id)

		with connection.cursor() as cursor:
			cursor.execute(sql)
			listtype_movie = dictfetchall(cursor)
			movies = listtype_movie[0]
			#print(movies)

	context = {'movies':movies,'customer_id':customer_id}
	return render(request, 'movie_detail_login.html', context)

#Render cart page to show what are in the order
def cart(request, customer_id):
	if request.method == 'GET':

		sql= """SELECT COUNT(movie_id) as "items",SUM(day*20) as "total"
		FROM "order" WHERE customer_id = '{}' """.format(customer_id)

		with connection.cursor() as cursor:
			cursor.execute(sql)
			row = dictfetchall(cursor)
			lineitem = row[0]
			#print(lineitem)

		sql= """SELECT m.movie_id, m.image as "image", m.movie_name as "item", m.price as "price",o.day as "quantity", SUM (o.day * 20) as "total"
		FROM movie m join "order" o on m.movie_id = o.movie_id
		WHERE customer_id = '{}'
		GROUP BY m.movie_id, m.movie_name, m.price, o.day, m.image """.format(customer_id)

		with connection.cursor() as cursor:
			cursor.execute(sql)
			order_list = dictfetchall(cursor)
			#print(order_list)

	context ={"lineitem": lineitem, "order_list": order_list, "customer_id":customer_id}
	return render(request, 'cart.html', context)

#add order into order table and re-render movie detail login
def addcart(request, customer_id, movie_id):

	sql = """SELECT day FROM "order" WHERE customer_id = '{}' AND movie_id = '{}'""".format(customer_id, movie_id)

	with connection.cursor() as cursor:
		cursor.execute(sql)
		row = cursor.fetchall()
		#print(row)

	if bool(row):
		sql = """UPDATE "order" SET day = day+1 WHERE customer_id = '{}' AND movie_id = '{}'""".format(customer_id, movie_id)
		with connection.cursor() as cursor:
			cursor.execute(sql)

	else :
		sql = """INSERT INTO "order" (customer_id, movie_id, day) VALUES ('{}', '{}', 1 )""".format(customer_id, movie_id)
		with connection.cursor() as cursor:
			cursor.execute(sql)

	return movie_detail_login(request, customer_id, movie_id)

#add order into order table and re-render store login
def addcart2(request, customer_id, movie_id):

	sql = """SELECT day FROM "order" WHERE customer_id = '{}' AND movie_id = '{}'""".format(customer_id, movie_id)

	with connection.cursor() as cursor:
		cursor.execute(sql)
		row = cursor.fetchall()

	if bool(row):
		sql = """UPDATE "order" SET day = day+1 WHERE customer_id = '{}' AND movie_id = '{}'""".format(customer_id, movie_id)
		with connection.cursor() as cursor:
			cursor.execute(sql)

	else :
		sql = """INSERT INTO "order" (customer_id, movie_id, day) VALUES ('{}', '{}', 1 )""".format(customer_id, movie_id)
		with connection.cursor() as cursor:
			cursor.execute(sql)

	return store_login(request, customer_id )

#add order into order table and re-render cart
def addcart3(request, customer_id, movie_id):

	sql = """UPDATE "order" SET day = day+1 WHERE customer_id = '{}' AND movie_id = '{}'""".format(customer_id, movie_id)

	with connection.cursor() as cursor:
		cursor.execute(sql)

	return cart(request, customer_id )

#remove order into order table and re-render cart
def removecart(request, customer_id, movie_id):

	sql = """SELECT day FROM "order" WHERE customer_id = '{}' AND movie_id = '{}'""".format(customer_id, movie_id)

	with connection.cursor() as cursor:
		cursor.execute(sql)
		row = cursor.fetchall()
		day = row[0][0]
		#print(day)
		#remove movie row if day(quantity) = 0

	if day == 1 :
		sql = """DELETE FROM "order" WHERE customer_id = '{}' AND movie_id = '{}'""".format(customer_id, movie_id)

		with connection.cursor() as cursor:
			cursor.execute(sql)

	else:
		sql = """UPDATE "order" SET day = day-1 WHERE customer_id = '{}' AND movie_id = '{}'""".format(customer_id, movie_id)
		
		with connection.cursor() as cursor:
			cursor.execute(sql)

	return cart(request, customer_id )

def cart_submit(request, customer_id):

	context = {'customer_id': customer_id}
	return render(request, 'checkout.html', context)

def library(request, customer_id):

	if request.method == 'GET':

		#print(customer_id)
		sql= """SELECT first_name, last_name,  phone_number, email FROM customer WHERE customer_id = '{}' """.format(customer_id)

		with connection.cursor() as cursor:
			cursor.execute(sql)
			customer = dictfetchall(cursor)
		#print(customer[0])

		sql= """SELECT  m.image, m.movie_name FROM "movie" as m, "customer" as c, "order" as o WHERE c."customer_id" = o."customer_id" 
		AND m.movie_id = o.movie_id AND c.customer_id = '{}' """.format(customer_id)

		with connection.cursor() as cursor:
			cursor.execute(sql)
			movie_list = dictfetchall(cursor)

		print(movie_list)

	context = {'customer':customer[0], 'movie_list':movie_list, 'customer_id': customer_id}

	return render(request, 'library.html', context)	

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [name[0].replace(" ", "_").lower() for name in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

