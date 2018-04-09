import React, { Component } from 'react';
import EventsPanel from './EventsPanel';
import EventsFilter from './EventsFilter';
import AddEvent from './AddEvent.js';

import events_data from './events.json';
import filter_data from './filters.json';

import '../App.css';

class Events extends Component {
  constructor() {
  	super();
  	this.state = {
  		filter: {
  			clubs: filter_data.clubs
  		},
  		events: []
  	}


    this.onClubFilterChange = this.onClubFilterChange.bind(this);
    this.onCreateEvent = this.onCreateEvent.bind(this);
  }

  componentDidMount() {
    /*fetch('https://bixr.herokuapp.com/api/')
	.then(res=>{
		return res.json();
	}).then(res_data => {
		// get data from django

		
	});*/

	this.setState({
			events: events_data
		})

  }

  filterEvents(){
	var filtered = events_data.filter(event => this.state.filter.clubs.includes(event.club));

	this.setState({
		events: filtered
	});
  }

  onClubFilterChange(event){
  	var mod = this.state.filter.clubs.slice();

  	if (event.target.checked) { // add to filter
  		if (mod.length == filter_data.clubs.length) // full
  			mod = [];
  		mod.push(event.target.name);
  	} else { // remove from filter
  		// if filter empty, filter should be full..?
  		mod.splice(mod.indexOf(event.target.name), 1)
  		if (mod.length == 0) {
  			mod = filter_data.clubs;
  		}
  	}

  	this.setState({
  		filter: {
  			clubs: mod
  		}
  	}, function() {this.filterEvents()});
  }

  onCreateEvent(event){
  	var new_event = 	{
		"title": "NewEvent",
		"desc": "Come check out this new event",
		"club": "Tower",
		"time": "2:00am",
		"capacity": "0/2"
	}

	var mod = this.state.events
	mod.unshift(new_event)
	this.setState({
		events: mod
	})
  }

  render() {
    return (
    	<div className="Events container">
	      <div className="row">
	        <div className= "col-3">
	        <EventsFilter onClubFilterChange={this.onClubFilterChange}/>
	        </div>

	        <div className= "col-9">
	           <div className= "container">
	              <div className= "row">
	                <AddEvent onCreateEvent={this.onCreateEvent}/>
	                </div>

	                <div className= "row">
	                	<EventsPanel events = {this.state.events}/>
	                </div>
	            </div>
	        </div>
	      </div>
	    </div>
    );
  }
}

export default Events;
