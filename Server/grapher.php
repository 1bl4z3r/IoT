<html>
  <head>
    <title>Untitled</title>
    <script src="plotly-latest.min.js"></script>
  </head>
  <body>
     <div id="tester" style="width:4800px;height:250px;"></div>
     <?php
     $s = file_get_contents('data.txt');
     $s = str_replace(' ', ', ', $s);
//     echo $s;
     ?>
     <script>
        var xx = [];
        for (var i = 0; i < 1000; i++)
             xx.push(i);
	TESTER = document.getElementById('tester');
	Plotly.plot( TESTER, [{
	x: xx,
	y: [<?php echo $s ?>] }], {
	margin: { t: 0 } } );
</script>
  </body>
</html>
