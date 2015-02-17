#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Python-nvd3 is a Python wrapper for NVD3 graph library.
NVD3 is an attempt to build re-usable charts and chart components
for d3.js without taking away the power that d3.js gives you.

Project location : https://github.com/areski/python-nvd3
"""

<<<<<<< HEAD
from .NVD3Chart import NVD3Chart, TemplateMixin


class discreteBarChart(TemplateMixin, NVD3Chart):
=======
from .NVD3Chart import NVD3Chart


class discreteBarChart(NVD3Chart):
>>>>>>> b3c763ecf687c7317f4a0af05d07db99af008e81
    """
    A discrete bar chart or bar graph is a chart with rectangular bars with
    lengths proportional to the values that they represent.

<<<<<<< HEAD
=======
    .. image:: ../_static/doc_images/discreteBarChart.png

>>>>>>> b3c763ecf687c7317f4a0af05d07db99af008e81
    Python example::

        from nvd3 import discreteBarChart
        chart = discreteBarChart(name='discreteBarChart', height=400, width=400)

        xdata = ["A", "B", "C", "D", "E", "F"]
        ydata = [3, 4, 0, -3, 5, 7]

        chart.add_serie(y=ydata, x=xdata)
        chart.buildhtml()

<<<<<<< HEAD
    Javascript generated:

    .. raw:: html

        <div id="discreteBarChart"><svg style="height:450px;"></svg></div>
        <script>
            data_discreteBarChart=[{"values": [{"y": 3, "x": "A"}, {"y": 4, "x": "B"}, {"y": 0, "x": "C"}, {"y": -3, "x": "D"}, {"y": 5, "x": "E"}, {"y": 7, "x": "F"}], "key": "Serie 1", "yAxis": "1"}];

            nv.addGraph(function() {
                var chart = nv.models.discreteBarChart();

                chart.margin({top: 30, right: 60, bottom: 20, left: 60});

                var datum = data_discreteBarChart;
                        chart.yAxis
                            .tickFormat(d3.format(',.0f'));
                        chart.tooltipContent(function(key, y, e, graph) {
                            var x = String(graph.point.x);
                            var y = String(graph.point.y);
                            var y = String(graph.point.y);

                            tooltip_str = '<center><b>'+key+'</b></center>' + y + ' at ' + x;
                            return tooltip_str;
                        });

                d3.select('#discreteBarChart svg')
                    .datum(datum)
                    .transition().duration(500)
                    .attr('width', 400)
                    .attr('height', 400)
                    .call(chart);
            });
        </script>


    """
    CHART_FILENAME = "./discretebarchart.html"
    template_chart_nvd3 = NVD3Chart.template_environment.get_template(CHART_FILENAME)

    def __init__(self, **kwargs):
        super(discreteBarChart, self).__init__(**kwargs)
        self.model = 'discreteBarChart'
=======
    Javascript generated::

        nv.addGraph(function() {
            var chart = nv.models.discreteBarChart();
            chart.tooltipContent(function(key, y, e, graph) {
                var x = String(graph.point.x);
                var y = String(graph.point.y);
                var y = String(graph.point.y);
                tooltip_str = '<center><b>'+key+'</b></center>' + y + ' at ' + x;
                return tooltip_str;
            });
            d3.select('#discreteBarChart svg')
                .datum(data_discreteBarChart)
                .transition().duration(500)
                .attr('width', 400)
                .attr('height', 400)
                .call(chart);

        return chart;
        });data_discreteBarChart=[
            {"key": "Serie 1",
            "yAxis": "1",
            "values": [{"x": "A", "y": 3},
                       {"x": "B", "y": 4},
                       {"x": "C", "y": 0},
                       {"x": "D", "y": 3},
                       {"x": "E", "y": 5},
                       {"x": "F", "y": 7}
        ]}];
    """
    def __init__(self, **kwargs):
        NVD3Chart.__init__(self, **kwargs)
        # self.slugify_name(kwargs.get('name', 'discreteBarChart'))
>>>>>>> b3c763ecf687c7317f4a0af05d07db99af008e81
        height = kwargs.get('height', 450)
        width = kwargs.get('width', None)

        if kwargs.get('x_is_date', False):
            self.set_date_flag(True)
            self.create_x_axis('xAxis',
<<<<<<< HEAD
                               format=kwargs.get('x_axis_format',
                                                 "%d %b %Y %H %S"),
=======
                               format=kwargs.get('x_axis_format', "%d %b %Y %H %S"),
>>>>>>> b3c763ecf687c7317f4a0af05d07db99af008e81
                               date=True)
        else:
            self.create_x_axis('xAxis', format=None)

        self.create_y_axis('yAxis', format=kwargs.get('y_axis_format', ".0f"))

        self.set_custom_tooltip_flag(True)

<<<<<<< HEAD
        self.set_graph_height(height)
=======
        # must have a specified height, otherwise it superimposes both charts
        if height:
            self.set_graph_height(height)
>>>>>>> b3c763ecf687c7317f4a0af05d07db99af008e81
        if width:
            self.set_graph_width(width)
