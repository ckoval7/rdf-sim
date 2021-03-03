<html>
<head>
  <title>RDF Sim Scenario Generator</title>
  <link rel="icon"
      type="image/png"
      href="/static/fox.png">
  <link rel="stylesheet" type="text/css" href="/static/style.css">
  <script src="/static/scenariogen.js"></script>
</head>
<body>
  <h1> RDF Sim</h1>
  <form>
    <div id="globals">
      <span class="field_labels">Scenario Name </span><input type="text" name="scenarioname" id="scenarioname"><br>
      <span class="field_labels">Frequency </span><input type="number" name="freq" id="freq"><label for="freq">MHz</label><br>
    </div>
    <div id="tx_card" class="cards">
      <h3>Transmitters</h3>
      <div id="tx0">
        <label>Transmitter</label><br>
        <input type="radio" id="stationaryTx" name="tx_type" value="stationary">
        <label for="stationaryTx">Stationary</label>&nbsp;
        <input type="radio" id="mobileTx" name="tx_type" value="mobile">
        <label for="mobileTx">Mobile</label>&nbsp;
        <input type="radio" id="gpsTx" name="tx_type" value="gps">
        <label for="gpsTx">GPS</label><br>
        <input type="button" value="New" onclick="addNewTx();">
      </div>
    </div>
    <div id="rx_card" class="cards">
      <h3>Receivers</h3>
      <div id="rx0">
        <label>Receiver</label><br>
        <input type="radio" id="stationaryRx" name="rx_type" value="stationary">
        <label for="stationaryRx">Stationary</label>&nbsp;
        <input type="radio" id="mobileRx" name="rx_type" value="mobile">
        <label for="mobileRx">Mobile</label>&nbsp;
        <input type="radio" id="gpsRx" name="rx_type" value="gps">
        <label for="gpsRx">GPS</label><br>
        <input type="button" value="New" onclick="addNewRx();">
      </div>
    </div>
  </form>
</body>
