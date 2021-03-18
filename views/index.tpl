<html>
<head>
  <link rel="icon"
      type="image/png"
      href="/static/fox.png">
  <link rel="stylesheet" type="text/css" href="/static/style.css">
</head>
<body>
  <div class="header">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="http://dfsim.net">dfsim.net</a></li>
    <li style="float:right"><a target="_blank" href="https://github.com/ckoval7/rdf-sim">GitHub</a></li>
  </ul>
  </div>
  <h3>Test transmitter 1:</h3>
  <p>Single mobile transmitter with a regular TX cycle of one minute active, three minutes idle.</p>
  <h3>RDF Receivers:</h3>
  % for id in rx_ids:
  <h4>Station {{id}}:</h4>
  <ul>
    <li><a href="{{id}}.xml">XML Data</a></li>
    <li><a href="/static/compass/compass.html?station_id={{id}}">Compass</a></li>
  </ul>
  % end

</body>
</html>
