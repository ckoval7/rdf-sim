<html>
<head>
  <title>RDF Sim Scenario Generator</title>
</head>
<body>
  <h1> RDF Sim</h1>
  <form>
    <div>
      Scenario Name <input type="text" name="scenarioname" id="scenarioname"><br>
      Frequency <input type="number" name="freq" id="freq"><label style="cursor: " for="freq">MHz</label><br>
    </div>
    <div style="display: inline-block; border-style: solid; border-width: 1px; padding: 5px; margin: 5px;">
      <h3>Transmitters</h3>
      <label>Transmitter</label><br>
      <input type="radio" id="stationaryTx" name="tx_type" value="stationary">
      <label for="stationaryTx">Stationary</label>&nbsp;
      <input type="radio" id="mobileTx" name="tx_type" value="mobile">
      <label for="mobileTx">Mobile</label>&nbsp;
      <input type="radio" id="gpsTx" name="tx_type" value="gps">
      <label for="gpsTx">GPS</label><br>
      <input type="button" value="New" onclick="addNewTx();">
    </div>
    <div style="display: inline-block; border-style: solid; border-width: 1px; padding: 5px; margin: 5px;">
      <h3>Receivers</h3>
      <label>Receiver</label><br>
      <input type="radio" id="stationaryRx" name="rx_type" value="stationary">
      <label for="stationaryRx">Stationary</label>&nbsp;
      <input type="radio" id="mobileRx" name="rx_type" value="mobile">
      <label for="mobileRx">Mobile</label>&nbsp;
      <input type="radio" id="gpsRx" name="rx_type" value="gps">
      <label for="gpsRx">GPS</label><br>
      <input type="button" value="New" onclick="addNewRx();">
    </div>
  </form>
</body>
