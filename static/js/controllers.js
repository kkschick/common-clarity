'use strict';

var loopControllers = angular.module('loopControllers', []);

loopControllers.controller('SettingsController', ['$scope', function($scope){
	$scope.master = {};

	$scope.addCohort = function(cohort) {
		console.log(angular.copy(cohort));
		$scope.master = angular.copy(cohort);
		$scope.cohort = {};
	};

	// $http.post('/api/addclass', $scope.master).
	// 	success(function() {
	// 	console.log("YAY");
	// }).
	// error(function() {
	// 	console.log("NO!");
	// });
}]);