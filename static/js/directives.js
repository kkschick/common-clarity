'use strict';

/* Directives */

var loopDirectives = angular.module('loopDirectives', []);

loopDirectives.directive( 'd3Pie', [
  function () {
    return {
      restrict: 'E',
      scope: {
        data: '='
      },
      link: function (scope, element) {

        var margin = {top: 50, right: 30, bottom: 30, left: 30},
          width = 400 - margin.left - margin.right,
          height = 360 - margin.top - margin.bottom,
          radius = Math.min(width, height) / 2;

        var color = d3.scale.ordinal()
          .range(["#547980", "#45ADA8", "#9DE0AD"]);

        var arc = d3.svg.arc()
          .outerRadius(radius - 10)
          .innerRadius(0);

        var pie = d3.layout.pie()
          .sort(null)
          .value(function(d){
            return d.Value;
            });

        var svg = d3.select(element[0]).append("svg")
            .attr("width", width)
            .attr("height", height)
          .append("g")
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

        scope.render = function(data) {

          svg.selectAll("*").remove();

          var tip = d3.tip()
            .attr('class', 'd3-tip')
            .offset([60, 0])
            .html(function(d) {
              if (d.data.Score === "M") {
                return "Meets Standard";
              }
              else if (d.data.Score === "A") {
                return "Approaches Standard";
              }
              else if (d.data.Score === "FB") {
                return "Falls Below Standard";
              }
            });

          svg.call(tip);


          data.forEach(function(d) {
            d.Value = +d.Value;
          });

          var g = svg.selectAll(".arc")
              .data(pie(data))
            .enter().append("g")
              .attr("class", "arc");

          g.append("path")
            .attr("d", arc)
            .style("fill", function(d) { return color(d.data.Score); })
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide);

          g.append("text")
            .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })
            .attr("dy", ".35em")
            .style("text-anchor", "middle")
            .text(function(d) { return d.data.Value.toFixed() + "%"; });

        };

          scope.$watch('data', function(){
              scope.render(scope.data);
          });
        }
    };
  }
]);

loopDirectives.directive( 'd3StackedBars', [
  function () {
    return {
      restrict: 'E',
      scope: {
        data: '='
      },
      link: function (scope, element) {
        var margin = {top: 30, right: 60, bottom: 60, left: 70},
          width = 560 - margin.left - margin.right,
          height = 360 - margin.top - margin.bottom;

        var svg = d3.select(element[0])
          .append("svg")
          .attr('width', width + margin.left + margin.right)
          .attr('height', height + margin.top + margin.bottom)
          .attr('id', 'svg_id')
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var x = d3.scale.ordinal().rangeRoundBands([0, width], .2);
        var y = d3.scale.linear().rangeRound([height, 0]);

        var color = d3.scale.ordinal()
          .range(["#547980", "#45ADA8", "#9DE0AD"]);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")
            .tickFormat(d3.format(".0%"));


        scope.render = function(data) {

          svg.selectAll("*").remove();

          x.domain(data.map(function(d) { return d.Name; }));

          color.domain(d3.keys(data[0]).filter(function(key) { return key !== "Name" && key !== "values"; }));

          data.forEach(function(d) {
          var y0 = 0;
          d.values = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +d[name]}; });
          d.values.forEach(function(d) { d.y0 /= y0; d.y1 /= y0; });
          });

          svg.selectAll('g.axis').remove();
          svg.append("g")
              .attr("class", "x axis")
              .attr("transform", "translate(0," + height + ")")
              .attr("fill", "white")
              .call(xAxis)
              .selectAll("text")
                .style("text-anchor", "end")
                .style("font-size","12px")
                .attr("dx", "-.8em")
                .attr("dy", ".15em")
                .attr("transform", function(d) {
                    return "rotate(-20)";
                    });

          svg.append("g")
              .attr("class", "y axis")
              .attr("fill", "white")
              .call(yAxis)
            .append("text")
              .attr("transform", "rotate(-90)")
              .attr("y", -60)
              .attr("x", -90)
              .attr("dy", ".6em")
              .style("text-anchor", "end")
              .attr("fill", "white")
              .text("% of students");

          var bars = svg.selectAll(".bar").data(data);
          bars.enter()
            .append("g")
            .attr("class", "bar")
            .attr("transform", function(d) { return "translate(" + x(d.Name) + ",0)"; });

          bars.selectAll("rect")
              .data(function(d) { return d.values; })
            .enter().append("rect")
              .attr("width", x.rangeBand())
              .attr("class", "rect")
              .attr("y", function(d) { return y(d.y1); })
              .attr("height", function(d) { return y(d.y0) - y(d.y1); })
              .style("fill", function(d) { return color(d.name); });

          bars.selectAll("text")
            .data(function(d) {return d.values;})
            .enter()
            .append("text")
            .attr("x", x.rangeBand() / 2)
            .attr("y", function(d, i) { return y(d.y1) + (y(d.y0) - y(d.y1))/2; })
            .style("text-anchor", "middle")
            .text(function(d) {
              if (d.name != "values") {
                  return ((((y(d.y0) - y(d.y1)) / height) * 100).toFixed()) + "%";
              }});


          var tip = d3.tip()
            .attr('class', 'd3-tip')
            .offset([-10, 0])
            .html(function(d) {
                if (d != "values") {
                  if (d === "3") {
                    return "Meets Standard (>75%)";
                  }
                  else if (d === "2") {
                    return "Approaches Standard (>50%)";
                  }
                  else if (d === "1") {
                    return "Falls Below Standard (>0%)";
                  }
          }});

          svg.call(tip);

          var legend = svg.selectAll(".legend")
                .data(color.domain().slice().reverse())
              .enter().append("g")
                .attr("class", "legend")
                .attr("transform", function(d, i) { return "translate(40," + i * 20 + ")"; });

          legend.append("rect")
              .attr("x", width - 36)
              .attr("width", 18)
              .attr("height", 18)
              .style("fill", color)
              .on('mouseover', tip.show)
              .on('mouseout', tip.hide);

          legend.append("text")
              .attr("x", width - 10)
              .attr("y", 9)
              .attr("dy", ".35em")
              .attr("fill", "white")
              .text(function(d) {
                if (d != "values") {
                  if (d === "3") {
                    return "M";
                  }
                  else if (d === "2") {
                    return "A";
                  }
                  else if (d === "1") {
                    return "FB";
                  }
          }});
      };

          scope.$watch('data', function(){
              scope.render(scope.data);
          });


        }
    };
  }
]);


loopDirectives.directive( 'd3StackedBarsWide', [
  function () {
    return {
      restrict: 'E',
      scope: {
        data: '='
      },
      link: function (scope, element) {
        var margin = {top: 30, right: 60, bottom: 60, left: 70},
          width = 560 - margin.left - margin.right,
          height = 360 - margin.top - margin.bottom;

        var svg = d3.select(element[0])
          .append("svg")
          .attr('width', width + margin.left + margin.right)
          .attr('height', height + margin.top + margin.bottom)
          .attr('id', 'svg_id')
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var x = d3.scale.ordinal().rangeRoundBands([0, width], .2);
        var y = d3.scale.linear().rangeRound([height, 0]);

        var color = d3.scale.ordinal()
          .range(["#547980", "#45ADA8", "#9DE0AD"]);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")
            .tickFormat(d3.format(".0%"));

        scope.render = function(data) {

          svg.selectAll("*").remove();

          // var axisTip = d3.tip()
          //   .attr('class', 'd3-tip')
          //   .offset([-10, 0])
          //   .html(function(d) { return '<a ng-model="collapsed" ng-click="collapsed=!collapsed">' + d.Description + '</a>';});

          // svg.call(axisTip);

          x.domain(data.map(function(d) { return d.Name; }));

          color.domain(d3.keys(data[0]).filter(function(key) { return key !== "Name" && key !== "values" && key !== "Description" && key !== "ID"; }));

          data.forEach(function(d) {
            var y0 = 0;
            d.values = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +d[name]}; });
            d.values.forEach(function(d) { d.y0 /= y0; d.y1 /= y0; });
            });

          svg.selectAll('g.axis').remove();
          svg.append("g")
              .attr("class", "x axis")
              .attr("transform", "translate(0," + height + ")")
              .attr("fill", "white")
              .call(xAxis)
              .selectAll("text")
                .style("text-anchor", "end")
                .style("font-size","12px")
                // .on('mouseover', axisTip.show)
                // .on('mouseout', axisTip.hide)
                .attr("dx", "-.8em")
                .attr("dy", ".15em")
                .attr("transform", function(d) {
                    return "rotate(-40)";
                    });

          svg.append("g")
              .attr("class", "y axis")
              .attr("fill", "white")
              .call(yAxis)
            .append("text")
              .attr("transform", "rotate(-90)")
              .attr("y", -60)
              .attr("x", -90)
              .attr("dy", ".6em")
              .style("text-anchor", "end")
              .attr("fill", "white")
              .text("% of students");

          // var barTip = d3.tip()
          //   .attr('class', 'd3-tip')
          //   .offset([-10, 0])
          //   .html(function(d) {
          //     if (d.name != "values") {
          //         return ((((y(d.y0) - y(d.y1)) / height) * 100).toFixed()) + "%";
          //     }});

          // svg.call(barTip);

          var bars = svg.selectAll(".bar").data(data);
          bars.enter()
            .append("g")
            .attr("class", "bar")
            .attr("transform", function(d) { return "translate(" + x(d.Name) + ",0)"; });

          bars.selectAll("rect")
              .data(function(d) { return d.values; })
            .enter().append("rect")
              .attr("width", x.rangeBand())
              .attr("class", "rect")
              .attr("y", function(d) { return y(d.y1); })
              .attr("height", function(d) { return y(d.y0) - y(d.y1); })
              .style("fill", function(d) { return color(d.name); });
              // .on('mouseover', barTip.show)
              // .on('mouseout', barTip.hide);

          bars.selectAll("text")
            .data(function(d) {return d.values;})
            .enter()
            .append("text")
            .attr("x", x.rangeBand() / 2)
            .attr("y", function(d, i) { return y(d.y1) + (y(d.y0) - y(d.y1))/2; })
            .style("text-anchor", "middle")
            .style("font-size", "10px")
            .text(function(d) {
              if (d.name != "values") {
                  return ((((y(d.y0) - y(d.y1)) / height) * 100).toFixed()) + "%";
              }});


          var legendTip = d3.tip()
            .attr('class', 'd3-tip')
            .offset([-10, 0])
            .html(function(d) {
                if (d != "values") {
                  if (d === "3") {
                    return "Meets Standard (>75%)";
                  }
                  else if (d === "2") {
                    return "Approaches Standard (>50%)";
                  }
                  else if (d === "1") {
                    return "Falls Below Standard (>0%)";
                  }
          }});

          svg.call(legendTip);

          var legend = svg.selectAll(".legend")
                .data(color.domain().slice().reverse())
              .enter().append("g")
                .attr("class", "legend")
                .attr("transform", function(d, i) { return "translate(40," + i * 20 + ")"; });

          legend.append("rect")
              .attr("x", width - 36)
              .attr("width", 18)
              .attr("height", 18)
              .style("fill", color)
              .on('mouseover', legendTip.show)
              .on('mouseout', legendTip.hide);

          legend.append("text")
              .attr("x", width - 10)
              .attr("y", 9)
              .attr("dy", ".35em")
              .attr("fill", "white")
              .text(function(d) {
                if (d != "values") {
                  if (d === "3") {
                    return "M";
                  }
                  else if (d === "2") {
                    return "A";
                  }
                  else if (d === "1") {
                    return "FB";
                  }
          }});
      };

          scope.$watch('data', function(){
              scope.render(scope.data);
          });


        }
    };
  }
]);

loopDirectives.directive( 'd3Bars', [
  function () {
    return {
      restrict: 'E',
      scope: {
        data: '='
      },
      link: function (scope, element) {
        var margin = {top: 15, right: 60, bottom: 150, left: 100},
          width = 400 - margin.left - margin.right,
          height = 360 - margin.top - margin.bottom;

        var svg = d3.select(element[0])
          .append("svg")
          .attr('width', width + margin.left + margin.right)
          .attr('height', height + margin.top + margin.bottom)
          .attr('id', 'svg_id')
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var x = d3.scale.ordinal().rangeRoundBands([0, width], .2);
        var y = d3.scale.linear().rangeRound([height, 0]);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")
            .tickFormat(d3.format(".0%"));

        scope.render = function(data) {

          svg.selectAll("*").remove();

          data.forEach(function(d) {
            d.value = +d.value;
          });

          x.domain(data.map(function(d) { return d.cohortName; }));
          y.domain([0, d3.max(data, function(d) { return d.value; })]);

          svg.selectAll('g.axis').remove();
          svg.append("g")
              .attr("class", "x axis")
              .attr("transform", "translate(0," + height + ")")
              .attr("fill", "white")
              .call(xAxis)
              .selectAll("text")
                .style("text-anchor", "end")
                .style("font-size","11px")
                .attr("dx", "2em")
                .attr("dy", ".7em")
                .attr("transform", function(d) {
                    return "rotate(-15)";
                    });

          svg.append("g")
              .attr("class", "y axis")
              .attr("fill", "white")
              .call(yAxis)
            .append("text")
              .attr("transform", "rotate(-90)")
              .attr("y", -70)
              .attr("x", -40)
              .attr("dy", ".6em")
              .style("text-anchor", "end")
              .attr("fill", "white")
              .text("% of students");

          svg.selectAll("bar")
              .data(data)
            .enter().append("rect")
              .style("fill", "#45ADA8")
              .attr("x", function(d) { return x(d.cohortName); })
              .attr("width", x.rangeBand())
              .attr("y", function(d) { return y(d.value); })
              .attr("height", function(d) { return height - y(d.value); });

          svg.append("text")
            .attr("x", parseFloat(shape.attr("x")) + width / 2 - 15)
            .attr("y", parseFloat(shape.attr("y")) - height / 2)
            .style("text-anchor", "middle")
            .style("font-size", "10px")
            .style("font-family", "sans-serif")
            .style("opacity", 0.7)
            .text(d3.format(",.1f")(d.value / 1000) + "k");

      };


        scope.$watch('data', function(){
            scope.render(scope.data);
        });
      }
    };
  }
]);