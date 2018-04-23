from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest

from django.template.response import TemplateResponse
from django.shortcuts import redirect

from django.urls import reverse
from django.http import HttpResponseRedirect
from api.models import User, PersonalEvent, ClubEvent, JoinedEvents
from django.views.generic import TemplateView
import json
from . import CASClient
from api.decorators import casauth

@casauth
def react(request):
	return TemplateResponse(request, 'index.html', {})

def test(request):
	return HttpResponse("test", status=400)

g_netid = ""
def set_netid(request, netID):
	global g_netid
	g_netid = netID
	return HttpResponse("good", status=200)


#------------------------------------------------------------------------------#
# HELPER FUNCTIONS #
# returns list of event id's
def joined_events_list(netid):
	user = User.objects.get(netid=netid)

	joined_events = JoinedEvents.objects.filter(participant=user)
	joined_events_json = json.loads(serializers.serialize('json', joined_events, fields="event"))

	# send values to a list
	return [e["fields"]["event"] for e in joined_events_json]


# appends isOwner and isAttending fields to list of events
def append_data_to_events(data_json, netid):
	events_joined = joined_events_list(netid)

	data = json.loads(data_json)
	# manipulate data to add owner field, 0 is not owner, 1 is owner
	for e in data: # e is the outer dictionary for the event
		userpk = int(e["fields"]["author"]) # get user pkid
		author = User.objects.get(pk=userpk).netid # user netid

		e["isOwner"] = 1 if author == netid else 0
		e["isAttending"] = 1 if e["pk"] in events_joined else 0


	return json.dumps(data)

	return HttpResponse(datxa_json, content_type='application/json')

# sends an email with given specs
def notify(subject, message, tolist):
	send_mail(subject, message, "example@example.com", tolist, fail_silently=False)


def get_netid(request):
	global g_netid
	if 'netid' in request.session:
		return request.session['netid']
	if g_netid:
		return g_netid
	return "dsawicki"
#------------------------------------------------------------------------------#
@casauth
def get_user(request, netid):
	user = User.objects.filter(netid=netid)
	if (len(user) != 1):
		return HttpResponse("User Not Found", status=404)
	user_json = serializers.serialize('json', user)
	return HttpResponse(user_json, content_type='application/json')

@casauth
def delete_user(request):
	netid = get_netid(request)
	user_set = User.objects.filter(netid=netid)
	user = User.objects.get(netid=netid)
	if len(user_set) != 1:
		return HttpResponse("User Not Found", status=404)
	# check joined events for dependencies
	dependencies_j = JoinedEvents.objects.filter(participant=user)
	if len(dependencies_j) > 0:
		# access the events they've joined
		event_ids = [j.event.id for j in joined_events]
		events = PersonalEvent.objects.filter(id__in=event_ids)
		for e in events: # decrement attendance
			att = e.attendance - 1
			e.attendance = att
			e.save()
	dependencies_j.delete() # remove the joinedevents entries
	# check hosted events for dependencies
	dependencies_e = PersonalEvent.objects.filter(author=user)
	if len(dependencies_e) > 0:
		dependencies_e.delete()
	# delete the user
	user.delete()
	return HttpResponse("deleted user " + netid)

@casauth
def get_events_for_user(request, netid):
	event_ids = joined_events_list(netid)
	events = PersonalEvent.objects.filter(id__in=event_ids)
	events_json = serializers.serialize('json', events)

	data_json = append_data_to_events(events_json, netid)

	return HttpResponse(data_json, content_type='application/json')

#------------------------------------------------------------------------------#
@casauth
def get_events(request):
	#netid = request.session['netid']
	netid = get_netid(request)

	dataq = PersonalEvent.objects.all()
	data_json = serializers.serialize('json', dataq)

	data_json = append_data_to_events(data_json, netid)

	return HttpResponse(data_json, content_type='application/json')

@casauth
def get_event(request, event_id):
	event = PersonalEvent.objects.filter(pk=event_id)
	if (len(event) != 1):
		return HttpResponse("Event Not Found", status=404)
	event_json = serializers.serialize('json', event)
	return HttpResponse(event_json, content_type='application/json')

@casauth
def hosted_events(request, netid):
	netid1 = netid
	user = User.objects.get(netid=netid1)
	events = PersonalEvent.objects.filter(author=user)
	events_json = serializers.serialize('json', events)

	data_json = append_data_to_events(events_json, netid)

	return HttpResponse(data_json, content_type='application/json')

@casauth
def get_users_for_event(request, event_id):
	event = PersonalEvent.objects.get(pk=int(event_id))
	joined_users = JoinedEvents.objects.filter(event=event)
	# make a list of the user ids
	user_ids = []
	for j in joined_users:
		user_id = j.participant.id
		user_ids.append(user_id)
	users = User.objects.filter(id__in=user_ids)
	users_json = serializers.serialize('json', users)
	return HttpResponse(users_json, content_type='application/json')

@csrf_exempt
@casauth
def post_event(request):
	# get the json data
	data_json = json.loads(request.body)
	data = data_json[0]
	# author
	authornetid = get_netid(request)# @casauth ensures they are logged in
	author = User.objects.get(netid=authornetid)
	description = data["description"]
	title = data["title"]
	date = data["date"]
	start = data["start"]
	end = data["end"]
	location = data["location"]
	eating_club = author.eating_club
	capacity = int(data["capacity"])
	e = PersonalEvent(author = author, description = description, title = title, date = date, start=start, end=end, location = location, eating_club = eating_club, capacity = capacity)
	e.save()
	return HttpResponse(e)

@csrf_exempt
@casauth
def delete_event(request, event_id):
	authornetid = get_netid(request) # @casauth ensures they are logged in
	author = User.objects.get(netid=authornetid)
	event_set = PersonalEvent.objects.filter(pk=event_id)
	if len(event_set) != 1:
		return HttpResponse("Event Not Found", status=404)
	event = PersonalEvent.objects.get(pk=event_id)
	# check if the author is correct
	if (event.author != author):
		return HttpResponse("Permission Denied", status=403)
	title = event.title
	# check joined events for dependencies
	dependencies = JoinedEvents.objects.filter(event=event)
	# find attendees
	attendees_id = [j.participant.netid for j in dependencies]

	if len(dependencies) > 0:
		dependencies.delete()
	# email the attendees
	tolist = [n+"@princeton.edu" for n in attendees_id]
	subject = 'An event you joined was deleted'
	message = "placeholderrrrrrr " + title + "."
	notify(subject, message, tolist)

	# delete the event
	event.delete()
	return HttpResponse("deleted event " + title)

@csrf_exempt
@casauth
def edit_event(request, event_id):
	e_set = PersonalEvent.objects.filter(pk=int(event_id))
	if len(e_set) != 1:
		return HttpResponse("Event Not Found", status=404)
	e = PersonalEvent.objects.get(pk=int(event_id))
	# check if correct author
	authornetid = get_netid(request)
	author = Users.objects.get(netid=authornetid)
	if (e.author != author):
		return HttpResponse("Permission Denied", status=403)
	data_json = json.loads(request.body)
	data = data_json[0]
	description = data["description"]
	attendance = data["attendance"]
	title = data["title"]
	date = data["date"]
	start = data["start"]
	end = data["end"]
	location = data["location"]
	capacity = int(data["capacity"])
	if capacity < e.attendance:
		return HttpResponse("Capacity cannot be less than attendance", status=400)
	e.description = description
	e.title = title
	e.date = date
	e.start = start
	e.end = end
	e.location = location
	e.capacity = capacity
	e.save()
	# email attendees
	# find attendees
	joined = JoinedEvents.objects.filter(event=e)
	attendees_id = [j.participant.netid for j in joined]
	tolist = []
	for netid in attendees_id:
		mail = netid + "@princeton.edu"
		tolist.append(mail)
	subject = 'An event you joined was edited'
	message = "PLACEHOLDER " + title + "."
	notify(subject, message, tolist)
	return HttpResponse("event " + str(event_id) + " updated")

#------------------------------------------------------------------------------#
@csrf_exempt
@casauth
def join_event(request):
	data_json = json.loads(request.body)
	data = data_json[0]
	event_id = int(data["event"])
	event_set = PersonalEvent.objects.filter(pk=event_id)

	# event not found
	if len(event_set) != 1:
		return HttpResponse("Event Not Found", status=404)
	event = PersonalEvent.objects.get(pk=event_id)
	# check if event full
	if (event.attendance >= event.capacity):
		return HttpResponse("Event Full", status=400)

	participant_netid = get_netid(request)
	participant = User.objects.get(netid=participant_netid)
	alreadyjoined = JoinedEvents.objects.filter(participant=participant).filter(event=event)
	if len(alreadyjoined) > 0:
		return HttpResponse("Already Joined", status=400)
	# increment attendance
	newatt = event.attendance + 1
	event_set.update(attendance=newatt)
	# add to table
	j = JoinedEvents(participant=participant, event=event)
	j.save()
	# email event host
	host = event.author.netid
	tomail = host + "@princeton.edu"
	tolist = [tomail]
	subject = 'Someone joined your event!'
	message = "Someone just joined your event " + event.title + ". Check who it is!"
	notify(subject, message, tolist)
	return HttpResponse(participant_netid + " joined " + str(event_id) + " " + str(event) + " attendance now " + str(newatt))

@csrf_exempt
@casauth
def unjoin_event(request):
	data_json = json.loads(request.body)
	data = data_json[0]
	event_id = int(data["event"])
	event_set = PersonalEvent.objects.filter(pk=event_id)
	# event not found
	if len(event_set) != 1:
		return HttpResponse("Event Not Found", status=404)
	event = PersonalEvent.objects.get(pk=event_id)
	# check if currently in event
	participant_netid = get_netid(request)
	participant = User.objects.get(netid=participant_netid)
	joined = JoinedEvents.objects.filter(participant=participant).filter(event=event)
	if len(joined) != 1: # if not joined in this event
		return HttpResponse("Event Not Joined", status=400)
	# decrement attendance
	newatt = event.attendance - 1
	event_set.update(attendance=newatt)
	# remove from table
	joined.delete()
	# email event host
	host = event.author.netid
	tomail = host + "@princeton.edu"
	tolist = [tomail]
	subject = 'Someone unjoined your event!'
	message = "Someone just unjoined your event " + event.title + "."
	notify(subject, message, tolist)
	return HttpResponse(participant_netid + " unjoined " + str(event_id) + " " + str(event) + " attendance now " + str(newatt))

#------------------------------------------------------------------------------#
@casauth
def get_club_events(request):
	data = ClubEvent.objects.all()
	data_json = serializers.serialize('json', data)
	return HttpResponse(data_json, content_type='application/json')

#------------------------------------------------------------------------------#
@casauth
def netid(request):
	return JsonResponse({'netid': get_netid(request)})

def login(request):
	C = CASClient.CASClient(request)

	auth_attempt = C.Authenticate()
	if "netid" in auth_attempt:  # Successfully authenticated.
		print("successfully authenticted")
		request.session['netid'] = auth_attempt['netid']
		return redirect("https://bixr.herokuapp.com")
	elif "location" in auth_attempt:  # Redirect to CAS.
		return redirect(auth_attempt["location"])
	else:  # This should never happen!
		abort(500)
