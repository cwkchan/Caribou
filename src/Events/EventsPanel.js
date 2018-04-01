import React, { Component } from 'react';
//import Event from './Event'
import events_data from './events.json';
import '../App.css';

class EventsPanel extends Component {
  render() {
    return (
      <div className="Events-panel">
      	<ul className="Events-list">
        {
      		events_data.map(function(event){
            return <li className="Events-event">
              <h2>{event.title}</h2>
              <p>{event.desc}</p>
            </li>;
          })
        }
      	</ul>
      </div>
    );
  }
}

export default EventsPanel;