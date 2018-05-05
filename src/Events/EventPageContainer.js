import React, { Component } from 'react';
import '../App.css';
import axios from 'axios'
import { withRouter } from 'react-router-dom';
import EventPage from './EventPage';


class EventPageContainer extends Component {
  constructor(props) {
        super(props)
    this.state = {
      fields: {},
      author: '',
      pk: 0,
      isOwner: false,
      isAttending: false,
      loaded: false
    }

    this.onJoinEvent = this.onJoinEvent.bind(this);
    this.onLeaveEvent = this.onLeaveEvent.bind(this);
    this.updateData = this.updateData.bind(this);
}

  updateData(force=false) {
        const event_id = this.props.match.params.event_id;
        const url = "https://bixr.herokuapp.com/api/event/" + event_id + "/";

        axios.get(url)
        .then(res => {
          console.log(res.data);
          this.setState({
              fields: res.data[0].fields,
              pk:res.data[0].pk,
              author:res.data[0].author,
              isOwner: res.data[0].isOwner,
              isAttending: res.data[0].isAttending,
              loaded:true
          }, () => {
            if(force) {
              this.forceUpdate();
            }

          });
    });
  }

  componentDidMount(){
    this.updateData();
  }

  componentDidUpdate(){
    this.updateData();
  }

  displayAttendees(event, event_pk) {
    event.stopPropagation();
    console.log(event);
    const url = "https://bixr.herokuapp.com/api/get_users_for_event/" + event_pk + "/";
    axios.get(url).then(res => {
        var netids = res.data.map(user => user.fields.netid);
        alert(netids);
    })
    .catch(err => alert("err:" + err))
  }


  onJoinEvent(event_id) {
    var data = [{
      event: event_id,
    }]
    axios.post("https://bixr.herokuapp.com/api/join_event/",  data)
    .then(res => this.updateData(true))
    .catch(err => {
          if(err.response.status == 401) {
            // redirect
            if(window.confirm("You must complete your profile before joining an event. Press OK to go to Profile page.")) {
              this.props.history.push('/myprofile/');
            }
          }
    });
  }

  onLeaveEvent(event_id) {
    var data = [{
      event: event_id,
    }]
    //alert(JSON.stringify(data));
      axios.post("https://bixr.herokuapp.com/api/unjoin_event/",  data)
      .then(res => this.updateData(true))
      .catch(err => alert(err));

  }

  shouldComponentUpdate(props, state) {
    return (this.props.match.params.event_id != this.state.pk);
  }



  render() {
    if(this.state.loaded) {
      return(
        <EventPage fields={this.state.fields} 
                   pk={this.state.pk} 
                   author={this.state.author}   
                   isOwner={this.state.isOwner}
                   isAttending={this.state.isAttending}
                   onLeaveEvent={this.onLeaveEvent}
                   onJoinEvent={this.onJoinEvent}
                   displayAttendees={this.displayAttendees}
         />
      );
    } else {
      return <div></div>
    }
  }
}

export default withRouter(EventPageContainer);