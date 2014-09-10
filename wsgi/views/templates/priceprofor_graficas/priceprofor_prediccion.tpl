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
//alert(JSON.stringify({{! modelosPrediccionList}}));
% if modelosPrediccionList != []:
	//alert("if");
	google.setOnLoadCallback(drawChart);
	function drawChart() {

/*
		var dateFormatter = new google.visualization.DateFormat({
			pattern:'yy-MM',
			//timeZone:0
		});		
 */		
		//dateFormatter.format(data,0);
		
		var data = google.visualization.arrayToDataTable({{! modelosPrediccionList}});
		
//      var options = {
//    	        width: 600,
//    	        height: 400,
//    	        legend: { position: 'top', maxLines: 3 },
//    			bar: { groupWidth: '75%' },
//    	        isStacked: true,
//    	      };
		
		//data.addColumn({type: 'string', role: 'annotation'});
		
 		var options = {
		//'is3D':true,
		title: 'MERCADO DIARIO ELECTRICO',
		//pointSize: 6,
		titleTextStyle:  {color: '#000000', fontName: 'Roboto', fontSize: '22', bold: 'true', italic: 'false'},
		width: '740',
		height: '400',
		vAxis: {
			title: 'Precio (€ / MWh)',
			textStyle:{color: '#000000', fontName: 'Roboto', fontSize: '14', bold: 'false', italic: 'true'},
	  	    titleTextStyle: {/*color:'#8253E8',*/color: '#000000', fontName: 'Roboto', fontSize: '18', bold: 'false', italic: 'false'}, /*gridlines: {color: '#00ff00', count: 6},*/
	  	    viewWindow: {min: 0},
	  	  },
	 	hAxis: {
			title: 'Dias (precision en horas)',
			showTextEvery: 24,
			//slantedText:true,
			//slantedTextAngle: 30,
			//format = 'yyyy/MM/dd HH:mm',
			//slantedTextAngle: 90,
		    //slantedText: false,
			textStyle: {color: '#000000', fontName: 'Roboto', fontSize: '14', bold: 'false', italic: 'true'},
	    	titleTextStyle: {/*color: '#8253E8',*/color: '#000000', fontName: 'Roboto', fontSize: '18', bold: 'false', italic: 'false'}, gridlines: {color: '#00ff00', count: 6}, viewWindowMode: 'pretty'},
	  		curveType: 'function',
	  		backgroundColor: {stroke: '#000000', strokeWidth: '2', /*fill: '#D1FFC6'*/},
    	    //backgroundColor: "transparent",
          	//isStacked: true,
			//bar: { groupWidth: '75%' },
    	    //legend: {position: 'none'},
			//legend: { position: 'right', maxLines: 6 },
			//legend: { position: 'right'},

			//series: {0: {type: "line"}},
    	    //series: {1: {type: "line"}},
    	    //series: {2: {type: "line"}},

    	    //series: {2: {type: "line"}, interpolateNulls: false},
 			//'colors' : ["#194D86","#699A36"],
 			//'colors' : ["black"],
    	    //'colors' : ["black","red"],
    	    //'colors' : ["black","red","blue"],
    	    //'colors' : ["black","red","grey"],
	  		//seriesType: "bars",
	  		//seriesType: "line",
			//seriesType: "bars", series: {0: {type: "line", color: "red"}}
 /*
			annotation: {
                // index here is the index of the DataTable column providing the annotation
                1: {
                    style: 'line'
                }
            }
 */
 			};

 		//interpolateNulls = true;
	  	  	% if modelosPrediccionList != [[]]:
		  		//var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
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

</head>

<body>

<!-- <div class="container"> -->
<!-- <div class="row"> -->

<br>

<form action="/TecnologiasDiarias" method="POST">
	<!-- style="margin-top:-340px;" -->
   	<div class='col-sm-6'>
       	<div class="form-group">
	        <!-- <div class='input-group date' id='datetimepicker1' data-date-format="DD/MM/YYYY"> -->
	        <div class='input-group date' id='datetimepicker1' data-date-format="DD/MM/YYYY" style="display: none;">
   		        <input type='text' name="select" class="form-control"></input>
       		        <!-- <span class="input-group-addon"><span class="glyphicon glyphicon-time"></span></span> -->
       		        <!-- <span class="input-group-addon"><span class="fa fa-calendar"></span></span> -->
       		        <span class="input-group-addon"><span class="fa fa-calendar-o"></span></span>
            </div>
        </div>
		<!-- <div>{{! fecha}}&nbsp;<br>{{! mensaje}}</div> -->
  	</div>
   	<!-- color del boton enviar -->
   	<!-- <input type="submit" class="btn btn-success"></input> -->
   	<input type="submit" value="Enviar" class="btn btn-primary" style="display: none;"></input>
		<!-- se comenta la fecha hasta que se pueda seleccionar un dayahead determinado -->
		<!-- <div><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{! fecha}} -->
		<div><br>
		%if mensaje:
			&nbsp;&nbsp;&nbsp;&nbsp;{{! mensaje}}
		%end
	<!-- para que la fecha quede pegada al grafico -->
	<!-- 	</div> -->
</form>

	<div id="chart_div" style="width: 800px; height: 400px;"></div>

	% from datetime import datetime, timedelta
	% from time import time
	<!-- alert({{datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')}}) -->

	% # print fecha
	% if fecha:
		% # si la hora local son las 14:00 entonces la hora en el servidor son 6 horas menos
	    % hora = 8
		% from datetime import datetime, timedelta
		% fechaDT = datetime.strptime(fecha, '%d/%m/%Y')
		% currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
	
		% indice = 0
		% if datetime.now().hour >= hora:
			    <form action="/TecnologiasDiarias" method="POST">
			    <!-- <form action="/PreciosDiarios" method="POST"> -->
	
			% if fechaDT == currentDate:
				% indice = 1
				% fechaDT2 = fechaDT - timedelta(3)
				% fecha2 = fechaDT2.strftime('%d/%m/%Y')
				% textofecha =  str(fecha2)
				% textoboton = 'HOY'
				% mensaje2 = ''
			% elif fechaDT == currentDate - timedelta(1):
				% indice = 2
				% fechaDT2 = fechaDT - timedelta(2)
				% fecha2 = fechaDT2.strftime('%d/%m/%Y')
				% textofecha =  str(fecha2)
				% textoboton = 'HOY'
				% mensaje2 = ''
			% elif fechaDT == currentDate - timedelta(2):
				% indice = 3
				% fechaDT2 = fechaDT - timedelta(1)
				% fecha2 = fechaDT2.strftime('%d/%m/%Y')
				% textofecha =  str(fecha2)
				% textoboton = 'HOY'
				% mensaje2 = ''
			% end
		
			% if indice == 1:
			    % whatTime = fechaDT - timedelta(3)
			% elif indice == 2:
				% whatTime = fechaDT - timedelta(2)
			% elif indice == 3:
				% whatTime = fechaDT - timedelta(1)
		    % end
	
			% if indice != 0:
				<br>
			    % whatString = whatTime.strftime('%d/%m/%Y')
			    <input type="text" name="select" value={{whatString}} hidden></input>

				<!-- comentar estas lineas mientras no halla datos del dia de mañana -->
			    <!-- &nbsp;&nbsp;&nbsp;&nbsp;<input type="submit" value={{textoboton}} hidden> -->
			    &nbsp;&nbsp;&nbsp;&nbsp;<input type="submit" class="btn btn-primary" value={{textoboton}} hidden></input>
				<br>&nbsp;&nbsp;&nbsp;&nbsp;{{textofecha}}
			    &nbsp;&nbsp;&nbsp;&nbsp;{{ mensaje2}}
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
