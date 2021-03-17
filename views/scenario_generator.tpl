<html>
<head>
  <title>RDF Sim Scenario Generator</title>
  <link rel="icon"
      type="image/png"
      href="/static/fox.png">
  <link rel="stylesheet" type="text/css" href="/static/style.css">
  <script src="/static/scenariogen.js"></script>
</head>
<body onload="loadPage();">
  <h1> RDF Sim</h1>
  <div class="event_div">
    <form name="rdfEvent">
      <span class="field_labels">Event Name </span>
      <input onfocusout="dfEvent.name = this.value;" required type="text" name="eventname" id="eventname"><br>
      <hr>
      <div class="scenario_div">
        <div id="globals">
          <span class="field_labels">Scenario Name </span>
          <input onfocusout="scenario.name = this.value;" required type="text" name="scenarioname" id="scenarioname"><br>
          <span class="field_labels">Frequency </span>
          <input onfocusout="scenario.frequency = this.value;" required type="number" name="freq" id="freq">
          <label for="freq">MHz</label><br>
        </div><br>
        <div id="tx_card" class="cards">
          <h3>Transmitters</h3>
          <input onclick="scenario.txOrder = 'round_robin';" type="radio" id="round_robin" name="tx_order" value="round_robin" checked>
          <label for="round_robin">Round Robin</label>&nbsp;
          <input onclick="scenario.txOrder = 'random';" type="radio" id="random" name="tx_order" value="random">
          <label for="random">Random</label>&nbsp;<br>
        </div>
        <div id="rx_card" class="cards">
          <h3>Receivers</h3>
        </div>
      </div>
    <br>
    <input type="button" value="Generate" onclick="submitJson();">
    <!-- <input type="button" value="New Scenario" onclick="addNewScenario();"> -->
  </form>
  </div>
</body>
