'use strict';

/* Directives */

var loopDirectives = angular.module('loopDirectives', []);

loopDirectives.directive( 'd3StackedBars', [
  function () {
    return {
      restrict: 'E',
      scope: {
        data: '='
      },
      link: function (scope, element) {
        var margin = {top: 30, right: 60, bottom: 60, left: 70},
          width = 600 - margin.left - margin.right,
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
          width = 800 - margin.left - margin.right,
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

        var barTip = d3.tip()
          .attr('class', 'd3-tip')
          .offset([-10, 0])
          .html(function(d) {
            if (d.name != "values") {
                return ((((y(d.y0) - y(d.y1)) / height) * 100).toFixed()) + "%";
            }});

        svg.call(barTip);

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
            .style("fill", function(d) { return color(d.name); })
            .on('mouseover', barTip.show)
            .on('mouseout', barTip.hide);

        bars.selectAll("text")
          .data(function(d) {return d.values;})
          .enter()
          .append("text")
          .attr("x", x.rangeBand() / 2)
          .attr("y", function(d, i) { return y(d.y1) + (y(d.y0) - y(d.y1))/2; })
          .style("text-anchor", "middle");

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

// loopDirectives.directive( 'd3Bars', [
//   function () {
//     return {
//       restrict: 'E',
//       scope: {
//         data: '='
//       },
//       link: function (scope, element) {
//         var margin = {top: 20, right: 20, bottom: 30, left: 40},
//           width = 480 - margin.left - margin.right,
//           height = 360 - margin.top - margin.bottom;
//         var svg = d3.select(element[0])
//           .append("svg")
//           .attr('width', width + margin.left + margin.right)
//           .attr('height', height + margin.top + margin.bottom)
//           .append("g")
//             .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

//         var x = d3.scale.ordinal().rangeRoundBands([0, width], .1);
//         var y = d3.scale.linear().range([height, 0]);

//         var xAxis = d3.svg.axis()
//             .scale(x)
//             .orient("bottom");

//         var yAxis = d3.svg.axis()
//             .scale(y)
//             .orient("left")
//             .ticks(10);

//         scope.render = function(data) {
//           x.domain(data.map(function(d) { return d.name; }));
//           y.domain([0, d3.max(data, function(d) { return d.value; })]);

//           svg.selectAll('g.axis').remove();
//           svg.append("g")
//               .attr("class", "x axis")
//               .attr("transform", "translate(0," + height + ")")
//               .call(xAxis);

//           svg.append("g")
//               .attr("class", "y axis")
//               .call(yAxis)
//             .append("text")
//               .attr("transform", "rotate(-90)")
//               .attr("y", 6)
//               .attr("dy", ".71em")
//               .style("text-anchor", "end")
//               .text("% of students");

//           var bars = svg.selectAll(".bar").data(data);
//           bars.enter()
//             .append("rect")
//             .attr("class", "bar")
//             .attr("x", function(d) { return x(d.name); })
//             .attr("width", x.rangeBand());

//           bars
//               .transition()
//               .duration(1000)
//               .attr('height', function(d) { return height - y(d.value); })
//               .attr("y", function(d) { return y(d.value); })
//         };

//           scope.$watch('data', function(){
//               scope.render(scope.data);
//           }, true);
//         }
//     };
//   }
// ]);