<html>

<meta charset=utf-8>

<head>
<script type="text/javascript" src="/resources/js/jquery.js"></script>
<script type="text/javascript" src="/resources/js/moment.js"></script>
<script type="text/javascript" src="/resources/js/bootstrap.js"></script>
<script type="text/javascript" src="/resources/js/datetimepicker.js"></script>
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<link rel="stylesheet" href="/resources/css/bootstrap.css"/>
<link rel="stylesheet" href="/resources/css/datetimepicker.css"/>

<script type="text/javascript">
google.load("visualization", "1", {packages:["corechart"]});
//alert(JSON.stringify({{! preciosList}}));
% if preciosList != []:
	//alert("if");
	google.setOnLoadCallback(drawChart);
	function drawChart() {
		var data = google.visualization.arrayToDataTable({{! preciosList}});
		var options = {
		//'is3D':true,
		title: 'MERCADO DIARIO ELECTRICO',
		pointSize: 6,
		titleTextStyle:  {color: '#000000', fontName: 'Roboto', fontSize: '22', bold: 'true', italic: 'false'},
		width: '800', 
		height: '400',
		vAxis: {
			title: 'Precio (€ / MWh)',
			textStyle:{color: '#000000', fontName: 'Roboto', fontSize: '14', bold: 'false', italic: 'true'},
	  	    titleTextStyle: {/*color:'#8253E8',*/color: '#000000', fontName: 'Roboto', fontSize: '18', bold: 'false', italic: 'false'}, /*gridlines: {color: '#00ff00', count: 6},*/
	  	    viewWindow: {min: 0}},
	 	hAxis: {
			title: 'Hora del dia (h)',
			//slantedTextAngle: 90,
		    //slantedText: false,
			textStyle: {color: '#000000', fontName: 'Roboto', fontSize: '14', bold: 'false', italic: 'true'},
	    	titleTextStyle: {/*color: '#8253E8',*/color: '#000000', fontName: 'Roboto', fontSize: '18', bold: 'false', italic: 'false'}, gridlines: {color: '#00ff00', count: 6}, viewWindowMode: 'pretty'},
	  		curveType: 'function',
	  		//colors: ['#8253E8'],
	  		//colors: ['blue'],
	  		backgroundColor: {stroke: '#000000', strokeWidth: '2', /*fill: '#D1FFC6'*/},
	  		legend: {position: 'none'},
	  		//seriesType: "line",
	  		seriesType: "bars",
            //series: {3: {type: "bars"}
	  		};
  	% if preciosList != [[]]:
  		/* var chart = new google.visualization.LineChart(document.getElementById('chart_div')); */
  		var chart = new google.visualization.ComboChart(document.getElementById('chart_div'));
		chart.draw(data, options);
	% end
	}
% end
</script>

<script type="text/javascript">
$(function(){$('#datetimepicker1').datetimepicker({pickTime: false});});
</script>

<!-- <title>Morris.js Donut Chart Example</title> -->
<script src="http://cdnjs.cloudflare.com/ajax/libs/raphael/2.1.0/raphael-min.js"></script>
<script src="http://cdn.oesmith.co.uk/morris-0.4.1.min.js"></script>

% if minMax[1]:
<!-- MAXIMO -->
<script type="text/javascript">
/* Play with this code and it'll update in the panel opposite. Why not try some of the options above? */
$(document).ready(function() {
Morris.Donut({
	element: 'donut-example',
  	data: [ {label: "Precio MAX", value: {{minMax[1]}} },
			//{label: "Hora del dia", value: {{minMax[3]}} }
		  ],
	//colors: ['#4B610B','#4B610B']
    colors: ['#FF0000','#FF0000']
	//colors: ['#DF0101','#DF0101']
});
});
</script>
% end

% if minMax[0]:
<!-- MINIMO -->
<script type="text/javascript">
/* Play with this code and it'll update in the panel opposite. Why not try some of the options above? */
$(document).ready(function() {
Morris.Donut({
	element: 'donut-example2',
  	data: [ {label: "Precio MIN", value: {{minMax[0]}} },
			//{label: "Hora del dia", value: {{minMax[2]}} }
		  ],
	//colors: ['#74DF00','#74DF00']
	//colors: ['#A5DF00','#A5DF00']
	colors: ['#86B404','#86B404']
});
});
</script>
% end

</head>

<body>

<!-- <div class="container"> -->
<!-- <div class="row"> -->

<br>

<form action="/PreciosDiarios" method="POST">
	<!-- style="margin-top:-340px;" -->
   	<div class='col-sm-6'>
       	<div class="form-group">
	        <!-- <div class='input-group date' id='datetimepicker1' data-date-format="DD/MM/YYYY"> -->
	        <div class='input-group date' id='datetimepicker1' data-date-format="DD/MM/YYYY">
   		        <input type='text' name="select" class="form-control"></input>
       		        <span class="input-group-addon"><span class="glyphicon glyphicon-time"></span></span>
            </div>
        </div>
		<!-- <div>{{! fecha}}&nbsp;<br>{{! mensaje}}</div> -->
  	</div>
   	<!-- color del boton enviar -->
   	<!-- <input type="submit" class="btn btn-success"></input> -->
   	<input type="submit" class="btn btn-primary"></input>
		<div><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{! fecha}}
		%if mensaje:
			&nbsp;&nbsp;&nbsp;&nbsp;{{! mensaje}}
		%end
	<!-- para que la fecha quede pegada al grafico -->
	<!-- 	</div> -->
</form>

	<div id="chart_div" style="width: 800px; height: 400px;"></div>

	% # print fecha
	% if fecha:
		% # hora = 8
		% # hora = 15
	    % hora = 14
		% from datetime import datetime, timedelta
		% fechaDT = datetime.strptime(fecha, '%d/%m/%Y')
		% currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
		% ONEDAY = timedelta(1)
	
		% indice = 0
		% if datetime.now().hour >= hora:
			    <form action="/PreciosDiarios" method="POST">
	
			% if fechaDT == currentDate:
				% indice = 1
				% fechaDT2 = fechaDT + ONEDAY
				% fecha2 = fechaDT2.strftime('%d/%m/%Y')
				% textofecha = str(fecha2)
				% textoboton = 'MAÑANA'
				<!-- % mensaje2 = 'precios disponibles a partir de las 15:00 horas' -->
				% mensaje2 = ''
			% elif fechaDT == currentDate + ONEDAY:
				% indice = 2
				% fechaDT2 = fechaDT - ONEDAY
				% fecha2 = fechaDT2.strftime('%d/%m/%Y')
				% textofecha =  str(fecha2)
				% textoboton = 'HOY'
				% mensaje2 = ''
			% end
		
			% if indice == 1:
			    % whatTime = fechaDT + ONEDAY
			    % indice = 2
			% elif indice == 2:
				% whatTime = fechaDT - ONEDAY
			    % indice = 1
		    % end
	
			% if indice != 0:
				<br>
			    % whatString = whatTime.strftime('%d/%m/%Y')
			    <input type="text" name="select" value={{whatString}} hidden></input>
			    &nbsp;&nbsp;&nbsp;&nbsp;<input type="submit" value={{textoboton}}>
				<br>&nbsp;&nbsp;&nbsp;&nbsp;{{textofecha}}
			    &nbsp;&nbsp;&nbsp;&nbsp;{{ mensaje2}}
			    </input>
			    </form>
			% end

		% end

		% if fechaDT:
			% if (fechaDT == currentDate or fechaDT == currentDate + timedelta(1)) and (indice != 0):
				<div id="donut-example" style="width:180px; margin: -570px 0 0 825px;"></div>
				<div id="donut-example2" style="width:180px; margin: -100px 0 0 825px;"></div>
			% else:
				<div id="donut-example" style="width:180px; margin: -490px 0 0 825px;"></div>
				<div id="donut-example2" style="width:180px; margin: -100px 0 0 825px;"></div>
			% end
		% end

	% end

</body>

</html>
