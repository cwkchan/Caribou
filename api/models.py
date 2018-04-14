from django.db import models
from datetime import datetime

# eating club
NONE = 'NN'
IVY = 'IV'
COTTAGE = 'CT'
TIGERINN = 'TI'
CAP = 'CA'
COLONIAL = 'CO'
CANNON = 'CN'
CHARTER = 'CH'
QUAD = 'QU'
TOWER = 'TO'
TERRACE = 'TE'
CLOISTER = 'CL'

EATING_CLUB_CHOICES = (
	(NONE, 'None'),
	(IVY, 'The Ivy Club'),
	(COTTAGE, 'University Cottage Club'),
	(TIGERINN, 'Tiger Inn'),
	(CAP, 'Cap and Gown Club'),
	(COLONIAL, 'Colonial Club'),
	(CANNON, 'Cannon Club'),
	(CHARTER, 'Princeton Charter Club'),
	(QUAD, 'Quadrangle Club'),
	(TOWER, ' Princeton Tower Club'),
	(TERRACE, 'Terrace Club'),
	(CLOISTER, 'Cloister Inn'),
	)

# Create your models here.
class User(models.Model):
	# id primary key generated by model
	first_name = models.CharField(max_length=40)
	last_name = models.CharField(max_length=40)
	netid = models.CharField(max_length = 10)
	# res_college
	NONE = 'NN'
	MATHEY = 'MA'
	ROCKY = 'RO'
	BUTLER = 'BU'
	WILSON = 'WI'
	WHITMAN = 'WH'
	FORBES = 'FO'
	RES_COLLEGE_CHOICES = (
		(NONE, 'None'),
		(MATHEY, 'Mathey'),
		(ROCKY, 'Rocky'),
		(BUTLER, 'Butler'),
		(WILSON, 'Wilson'),
		(WHITMAN, 'Whitman'),
		(FORBES, 'Forbes'),
		)
	res_college = models.CharField(
		max_length=2,
		choices = RES_COLLEGE_CHOICES,
		default = NONE,
		)
	year = models.CharField(max_length=4)

	eating_club = models.CharField(
		max_length = 2,
		choices = EATING_CLUB_CHOICES,
		default = NONE,
		)
	clubs_bickering = models.CharField(
		max_length = 2,
		choices = EATING_CLUB_CHOICES,
		default = NONE,
		)
	# picture URL to the image file
	picture = models.URLField('profile picture')

	# user_permission
	#not sure yet
	def __str__(self):
		return self.netid

class PersonalEvent(models.Model):
	event_type = models.CharField(max_length=40, default="")
	date_posted = models.DateTimeField(auto_now=True)
	author = models.ForeignKey('User', on_delete=models.CASCADE,)
	description = models.TextField('description')
	title = models.CharField(max_length=100)
	location = models.CharField(max_length=40)
	dt = datetime.now()
	start_time = models.DateTimeField(default=dt)
	end_time = models.DateTimeField(default=dt)
	eating_club = models.CharField(
		max_length = 2,
		choices = EATING_CLUB_CHOICES,
		default = NONE,
		)
	capacity = models.IntegerField(default=1)
	attendance = models.IntegerField(default=0)

	def __str__(self):
		return self.title

class ClubEvent(models.Model):
	event_type = models.CharField(max_length=40)
	date_posted = models.DateTimeField(auto_now=True)
	author = models.ForeignKey('User', on_delete=models.CASCADE,)
	description = models.CharField(max_length = 300)
	title = models.CharField(max_length=100)
	location = models.CharField(max_length=40)
	dt = datetime.now()
	start_time = models.DateTimeField(default=dt)
	end_time = models.DateTimeField(default=dt)
	eating_club = models.CharField(
		max_length = 2,
		choices = EATING_CLUB_CHOICES,
		default = NONE,
		)
	# tags
	def __str__(self):
		return self.title

class JoinedEvents(models.Model):
	participant = models.ForeignKey('User', on_delete=models.CASCADE)
	event = models.ForeignKey('PersonalEvent', on_delete=models.CASCADE)
	def __str__(self):
		s = self.participant.netid + ": " + str(self.event.id) + " " + self.event.title
		return s