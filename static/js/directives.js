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
        var margin = {top: 20, right: 20, bottom: 30, left: 40},
          width = 480 - margin.left - margin.right,
          height = 360 - margin.top - margin.bottom;

        var svg = d3.select(element[0])
          .append("svg")
          .attr('width', width + margin.left + margin.right)
          .attr('height', height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var x = d3.scale.ordinal().rangeRoundBands([0, width], .1);
        var y = d3.scale.linear().rangeRound([height, 0]);

        var color = d3.scale.ordinal()
          .range(["#547980", "#45ADA8", "#9DE0AD", "#E5FCC2", "#a05d56", "#d0743c", "#ff8c00"]);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")
            .tickFormat(d3.format(".0%"));

        scope.render = function(data) {
          x.domain(data.map(function(d) { return d.Name; }));


          color.domain(d3.keys(data[0]).filter(function(key) { return key !== "Name"; }));

          data.forEach(function(d) {
          var y0 = 0;
          d.ages = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +d[name]}; });
          d.ages.forEach(function(d) { d.y0 /= y0; d.y1 /= y0; });
          });

    data.sort(function(a, b) { return b.ages[0].y1 - a.ages[0].y1; });

          // y.domain([0, d3.max(data, function(d) { return d.value; })]);

          // svg.selectAll('g.axis').remove();
          svg.append("g")
              .attr("class", "x axis")
              .attr("transform", "translate(0," + height + ")")
              .call(xAxis);

          svg.append("g")
              .attr("class", "y axis")
              .call(yAxis)
            .append("text")
              .attr("transform", "rotate(-90)")
              .attr("y", 6)
              .attr("dy", ".71em")
              .style("text-anchor", "end")
              .text("% of students");


          var bars = svg.selectAll(".bar").data(data);
          bars.enter()
            .append("g")
            .attr("class", "bar")
            .attr("transform", function(d) { return "translate(" + x(d.Name) + ",0)"; });

          bars.selectAll("rect")
              .data(function(d) { return d.ages; })
            .enter().append("rect")
              .attr("width", x.rangeBand())
              .attr("y", function(d) { return y(d.y1); })
              .attr("height", function(d) { return y(d.y0) - y(d.y1); })
              .style("fill", function(d) { return color(d.name); });
          // bars
          //     .transition()
          //     .duration(1000)
          //     .attr('height', function(d) { return height - y(d.value); })
          //     .attr("y", function(d) { return y(d.value); })
        };

          scope.$watch('data', function(){
              scope.render(scope.data);
          }, true);
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