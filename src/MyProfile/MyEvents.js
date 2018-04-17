import React, { Component } from 'react';
import eating_club_map from '../Events/eating_club_map.json';
import '../App.css';
import axios from 'axios'


class MyEvents extends Component {
  constructor(props) {
    super(props)
    this.state={
      myEvents: []
    };

    /*this.handleDelete = this.handleDelete.bind(this);*/
  }

  componentDidMount() {
    const netid = localStorage.getItem('netid') + "/";
    const url = "https://bixr.herokuapp.com/api/get_events";

    axios.get(url
            ).then(res => {
      console.log(res.data);
      this.setState({
        myEvents: res.data
      });
    });
  }



  render() {
    return (
        <div className="Events-panel">
        	<ul className="Events-list">
          {
        		this.state.myEvents.map(function(event){
              return <li className="Events-event">
                <div className="event-header">
                  <h2>{event.fields.title}</h2>
                  <p>{eating_club_map[event.fields.eating_club]} &bull; {event.fields.time}</p>
                </div>
                <p>{event.fields.description}</p>

              </li>;
            }, this)
          }
        	</ul>
        </div>
    );
  }
}

export default MyEvents;