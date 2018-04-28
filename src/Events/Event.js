import React, { Component } from 'react';
//import { withRouter } from 'react-router';
import {Link, withRouter } from 'react-router-dom';

import FontAwesomeIcon from '@fortawesome/react-fontawesome'



//import Event from './Event'
import eating_club_map from './eating_club_map.json';
import '../App.css';

class Event extends Component {

	constructor(props){
		super(props)

		this.buttons = this.buttons.bind(this)
	/*	this.getAllEventInfo = this.getAllEventInfo.bind(this)*/
	}

	componentDidMount(){
		console.log(this.props.loc)
	}

	owner_buttons() {
			return (
				<div className="owner-buttons">
						<button className="btn btn-outline-secondary owner-btn " onClick={(e) => this.props.displayAttendees(e,this.props.pk)}><FontAwesomeIcon icon="user" /></button>
						<button className="btn btn-outline-secondary owner-btn " onClick={(e) => this.props.toggleEditMode(e)}><FontAwesomeIcon icon="pencil-alt" /></button>
						<button className="btn btn-outline-secondary owner-btn" onClick={(e) => this.props.onRemoveEvent(e,this.props.pk)}><FontAwesomeIcon icon="trash-alt" /></button>
				</div>
				);
	}

	buttons() {
		if (this.props.isAttending) {
			return <button className="btn btn-outline-danger leave-button" onClick={() => this.props.onLeaveEvent(this.props.pk)}> Leave </button>
		} else {
			return <button disabled={this.props.attendance==this.props.capacity || this.props.isOwner} className="btn btn-outline-secondary join-button" onClick={() => this.props.onJoinEvent(this.props.pk)}> Join </button>
		}
	}


  render() {

  	return(
    <div className="card Events-event" >

		 <div onClick={()=> this.props.history.push('/events/'+this.props.pk + "/")}>
		 		<div className="event-header Events-panel" disabled = {true}>
			 		<div className="row">
			 			<div className="col">
				  		<h2>{this.props.title}</h2>
				  	</div>
				  	{!!this.props.isOwner && 
				  		<div className="col">
				  		  {this.owner_buttons()}
				  	 </div>
				     }

				  </div>

				  <div className="row"><div className="col">
			    	<p>{eating_club_map[this.props.eating_club]} &bull; {this.props.start} - {this.props.end}</p>
			    </div></div>
				</div>
		 </div>

	    <div className="card-body event-body">
	         <p>{this.props.description}</p>
	         <p style={{fontStyle:'italic'}}>{"Location: "+ this.props.loc}</p>
	         <p>{this.props.attendance == 0 ? "Be the first to join!" : ""+this.props.attendance+"/"+this.props.capacity+" going!"}</p>
	    </div>

	    <div className="event-footer">
	    	{this.buttons()}
	    </div>
    </div>
    );
  }
}

//

export default withRouter(Event);
