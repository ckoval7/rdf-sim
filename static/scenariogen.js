let transmitters = [];
let receivers = [];

function loadPage() {
  addNewTx(0);
  addNewRx(0);
  //Set up the initial TX and RX fields
}

function setEventName() {

}

function setScenarioName(id_num) {

}

function setScenarioFreq(id_num) {

}

//rx station_id
function setStationId(id_num) {
  let rx_index = receivers.findIndex(x => x.rx_id === id_num);
  let station_id = document.getElementById('rx_station_id' + id_num).value;
  receivers[rx_index].station_id = station_id;
}

//rx lat
function setRxLat(id_num) {
  let rx_index = receivers.findIndex(x => x.rx_id === id_num);
  let latitude = document.getElementById('latRx' + id_num).value;
  receivers[rx_index].latitude = latitude;
}

//rx lon
function setRxLon(id_num) {
  let rx_index = receivers.findIndex(x => x.rx_id === id_num);
  let longitude = document.getElementById('lonRx' + id_num).value;
  receivers[rx_index].longitude = longitude;
}

//rx heading
function setHeading(id_num) {
  let rx_index = receivers.findIndex(x => x.rx_id === id_num);
  let heading = document.getElementById('headingRx' + id_num).value;
  receivers[rx_index].heading = heading;
}

//rx path
function setRxPath(id_num) {
  let rx_index = receivers.findIndex(x => x.rx_id === id_num);
  let pathfile = document.getElementById('pathfile' + id_num).value;
  receivers[rx_index].pathfile = pathfile;
}

//rx speed
function setRxSpeed(id_num) {
  let rx_index = receivers.findIndex(x => x.rx_id === id_num);
  let speed = document.getElementById('speedRx' + id_num).value;
  receivers[rx_index].speed = speed;
}

//rx client addr
function setRxGps(id_num) {
  let rx_index = receivers.findIndex(x => x.rx_id === id_num);
  let gpsAddr = document.getElementById('gpsurl' + id_num).value;
  receivers[rx_index].gpsAddr = gpsAddr;
}

// min uptime
function setMinUptime(id_num) {
  let tx_index = transmitters.findIndex(x => x.tx_id === id_num);
  let minUptime = document.getElementById('latTx' + id_num).value;
}
// max uptime
function setMaxUptime(id_num) {
  let tx_index = transmitters.findIndex(x => x.tx_id === id_num);
  let
}
// min downtime
function setMinDowntime(id_num) {
  let tx_index = transmitters.findIndex(x => x.tx_id === id_num);
  let
}
// max downtime
function setMaxDowntime(id_num) {
  let tx_index = transmitters.findIndex(x => x.tx_id === id_num);
  let
}

//tx lat
function setTxLat(id_num) {
  let tx_index = transmitters.findIndex(x => x.tx_id === id_num);
  let latitude = document.getElementById('latTx' + id_num).value;
  transmitters[tx_index].latitude = latitude;
}

//tx lon
function setTxLon(id_num) {
  let tx_index = transmitters.findIndex(x => x.tx_id === id_num);
  let longitude = document.getElementById('lonTx' + id_num).value;
  transmitters[tx_index].longitude = longitude;
}

//tx heading
function setHeading(id_num) {
  let tx_index = transmitters.findIndex(x => x.tx_id === id_num);
  let heading = document.getElementById('headingTx' + id_num).value;
  transmitters[tx_index].heading = heading;
}

//tx path
function setTxPath(id_num) {
  let tx_index = transmitters.findIndex(x => x.tx_id === id_num);
  let pathfile = document.getElementById('pathfile' + id_num).value;
  transmitters[tx_index].pathfile = pathfile;
}

//tx speed
function setTxSpeed(id_num) {
  let tx_index = transmitters.findIndex(x => x.tx_id === id_num);
  let speed = document.getElementById('speedTx' + id_num).value;
  transmitters[tx_index].speed = speed;
}

//tx client addr
function setTxGps(id_num) {
  let tx_index = transmitters.findIndex(x => x.tx_id === id_num);
  let gpsAddr = document.getElementById('gpsurl' + id_num).value;
  transmitters[tx_index].gpsAddr = gpsAddr;
}

function addNewRx(id_num) {
  receivers.push({rx_id: id_num,});
  let rx_index = receivers.length - 1;
  console.log("Receivers: " + receivers.length);
  //Add another receiver
  delElement('new_rx_button');

  const newRx = document.createElement('div');
  newRx.id = "rx" + id_num;

  const rxName = document.createElement('h4');
  rxName.innerHTML = "Receiver " + id_num;

  const basicRxItems = document.createElement('div');
  basicRxItems.id = "basicRxItems" + id_num;

  const station_id_span = document.createElement('span');
  station_id_span.className = 'field_labels';
  station_id_span.innerHTML = "Station ID: ";

  const station_id = document.createElement('input');
  station_id.id = 'rx_station_id' + id_num;
  station_id.setAttribute('onfocusout', 'setStationId('+id_num+');');

  const stationaryRx = document.createElement('input');
  stationaryRx.type = 'radio';
  stationaryRx.id = 'stationaryRx' + id_num;
  stationaryRx.name = 'rx_type' + id_num;
  stationaryRx.value = "stationary";
  stationaryRx.setAttribute('onclick', 'showStationaryRx(' + id_num + ');');

  const stationaryRxLabel = document.createElement('label');
  stationaryRxLabel.for = "stationaryRx";
  stationaryRxLabel.innerHTML = "Stationary &nbsp;";

  const mobileRx = document.createElement('input');
  mobileRx.type = 'radio';
  mobileRx.id = 'mobileRx' + id_num;
  mobileRx.name = 'rx_type' + id_num;
  mobileRx.value = "mobile";
  mobileRx.setAttribute('onclick', 'showMobileRx(' + id_num + ');');

  const mobileRxLabel = document.createElement('label');
  mobileRxLabel.for = "mobileRx";
  mobileRxLabel.innerHTML = "Mobile &nbsp;";

  const gpsRx = document.createElement('input');
  gpsRx.type = 'radio';
  gpsRx.id = 'gpsRx' + id_num;
  gpsRx.name = 'rx_type' + id_num;
  gpsRx.value = "gps";
  gpsRx.setAttribute('onclick', 'showGpsRx(' + id_num + ');');

  const gpsRxLabel = document.createElement('label');
  gpsRxLabel.for = "gpsRx";
  gpsRxLabel.innerHTML = "GPS &nbsp;";

  const newRxButton = document.createElement('input');
  newRxButton.type = 'button';
  newRxButton.id = 'new_rx_button';
  newRxButton.value = 'New';
  newRxButton.setAttribute('onclick', 'addNewRx('+(id_num + 1)+');');

  const delRxButton = document.createElement('input');
  delRxButton.type = 'button';
  delRxButton.id = 'del_rx_button';
  delRxButton.value = 'Delete';
  // delRxButton.style.float = 'right';
  delRxButton.setAttribute('onclick', 'delRx(' + id_num + ');');

  rx = document.getElementById('rx_card');
  rx.appendChild(newRx);
  newRx.appendChild(rxName);
  newRx.appendChild(delRxButton);
  newRx.appendChild(basicRxItems);
  // new_button = document.getElementById('new_rx_button');
  // rx.insertBefore(basicRxItems, new_button);

  basicRxItems.appendChild(station_id_span);
  basicRxItems.appendChild(station_id);
  basicRxItems.appendChild(document.createElement('br'));
  basicRxItems.appendChild(stationaryRx);
  basicRxItems.appendChild(stationaryRxLabel);
  basicRxItems.appendChild(mobileRx);
  basicRxItems.appendChild(mobileRxLabel);
  basicRxItems.appendChild(gpsRx);
  basicRxItems.appendChild(gpsRxLabel);
  basicRxItems.appendChild(document.createElement('br'));

  const rxhr = document.createElement('hr');
  rxhr.id = 'rxhr' + id_num;
  rx.appendChild(rxhr);
  rx.appendChild(newRxButton);
  basicRxItems.appendChild(document.createElement('br'));
}

function addNewTx(id_num) {
  transmitters.push({tx_id: id_num,});
  console.log("Transmitters: " + transmitters.length);

  delElement('new_tx_button');

  const newTx = document.createElement('div');
  newTx.id = "tx" + id_num;

  const txName = document.createElement('h4');
  txName.innerHTML = "Transmitter " + id_num;

  const basicTxItems = document.createElement('div');
  basicTxItems.id = "basicTxItems" + id_num;

  const uptimeMinSpan = document.createElement('span');
  uptimeMinSpan.className = 'field_labels';
  uptimeMinSpan.innerHTML = "Min Uptime: ";

  const uptimeMinInput = document.createElement('input');
  uptimeMinInput.type = 'number';
  uptimeMinInput.id = 'tx-minUptime' + id_num;

  const uptimeMaxSpan = document.createElement('span');
  uptimeMaxSpan.className = 'field_labels';
  uptimeMaxSpan.innerHTML = "Max Uptime: ";

  const uptimeMaxInput = document.createElement('input');
  uptimeMaxInput.type = 'number';
  uptimeMaxInput.id = 'tx-maxUptime' + id_num;

  const downtimeMinSpan = document.createElement('span');
  downtimeMinSpan.className = 'field_labels';
  downtimeMinSpan.innerHTML = "Min Downtime: ";

  const downtimeMinInput = document.createElement('input');
  downtimeMinInput.type = 'number';
  downtimeMinInput.id = 'tx-minDowntime' + id_num;

  const downtimeMaxSpan = document.createElement('span');
  downtimeMaxSpan.className = 'field_labels';
  downtimeMaxSpan.innerHTML = "Max Downtime: ";

  const downtimeMaxInput = document.createElement('input');
  downtimeMaxInput.type = 'number';
  downtimeMaxInput.id = 'tx-maxDowntime' + id_num;

  const stationaryTx = document.createElement('input');
  stationaryTx.type = 'radio';
  stationaryTx.id = 'stationaryTx' + id_num;
  stationaryTx.name = 'tx' + id_num + '_type';
  stationaryTx.value = "stationary";
  stationaryTx.setAttribute('onclick', 'showStationaryTx(' + id_num + ');');

  const stationaryTxLabel = document.createElement('label');
  stationaryTxLabel.for = "stationaryTx";
  stationaryTxLabel.innerHTML = "Stationary &nbsp;";

  const mobileTx = document.createElement('input');
  mobileTx.type = 'radio';
  mobileTx.id = 'mobileTx' + id_num;
  mobileTx.name = 'tx' + id_num + '_type';
  mobileTx.value = "mobile";
  mobileTx.setAttribute('onclick', 'showMobileTx(' + id_num + ');');

  const mobileTxLabel = document.createElement('label');
  mobileTxLabel.for = "mobileTx";
  mobileTxLabel.innerHTML = "Mobile &nbsp;";

  const gpsTx = document.createElement('input');
  gpsTx.type = 'radio';
  gpsTx.id = 'gpsTx' + id_num;
  gpsTx.name = 'tx' + id_num + '_type';
  gpsTx.value = "gps";
  gpsTx.setAttribute('onclick', 'showGpsTx(' + id_num + ');');

  const gpsTxLabel = document.createElement('label');
  gpsTxLabel.for = "gpsTx";
  gpsTxLabel.innerHTML = "GPS &nbsp;";

  const newTxButton = document.createElement('input');
  newTxButton.type = 'button';
  newTxButton.id = 'new_tx_button';
  newTxButton.value = 'New';
  newTxButton.setAttribute('onclick', 'addNewTx('+(id_num + 1)+');');

  const delTxButton = document.createElement('input');
  delTxButton.type = 'button';
  delTxButton.id = 'del_tx_button';
  delTxButton.value = 'Delete';
  // delTxButton.style.float = 'right';
  delTxButton.setAttribute('onclick', 'delTx(' + id_num + ');');

  tx = document.getElementById('tx_card');
  tx.appendChild(newTx);
  newTx.appendChild(txName);
  newTx.appendChild(delTxButton);
  newTx.appendChild(basicTxItems);
  // new_button = document.getElementById('new_tx_button');
  // tx.insertBefore(basicTxItems, new_button);

  basicTxItems.appendChild(uptimeMinSpan);
  basicTxItems.appendChild(uptimeMinInput);
  basicTxItems.appendChild(document.createElement('br'));
  basicTxItems.appendChild(uptimeMaxSpan);
  basicTxItems.appendChild(uptimeMaxInput);
  basicTxItems.appendChild(document.createElement('br'));
  basicTxItems.appendChild(downtimeMinSpan);
  basicTxItems.appendChild(downtimeMinInput);
  basicTxItems.appendChild(document.createElement('br'));
  basicTxItems.appendChild(downtimeMaxSpan);
  basicTxItems.appendChild(downtimeMaxInput);
  basicTxItems.appendChild(document.createElement('br'));
  basicTxItems.appendChild(stationaryTx);
  basicTxItems.appendChild(stationaryTxLabel);
  basicTxItems.appendChild(mobileTx);
  basicTxItems.appendChild(mobileTxLabel);
  basicTxItems.appendChild(gpsTx);
  basicTxItems.appendChild(gpsTxLabel);
  basicTxItems.appendChild(document.createElement('br'));

  const txhr = document.createElement('hr');
  txhr.id = 'txhr' + id_num;
  tx.appendChild(txhr);
  tx.appendChild(newTxButton);
  basicTxItems.appendChild(document.createElement('br'));
  //Add another transmitter
}

function addNewScenario() {
  console.log("New Scenario Test");
}

function showStationaryTx(id_num) {
  //Fields for stationary tx
  console.log("Stationary TX Test");
  delElement('specialTxItems' + id_num);
  const specialTx = document.createElement('div');
  specialTx.id = "specialTxItems" + id_num;

  const latInput = document.createElement('input');
  latInput.id = 'latTx' + id_num;

  const latspan = document.createElement('span');
  latspan.className = "field_labels";
  latspan.innerHTML = "Latitude: ";

  const lonInput = document.createElement('input');
  lonInput.id = 'lonTx' + id_num;

  const lonspan = document.createElement('span');
  lonspan.className = "field_labels";
  lonspan.innerHTML = "Longitude: ";


  tx = document.getElementById('tx' + id_num);
  tx.append(specialTx);
  // tx.insertBefore(specialTx, document.getElementById('del_tx_button'));

  specialTx.appendChild(latspan);
  specialTx.appendChild(latInput);
  specialTx.appendChild(document.createElement('br'));
  specialTx.appendChild(lonspan);
  specialTx.appendChild(lonInput);
  specialTx.appendChild(document.createElement('br'));
}

function showMobileTx(id_num) {
  //Fields for mobile tx
  console.log("Mobile TX Test");

  delElement('specialTxItems' + id_num);
  const specialTx = document.createElement('div');
  specialTx.id = "specialTxItems" + id_num;

  const pathfile = document.createElement('input');
  // pathfile.type = "file";
  pathfile.id = 'pathfile' + id_num;

  const pathspan = document.createElement('span');
  pathspan.className = "field_labels";
  pathspan.innerHTML = "Path File: ";

  const speedInput = document.createElement('input');
  speedInput.id = 'speedtx' + id_num;
  speedInput.type = "number";

  const speedSpan = document.createElement('span');
  speedSpan.className = "field_labels";
  speedSpan.innerHTML = "Speed: ";


  tx = document.getElementById('tx' + id_num);
  tx.append(specialTx);
  // tx.insertBefore(specialTx, document.getElementById('del_tx_button'));

  specialTx.appendChild(pathspan);
  specialTx.appendChild(pathfile);
  specialTx.appendChild(document.createElement('br'));
  specialTx.appendChild(speedSpan);
  specialTx.appendChild(speedInput);
  specialTx.appendChild(document.createElement('br'));
}

function showGpsTx(id_num) {
  //Fields for GPS tx
  console.log("GPS TX Test");

  delElement('specialTxItems' + id_num);
  const specialTx = document.createElement('div');
  specialTx.id = "specialTxItems" + id_num;

  const gpsurl = document.createElement('input');
  // pathfile.type = "file";
  gpsurl.id = 'gpsurl' + id_num;

  const gpsurlspan = document.createElement('span');
  gpsurlspan.className = "field_labels";
  gpsurlspan.innerHTML = "GPS Client: ";

  tx = document.getElementById('tx' + id_num);
  tx.append(specialTx);
  // tx.insertBefore(specialTx, document.getElementById('del_tx_button'));

  specialTx.appendChild(gpsurlspan);
  specialTx.appendChild(gpsurl);
  specialTx.appendChild(document.createElement('br'));
}

function showStationaryRx(id_num) {
  //Fields for stationary rx
  console.log("Stationary RX Test");

  let rx_index = receivers.findIndex(x => x.rx_id === id_num);
  receivers[rx_index].rx_type = "stationary";

  delElement('specialRxItems' + id_num);
  const specialRx = document.createElement('div');
  specialRx.id = "specialRxItems" + id_num;

  const latInput = document.createElement('input');
  latInput.id = 'latRx' + id_num;
  latInput.setAttribute('onfocusout', 'setRxLat(' + id_num + ');');

  const latspan = document.createElement('span');
  latspan.className = "field_labels";
  latspan.innerHTML = "Latitude: ";

  const lonInput = document.createElement('input');
  lonInput.id = 'lonRx' + id_num;
  lonInput.setAttribute('onfocusout', 'setRxLon(' + id_num + ');');

  const lonspan = document.createElement('span');
  lonspan.className = "field_labels";
  lonspan.innerHTML = "Longitude: ";

  const headingInput = document.createElement('input');
  headingInput.id = 'headingRx' + id_num;
  headingInput.setAttribute('onfocusout', 'setHeading(' + id_num + ');');

  const headingspan = document.createElement('span');
  headingspan.className = "field_labels";
  headingspan.innerHTML = "Heading: ";

  rx = document.getElementById('rx' + id_num);
  rx.append(specialRx);
  // rx.insertBefore(specialRx, document.getElementById('del_rx_button'));

  specialRx.appendChild(latspan);
  specialRx.appendChild(latInput);
  specialRx.appendChild(document.createElement('br'));
  specialRx.appendChild(lonspan);
  specialRx.appendChild(lonInput);
  specialRx.appendChild(document.createElement('br'));
  specialRx.appendChild(headingspan);
  specialRx.appendChild(headingInput);
  specialRx.appendChild(document.createElement('br'));
}

function showMobileRx(id_num) {
  //Fields for mobile rx
  console.log("Mobile RX Test");
  let rx_index = receivers.findIndex(x => x.rx_id === id_num);
  receivers[rx_index].rx_type = "mobile";

  delElement('specialRxItems' + id_num);
  const specialRx = document.createElement('div');
  specialRx.id = "specialRxItems" + id_num;

  const pathfile = document.createElement('input');
  pathfile.id = 'pathfile' + id_num;
  pathfile.setAttribute('onfocusout', 'setRxPath(' + id_num + ');');

  const pathspan = document.createElement('span');
  pathspan.className = "field_labels";
  pathspan.innerHTML = "Path File: ";

  const speedInput = document.createElement('input');
  speedInput.id = 'speedRx' + id_num;
  speedInput.type = "number";
  speedInput.setAttribute('onfocusout', 'setRxSpeed(' + id_num + ');');

  const speedSpan = document.createElement('span');
  speedSpan.className = "field_labels";
  speedSpan.innerHTML = "Speed: ";


  rx = document.getElementById('rx' + id_num);
  rx.append(specialRx);
  // rx.insertBefore(specialRx, document.getElementById('del_rx_button'));

  specialRx.appendChild(pathspan);
  specialRx.appendChild(pathfile);
  specialRx.appendChild(document.createElement('br'));
  specialRx.appendChild(speedSpan);
  specialRx.appendChild(speedInput);
  specialRx.appendChild(document.createElement('br'));
}

function showGpsRx(id_num) {
  //Fields for GPS rx
  console.log("GPS RX Test");

  let rx_index = receivers.findIndex(x => x.rx_id === id_num);
  receivers[rx_index].rx_type = "gps";

  delElement('specialRxItems' + id_num);
  const specialRx = document.createElement('div');
  specialRx.id = "specialRxItems" + id_num;

  const gpsurl = document.createElement('input');
  gpsurl.id = 'gpsurl' + id_num;
  gpsurl.setAttribute('onfocusout', 'setRxGps(' + id_num + ');');

  const gpsurlspan = document.createElement('span');
  gpsurlspan.className = "field_labels";
  gpsurlspan.innerHTML = "GPS Client: ";

  rx = document.getElementById('rx' + id_num);
  rx.append(specialRx);
  // rx.insertBefore(specialRx, document.getElementById('del_rx_button'));

  specialRx.appendChild(gpsurlspan);
  specialRx.appendChild(gpsurl);
  specialRx.appendChild(document.createElement('br'));
}

function delRx(id_num) {
  let rx_index = receivers.findIndex(x => x.rx_id === id_num);
  receivers.splice(rx_index, 1);
  delElement('rx' + id_num);
  delElement('rxhr' + id_num);
  console.log("Deleting rx " + id_num + " at index " + rx_index);
}

function delTx(id_num) {
  let tx_index = transmitters.findIndex(x => x.tx_id === id_num);
  transmitters.splice(tx_index, 1);
  delElement('tx' + id_num);
  delElement('txhr' + id_num);
  console.log("Deleting tx " + id_num + " at index " + tx_index);
}

function delElement(deleteMe) {
  //Delete a RX or TX
  if (document.contains(document.getElementById(deleteMe))) {
    document.getElementById(deleteMe).remove();
  } else {
    console.log('Can\'t Delete invalid ID: ' + deleteMe);
  }
}

function submitJson() {
  //Send the info to the backend
}
