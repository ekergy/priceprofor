
<html lang="en-gb" dir="ltr" class="uk-notouch">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
<!-- 	<title>Price Profor rest API for the mobile app.</title> -->
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
% technologyDT = datetime(technologyDT.year, technologyDT.month, technologyDT.day)

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
		<div class="uk-grid uk-vertical-align-middle" data-uk-grid-margin="" data-uk-grid-match="{row: false}">

<!--
				<div class="uk-width-medium-1-1">
				    <div class="uk-panel uk-panel-boxshadow-fecha uk-text-center uk-panel-border-radius">
				    <h3 class="" style="color:#3366cc;background-color:white;padding:10px;">
					    <b>
					    FECHA &nbsp;#{{str(date.strftime(technologyDT,'%d/%m/%Y'))}}
					    </b>
				    </h3>
				    </div>
				</div>
				<br></br>
 -->

			<div class="uk-width-medium-1-1">
				<!-- <div class="uk-panel"> -->
				<div class="uk-panel uk-panel-box">
				<!-- <table id="table_prevision" class="uk-table uk-table-hover uk-table-striped uk-table-condensed"> -->
				<!-- <table id="table_prevision" class="uk-table uk-table-condensed"> -->
				<table id="table_prevision" class="uk-table uk-table-hover">
				    <thead>
	                    <tr>
	                        <th title="Fecha">Fecha</th>
	                        <th title="Hora">Hora</th>
	                        <th title="Precio">Precio</th>
	                        <th title="Previsión Eolica">Prevision Eolica</th>
	                        <th title="Previsión Demanda">Prevision Demanda</th>
	                        <th title="Energia Gestionada" >Energia Gestionada</th>
	                    </tr>
	                </thead>
	                <tbody>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=0),'%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[1][0]}}</td>
	                        <td>{{preciosList[1][1]}} €</td>
	                        <td>{{previsionEolicaList[0]}} MWh</td>
	                        <td>{{previsionDemandaList[0]}} MWh</td>
	                        <td>{{energiaGestionadaList[0]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=1),'%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[2][0]}}</td>
	                        <td>{{preciosList[2][1]}} €</td>
	                        <td>{{previsionEolicaList[1]}} MWh</td>
	                        <td>{{previsionDemandaList[1]}} MWh</td>
	                        <td>{{energiaGestionadaList[1]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=2),'%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[3][0]}}</td>
	                        <td>{{preciosList[3][1]}} €</td>
	                        <td>{{previsionEolicaList[2]}} MWh</td>
	                        <td>{{previsionDemandaList[2]}} MWh</td>
	                        <td>{{energiaGestionadaList[2]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=3), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[4][0]}}</td>
	                        <td>{{preciosList[4][1]}} €</td>
	                        <td>{{previsionEolicaList[3]}} MWh</td>
	                        <td>{{previsionDemandaList[3]}} MWh</td>
	                        <td>{{energiaGestionadaList[3]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=4), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[5][0]}}</td>
	                        <td>{{preciosList[5][1]}} €</td>
	                        <td>{{previsionEolicaList[4]}} MWh</td>
	                        <td>{{previsionDemandaList[4]}} MWh</td>
	                        <td>{{energiaGestionadaList[4]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=5), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[6][0]}}</td>
	                        <td>{{preciosList[6][1]}} €</td>
	                        <td>{{previsionEolicaList[5]}} MWh</td>
	                        <td>{{previsionDemandaList[5]}} MWh</td>
	                        <td>{{energiaGestionadaList[5]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=6), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[7][0]}}</td>
	                        <td>{{preciosList[7][1]}} €</td>
	                        <td>{{previsionEolicaList[6]}} MWh</td>
	                        <td>{{previsionDemandaList[6]}} MWh</td>
	                        <td>{{energiaGestionadaList[6]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=7), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[8][0]}}</td>
	                        <td>{{preciosList[8][1]}} €</td>
	                        <td>{{previsionEolicaList[7]}} MWh</td>
	                        <td>{{previsionDemandaList[7]}} MWh</td>
	                        <td>{{energiaGestionadaList[7]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=8), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[9][0]}}</td>
	                        <td>{{preciosList[9][1]}} €</td>
	                        <td>{{previsionEolicaList[8]}} MWh</td>
	                        <td>{{previsionDemandaList[8]}} MWh</td>
	                        <td>{{energiaGestionadaList[8]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=9), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[10][0]}}</td>
	                        <td>{{preciosList[10][1]}} €</td>
	                        <td>{{previsionEolicaList[9]}} MWh</td>
	                        <td>{{previsionDemandaList[9]}} MWh</td>
	                        <td>{{energiaGestionadaList[9]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=10), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[11][0]}}</td>
	                        <td>{{preciosList[11][1]}} €</td>
	                        <td>{{previsionEolicaList[10]}} MWh</td>
	                        <td>{{previsionDemandaList[10]}} MWh</td>
	                        <td>{{energiaGestionadaList[10]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=11), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[12][0]}}</td>
	                        <td>{{preciosList[12][1]}} €</td>
	                        <td>{{previsionEolicaList[11]}} MWh</td>
	                        <td>{{previsionDemandaList[11]}} MWh</td>
	                        <td>{{energiaGestionadaList[11]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=12), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[13][0]}}</td>
	                        <td>{{preciosList[13][1]}} €</td>
	                        <td>{{previsionEolicaList[12]}} MWh</td>
	                        <td>{{previsionDemandaList[12]}} MWh</td>
	                        <td>{{energiaGestionadaList[12]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=13), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[14][0]}}</td>
	                        <td>{{preciosList[14][1]}} €</td>
	                        <td>{{previsionEolicaList[13]}} MWh</td>
	                        <td>{{previsionDemandaList[13]}} MWh</td>
	                        <td>{{energiaGestionadaList[13]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=14), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[15][0]}}</td>
	                        <td>{{preciosList[15][1]}} €</td>
	                        <td>{{previsionEolicaList[14]}} MWh</td>
	                        <td>{{previsionDemandaList[14]}} MWh</td>
	                        <td>{{energiaGestionadaList[14]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=15), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[16][0]}}</td>
	                        <td>{{preciosList[16][1]}} €</td>
	                        <td>{{previsionEolicaList[15]}} MWh</td>
	                        <td>{{previsionDemandaList[15]}} MWh</td>
	                        <td>{{energiaGestionadaList[15]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=16), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[17][0]}}</td>
	                        <td>{{preciosList[17][1]}} €</td>
	                        <td>{{previsionEolicaList[16]}} MWh</td>
	                        <td>{{previsionDemandaList[16]}} MWh</td>
	                        <td>{{energiaGestionadaList[16]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=17), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[18][0]}}</td>
	                        <td>{{preciosList[18][1]}} €</td>
	                        <td>{{previsionEolicaList[17]}} MWh</td>
	                        <td>{{previsionDemandaList[17]}} MWh</td>
	                        <td>{{energiaGestionadaList[17]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=18), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[19][0]}}</td>
	                        <td>{{preciosList[19][1]}}</td>
	                        <td>{{previsionEolicaList[18]}} MWh</td>
	                        <td>{{previsionDemandaList[18]}} MWh</td>
	                        <td>{{energiaGestionadaList[18]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=19), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[20][0]}}</td>
	                        <td>{{preciosList[20][1]}} €</td>
	                        <td>{{previsionEolicaList[19]}} MWh</td>
	                        <td>{{previsionDemandaList[19]}} MWh</td>
	                        <td>{{energiaGestionadaList[19]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=20), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[21][0]}}</td>
	                        <td>{{preciosList[21][1]}} €</td>
	                        <td>{{previsionEolicaList[20]}} MWh</td>
	                        <td>{{previsionDemandaList[20]}} MWh</td>
	                        <td>{{energiaGestionadaList[20]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=21), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[22][0]}}</td>
	                        <td>{{preciosList[22][1]}} €</td>
	                        <td>{{previsionEolicaList[21]}} MWh</td>
	                        <td>{{previsionDemandaList[21]}} MWh</td>
	                        <td>{{energiaGestionadaList[21]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=22), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[23][0]}}</td>
	                        <td>{{preciosList[23][1]}} €</td>
	                        <td>{{previsionEolicaList[22]}} MWh</td>
	                        <td>{{previsionDemandaList[22]}} MWh</td>
	                        <td>{{energiaGestionadaList[22]}} MWh</td>
	                    </tr>
	                    <tr>
	                        <td>{{str(date.strftime(technologyDT + timedelta(hours=23), '%d/%m/%Y'))}}</td>
	                        <td>{{preciosList[24][0]}}</td>
	                        <td>{{preciosList[24][1]}} €</td>
	                        <td>{{previsionEolicaList[23]}} MWh</td>
	                        <td>{{previsionDemandaList[23]}} MWh</td>
	                        <td>{{energiaGestionadaList[23]}} MWh</td>
	                    </tr>
	                </tbody>
	            </table>
				</div>
			</div>
		</div>
	</div>
</div>
<br></br>
</body>

<script>
$(document).ready(function() {
    $('#table_prevision').dataTable();
} );
</script>

</html>
