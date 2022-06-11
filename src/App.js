import React, { Component }from "react";
import './App.css';

class App extends Component {

  state = {
    events: null,
    name: [],
    venue: [],
    info: [],
    temp: [],
    weather: [],
    high: [],
    low: [],
  }

  callApi = async () => {
    const ipResponse = await fetch("https://geolocation-db.com/json/");
    const ipBody = await ipResponse.json();
    const ip = await ipBody['IPv4'];
    const response = await fetch("http://127.0.0.1:5000/" + ip);
    const body = await response.json();
    if (response.status !== 200) throw Error(body.message);
    const dataEvents = await body['events'];
    const page = await dataEvents['page'];
    const totalElements = await page['totalElements'];
    if ( totalElements === 0 ) {
      this.setState({ events: 'No events'});
    } else {
      var names = [];
      var venues = [];
      var urls = [];
      const embedded = await dataEvents['_embedded'];
      const events = await embedded['events'];
      for (let i = 0; i < events.length; i++) {
        names.push(events[i]['name']);
        venues.push(events[i]['_embedded']['venues'][0]['name']);
        urls.push(events[i]['url']);
      }
      this.setState({ name: names });
      this.setState({ venue: venues });
      this.setState({ info: urls })
      this.setState({ events: 'See event details below:'});
    };
    const dataWeather = await body['weather'];
    const weather = await dataWeather['weather'][0]['main'];
    const temp = await dataWeather['main']['temp'];
    const high = await dataWeather['main']['temp_max'];
    const low = await dataWeather['main']['temp_min'];
    this.setState({ temp: temp })
    this.setState({ weather: weather })
    this.setState({ high: high })
    this.setState({ low: low })
  }

  render() {
    const first = (
      <div>
        <p>Click the button below for a message</p>
        <button onClick={this.callApi}>Show Message</button>
      </div>
    );
    const displayEvents = (
      <div>
        <table>
          <tr>
            <td>Event Name:</td>
            <td>Venue:</td>
            <td>Link for more info:</td>
          </tr>
          <tr>
            <td>
              {this.state.name.map(item => (
                <tr>
                  <td class='item'>
                    {item}
                  </td>
                </tr>
              ))}
            </td>
            <td>
              {this.state.venue.map(item => (
                <tr>
                  <td class='item'>
                    {item}
                  </td>
                </tr>
              ))}
            </td>
            <td>
              {this.state.info.map(item => (
                <tr>
                  <td class='item'>
                    <a href={item}>{item}</a>
                  </td>
                </tr>
              ))}
            </td>
          </tr>
        </table>
      </div>
    );
    const displayWeather = (
      <div>
        <p>
          The Weather In Your Area Is:
        </p>
        <table>
          <tr>
            <td>
              Current Weather:
            </td>
            <td>
              Current Tempature:
            </td>
            <td>
              High:
            </td>
            <td>
              Low:
            </td>
          </tr>
          <tr>
            <td>
              {this.state.weather}
            </td>
            <td>
              {this.state.temp}
            </td>
            <td>
              {this.state.high}
            </td>
            <td>
              {this.state.low}
            </td>
          </tr>
        </table>
      </div>
    )
    if (this.state.events === null) {
      return[first];
    } else {
      return[first, displayEvents, displayWeather];
    }
  }

}

export default App;
