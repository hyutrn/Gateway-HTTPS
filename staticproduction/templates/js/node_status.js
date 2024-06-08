const now = new Date();
var data_list = [];
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

const client = mqtt.connect('ws://rasp.local:8083/mqtt', {
  clientId: getCookie('username') + now.getTime(),  // Replace with a unique client ID
  username: 'node',
  password: 'test'
});

client.on('connect', () => {
  console.log('Connected to MQTT broker!');

  // Subscribe to topics or publish messages here
  client.subscribe('nodes/sensors/#', { qos: 1 }, (error) => {
    if (!error) {
      console.log('Subscribed to test topic!');
    }
    else {
      console.alert('Error subscribing a topic!');
    }
  });
  client.subscribe('nodes/actuators/#', { qos: 1 }, (error) => {
    if (!error) {
      console.log('Subscribed to test topic!');
    }
    else {
      console.alert('Error subscribing a topic!');
    }
  });
});

client.on('error', (error) => {
  console.error('Connection error:', error);
});

client.on('message', function (topic, message) {
  console.log(message.toString())
})

// Use fetch GET method to get the data from the server when web is loaded with URL: /get_data and console.log the data
window.addEventListener('load', () => {
  fetch('/get_data')
    .then(response => response.json())
    .then(data => {
      data_list = data;
      console.log(data);
      generateTable(data);
    });
});

function generateTable(data) {
  for (const item in data) {
    if (item.feature == "sensor") {
      generateInformationSensor(item);
    }
    else if (item.feature == "actuator") {
      generateInformationActuator(item);
    }
  }
}

function generateInformationSensor(item) {
  let sensor = document.createElement('div');
  sensor.className = "Sensor-node";
  if (item.status[0] == false) {
    sensor.className += " Disabled";
  }
  let sensor_id = document.createElement('span');
  sensor_id.id = item.id;
  
}