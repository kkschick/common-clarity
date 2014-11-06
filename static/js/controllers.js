'use strict';

var loopControllers = angular.module('loopControllers', []);

loopControllers.controller('SettingsController', ['$scope', function($scope){
	$scope.master = {};

	$scope.addCohort = function(cohort) {
		$scope.master = angular.copy(cohort);
		$scope.cohort = {};
		$http.post("api/addclass", $scope.master).success(function(data, status, headers) {
		alert("Class added!");
	});
	};

}]);