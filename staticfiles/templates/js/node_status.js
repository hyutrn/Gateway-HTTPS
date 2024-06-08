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
  client.subscribe('nodes/actuators_modify/#', { qos: 1 }, (error) => {
    if (!error) {
      console.log('Subscribed to test topic!');
    }
    else {
      console.alert('Error subscribing a topic!');
    }
  });
  client.subscribe('nodes/authorize/#', { qos: 1 }, (error) => {
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
  message = message.toString();
  handleMessages(topic, message);
})

// Use fetch GET method to get the data from the server when web is loaded with URL: /get_data and console.log the data
window.addEventListener('load', () => {
  console.log("window loaded");
  console.log(getCookie('token'));
  console.log(getCookie('csrftoken'));
  fetch('/get_data', {
    method: 'GET',
    headers: {
      'Authorization': 'Token ' + getCookie('token'),
    },
    data: {
      'csrfmiddlewaretoken': getCookie('csrftoken')
    }
  })
    .then(response => response.json())
    .then(data => {
      data_list = data;
      generateTable(data_list);
      enableInterruptSwitch();
    });
  fetch('/auto_mode', {
    method: 'GET',
    headers: {
      'Authorization': 'Token ' + getCookie('token'),
    },
    headers: {
      'CSRF-Token': getCookie('csrftoken')
    }
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      if (data.auto_flag == true) {
        autoButton.checked = true;
      }
      else {
        autoButton.checked = false;
      }
    });
});

// Set up the event listener for the room auto button
const autoButton = document.querySelector('#automatic > input');
autoButton.addEventListener('click', () => {
  const check_button = autoButton.checked;
  console.log(check_button);
  if (check_button == true) {
    client.publish('nodes/authorize', 'True', { qos: 1 });
  }
  else {
    client.publish('nodes/authorize', 'False', { qos: 1 });
  }

});

function generateTable(data) {
  console.log("generateTable");
  for (let index = 0; index < data.length; index++) {
    const item = data[index];
    if (item.feature == "sensor") {
      generateInformationSensor(item);
    }
    else if (item.feature == "actuator") {
      generateInformationActuator(item);
    }
  }
}

function generateInformationSensor(item) {
  const sensorNode = document.createElement('div');
  sensorNode.classList.add("Sensor-node");
  if (item.status[0] == false) {
    sensorNode.classList.add("Disabled");
  }
  const sensor_id = document.createElement('span');
  sensor_id.id = item.id;
  sensor_id.textContent = `ID: ${item.id}`;
  sensorNode.appendChild(sensor_id);

  const informationDiv = document.createElement("div");
  informationDiv.classList.add("Information");


  const sensorTypes = ["Temperature1", "Temperature2", "Air-humidity1", "Air-humidity2", "Soil-moisture1", "Soil-moisture2", "Light-intensity1", "Light-intensity2"];
  for (let index = 1; index < item.status.length; index++) {
    const sensorType = document.createElement("div");
    sensorType.classList.add("Sensor-information", sensorTypes[index - 1]);
    if (item.status[index] == false || item.status[0] == false) {
      sensorType.classList.add("Disabled");
    }

    const sensorTypeTitle = document.createElement("span");
    sensorTypeTitle.textContent = `Sensor ${(index-1) % 2 + 1}:`;
    sensorType.appendChild(sensorTypeTitle);

    const valueSensor = document.createElement("div");
    valueSensor.classList.add("Value-sensor");

    const value = document.createElement("span");
    if (item.data != null && item.data[index] != null) {
      value.textContent = item.data[index];
    }
    else {
      value.textContent = 0;
    }
    valueSensor.appendChild(value);

    const img = document.createElement("img");
    img.alt = "icon";
    valueSensor.appendChild(img);
    sensorType.appendChild(valueSensor);
    informationDiv.appendChild(sensorType);
  }
  sensorNode.appendChild(informationDiv);
  const sensorTableElement = document.querySelector(".Sensor-table");
  sensorTableElement.appendChild(sensorNode);
}

function generateInformationActuator(item) {
  const actuatorNode = document.createElement('div');
  actuatorNode.classList.add("Actuator-node");
  if (item.status[0] == false) {
    actuatorNode.classList.add("Disabled");
  }
  const actuator_id = document.createElement('span');
  actuator_id.id = item.id;
  actuator_id.textContent = `ID: ${item.id}`;
  actuatorNode.appendChild(actuator_id);

  const informationDiv = document.createElement("div");
  informationDiv.classList.add("Information");

  const actuatorTypes = ["Motor1", "Motor2", "Motor3", "Motor4"];
  const actuatorName = ["Pump", "Fan", "Light", "Motor 4"];
  for (let index = 1; index < item.status.length; index++) {
    const actuatorInformation = document.createElement("div");
    actuatorInformation.classList.add("Actuator-information", actuatorTypes[index - 1]);
    if (item.status[index] == false || item.status[0] == false) {
      actuatorInformation.classList.add("Disabled");
    }
    const actuatorTypeTitle = document.createElement("span");
    actuatorTypeTitle.textContent = `${actuatorName[index - 1]}:`;
    actuatorInformation.appendChild(actuatorTypeTitle);

    const controlActuator = document.createElement("div");
    controlActuator.classList.add("Control");

    const switchControl = document.createElement("label");
    switchControl.classList.add("Switch");
    const input = document.createElement("input");
    input.type = "checkbox";
    if (item.data != null && item.data[index] != null) {
      input.checked = item.data[index];
    }
    if (item.status[index] != true || item.status[0] != true) {
      switchControl.classList.add("Disabled");
      input.disabled = true;
    }
    switchControl.appendChild(input);
    const span = document.createElement("span");
    span.classList.add("Slider", "round");
    switchControl.appendChild(span);
    controlActuator.appendChild(switchControl);
    actuatorInformation.appendChild(controlActuator);
    informationDiv.appendChild(actuatorInformation);
  }
  actuatorNode.appendChild(informationDiv);
  const actuatorTableElement = document.querySelector(".Actuators-table");
  actuatorTableElement.appendChild(actuatorNode);
}

function handleMessages(topic, message) {
  if (topic.includes("nodes/authorize")) {
    if (message == "True") {
      autoButton.checked = true;
    }
    else {
      autoButton.checked = false;
    }
  }
  // nodes/sensors/#
  else if (topic.includes("nodes/sensors")) {
    const sensor_id = topic.split("/")[2];
    handleSensorData(sensor_id, message);
  }
  else if (topic.includes("nodes/actuators_modify")) {
    const actuator_id = topic.split("/")[2];
    handleActuatorData(actuator_id, message);
  }
  enableInterruptSwitch();
}

function handleSensorData(sensor_id, message) {
  const sensorNode = document.querySelector(`.Sensor-node [id='${sensor_id}']`).parentNode;
  // Convert message to JSON
  if (message == "offline") {
    sensorNode.classList.add("Disabled");
    const sensorInformation = sensorNode.querySelectorAll(".Sensor-information");
    sensorInformation.forEach(element => {
      element.classList.add("Disabled");
    });
    return;
  }
  message = JSON.parse(message);
  console.log(message);
  const css_class = ["Temperature1", "Temperature2", "Air-humidity1", "Air-humidity2", "Soil-moisture1", "Soil-moisture2", "Light-intensity1", "Light-intensity2"];
  const key_list = ["air_temperature_1", "air_temperature_2", "air_humidity_1", "air_humidity_2", "soil_moisture_1", "soil_moisture_2", "light_intensity_1", "light_intensity_2"];
  const sensorInformation = sensorNode.querySelectorAll(".Sensor-information");
  for (let index = 0; index < css_class.length; index++) {
    if (message[key_list[index]] != null) {
      sensorInformation[index].classList.remove("Disabled");
      sensorInformation[index].querySelector(".Value-sensor > span").textContent = message[key_list[index]];
    }
    else {
      sensorInformation[index].classList.add("Disabled");
    }
  }
  sensorNode.classList.remove("Disabled");
}

function handleActuatorData(actuator_id, message) {
  console.log(actuator_id);
  const actuatorNode = document.querySelector(`.Actuator-node [id='${actuator_id}']`).parentNode;
  // Convert message to JSON
  if (message == "offline") {
    actuatorNode.classList.add("Disabled");
    const actuatorInformation = actuatorNode.querySelectorAll(".Actuator-information");
    actuatorInformation.forEach(element => {
      element.classList.add("Disabled");
      element.querySelector(".Control > label").classList.add("Disabled");
      element.querySelector(".Control > label > input").disabled = true;
    });
    return;
  }
  message = JSON.parse(message);
  console.log(message);
  const css_class = ["Motor1", "Motor2", "Motor3", "Motor4"];
  const key_list = ["motor_1", "motor_2", "motor_3", "motor_4"];
  const actuatorInformation = actuatorNode.querySelectorAll(".Actuator-information");
  for (let index = 0; index < css_class.length; index++) {
    if (message[key_list[index]] != null) {
      actuatorInformation[index].classList.remove("Disabled");
      actuatorInformation[index].querySelector(".Control > label").classList.remove("Disabled");
      actuatorInformation[index].querySelector(".Control > label > input").disabled = false;
      actuatorInformation[index].querySelector(".Control > label > input").checked = message[key_list[index]];
    }
    else {
      actuatorInformation[index].classList.add("Disabled");
    }
  }
  actuatorNode.classList.remove("Disabled");


}

function enableInterruptSwitch() {
  const switchControl = document.querySelectorAll(".Switch > input");
  switchControl.forEach(element => {
    element.addEventListener('click', () => {
      const actuator_id = element.parentNode.parentNode.parentNode.parentNode.parentNode.querySelector("span").id;
      const actuator_information = element.parentNode.parentNode.parentNode.parentNode.parentNode.querySelectorAll(".Actuator-information");
      const css_class = ["Motor1", "Motor2", "Motor3", "Motor4"];
      const key_list = ["motor_1", "motor_2", "motor_3", "motor_4"];
      let message_send = {};
      for (let index = 0; index < css_class.length; index++) {
        const actuator = actuator_information[index];
        const data = actuator.querySelector("input").checked;
        message_send[key_list[index]] = data;
      }
      console.log(message_send);
      client.publish(`nodes/actuators/${actuator_id}`, JSON.stringify(message_send), { qos: 1 });
    });
  });
}