
<html lang="en-gb" dir="ltr" class="uk-notouch">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
	<!-- <title>Price Profor rest API for the mobile app.</title> -->
    <link rel="shortcut icon" href="images/favicon.ico" type="image/x-icon">
    <link rel="apple-touch-icon-precomposed" href="images/apple-touch-icon.png">
    <link rel="stylesheet" href="/uikit/css/uikit.css">
    <link rel="stylesheet" href="/uikit/css/uikit.almost-flat.css">
    <link rel="stylesheet" href="http://cdn.datatables.net/1.10.1/css/jquery.dataTables.css"/>
    <script src="/js/jquery.js"></script>
    <script src="/uikit/js/uikit.min.js"></script>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
	<script type="text/javascript" src="http://cdn.datatables.net/1.10.1/js/jquery.dataTables.min.js"></script>
</head>

% from datetime import datetime, timedelta, date
% pricesDT = datetime(pricesDT.year, pricesDT.month, pricesDT.day)

<style>

    .uk-panel-boxshadow-fecha {
/*
   	-webkit-box-shadow: inset 0px 0px 0px 5px #0099c6;
	-moz-box-shadow:    inset 0px 0px 0px 5px #0099c6;
	box-shadow:         inset 0px 0px 0px 5px #0099c6;
*/
   	-webkit-box-shadow: 0px 0px 0px 5px #3366cc;
	-moz-box-shadow:    0px 0px 0px 5px #3366cc;
	box-shadow:         0px 0px 0px 5px #3366cc;
 	}

/*
    .uk-panel-boxshadow-fecha {
   	-webkit-box-shadow: 0px 0px 0px 5px #0099c6;
	-moz-box-shadow:    0px 0px 0px 5px #0099c6;
	box-shadow:         0px 0px 0px 5px #0099c6;
 	}
*/

    .uk-panel-boxshadow-minimo {
   	-webkit-box-shadow: 0px 0px 0px 5px #109618;
	-moz-box-shadow:    0px 0px 0px 5px #109618;
	box-shadow:         0px 0px 0px 5px #109618;
 	}

    .uk-panel-boxshadow-medio {
  	-webkit-box-shadow: 0px 0px 0px 5px #f1ca3a;
	-moz-box-shadow:    0px 0px 0px 5px #f1ca3a;
	box-shadow:         0px 0px 0px 5px #f1ca3a;
 	}

    .uk-panel-boxshadow-maximo {
  	-webkit-box-shadow: 0px 0px 0px 5px #dc3912;
	-moz-box-shadow:    0px 0px 0px 5px #dc3912;
	box-shadow:         0px 0px 0px 5px #dc3912;
 	}

    .uk-panel-border-radius {
  	-webkit-border-radius: 2.5px;
	-moz-border-radius:    2.5px;
	border-radius:         2.5px;
 	}

</style>

<body>
	<br></br>
	<!-- <div class="uk-container uk-container-center"> -->
 	<div class="uk-container">
	<!-- <div class="uk-grid uk-vertical-align-middle" data-uk-grid-margin="" data-uk-grid-match="{row: false}"> -->
			<!-- <div class="uk-width-medium-1-1" style="min-height: 85px;"> -->
			<div class="uk-width-medium-1-1">
			    <div class="uk-panel uk-panel-boxshadow-fecha uk-text-center uk-panel-border-radius">
			    <h3 class="" style="color:#3366cc;background-color:white;padding:10px;">
				    <b>
				    FECHA &nbsp;{{str(date.strftime(pricesDT,'%d/%m/%Y'))}}
				    </b>
			    </h3>
			    </div>
			</div>
	<br></br>
			<div class="uk-width-medium-1-1" >
				<!-- <div class="uk-panel uk-panel-box"> -->
				<div class="uk-panel">
					<div id="chart_div_prices" style="height: 400px;"></div>
					<!-- <div id="chart_div_prices" style="height: 400px; width: 1062.5px;"></div> -->
				</div>
			</div>
	<br></br>
	<!-- <div class="uk-grid uk-vertical-align-middle" data-uk-grid-margin="" data-uk-grid-match="{row: false}"> -->
	<div class="uk-grid" data-uk-grid-margin="" data-uk-grid-match="{row: false}">
			<div class="uk-width-medium-1-3" style="min-height: 100px;">
			    <div class="uk-panel uk-panel-boxshadow-minimo uk-text-center uk-panel-border-radius">
				    <h3 class="" style="color:#109618;background-color:white;padding:10px;">
				    Precio Minimo &nbsp;{{minmax[0]}} €<br>Hora {{hoursMIN}}
				    </h3>
			    </div>
			</div>
			<div class="uk-width-medium-1-3" style="min-height: 100px;">
				<!-- <div class="uk-panel uk-panel-box uk-panel-header uk-panel-box-warging uk-text-center"> -->
 			    <!-- <div class="uk-panel uk-panel-box uk-panel-box-warging uk-text-center"> -->
 			    <!-- <div class="uk-panel uk-panel-box uk-panel-boxshadow-medio uk-text-center"> -->
 			    <div class="uk-panel uk-panel-boxshadow-medio uk-text-center uk-panel-border-radius">
					<h3 class="" style="color:#f1ca3a;background-color:white;padding:10px;">
					Precio Medio &nbsp;{{meanList}} €
					</h3>
				<!-- <h3 class="uk-panel-title"> Precio Medio</h3> -->
			    </div>
			</div>
			<div class="uk-width-medium-1-3 " style="min-height: 100px;">
			    <div class="uk-panel uk-panel-boxshadow-maximo uk-text-center uk-panel-border-radius">
				    <h3 class="" style="color:#dc3912;background-color:white;padding:10px;">
				    Precio Maximo &nbsp;{{minmax[1]}} €<br>Hora {{hoursMAX}}
				    </h3>
			    </div>
			</div>
		</div>
		<!-- </div> -->
	</div>
	<br></br>
</body>

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
        //title: 'PRECIOS',
        //pointSize: 6,
        titleTextStyle:  {color: '#000000', fontName: 'Roboto', fontSize: '22', bold: 'true', italic: 'false'},
        //width: '750',
		//height: '400',
        vAxis: {
        	title: 'Precio (€ / MWh)',
        	textStyle:{color: '#000000', fontName: 'Roboto', fontSize: '14', bold: 'false', italic: 'true'},
        	titleTextStyle: {/*color:'#8253E8',*/color: '#000000', fontName: 'Roboto', fontSize: '18', bold: 'false', italic: 'false'},
        	/*gridlines: {color: '#00ff00', count: 6},*/
        	viewWindow: {min: 0},
        	},
        hAxis: {
        	title: 'Hora del dia (h)',
            //slantedTextAngle: 90,
            //slantedText: false,
            textStyle: {color: '#000000', fontName: 'Roboto', fontSize: '14', bold: 'false', italic: 'true'},
            titleTextStyle: {/*color: '#8253E8',*/color: '#000000', fontName: 'Roboto', fontSize: '18', bold: 'false', italic: 'false'},
            gridlines: {color: '#00ff00', count: 6},
            viewWindowMode: 'pretty'
            },
            curveType: 'function',
            //colors: ['#8253E8'],
            //colors: ['blue'],
            backgroundColor: {stroke: '#000000', strokeWidth: '2', /*fill: '#D1FFC6'*/},
            //legend: {position: 'none'},
            legend: { position: 'right'},
            seriesType: "bars",
			series: {1: {type: "line", color: '#f1ca3a'}}
            };
    % if preciosList != [[]]:
        var chart_pri = new google.visualization.ComboChart(document.getElementById('chart_div_prices'));
        chart_pri.draw(data, options);
    % end
    }
% end
</script>

</html>
