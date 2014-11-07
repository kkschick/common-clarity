'use strict';

var loopControllers = angular.module('loopControllers', []);


loopControllers.controller('SettingsController', ['$scope', '$http', function($scope, $http){
	$scope.master = {};

	$scope.addCohort = function(cohort) {
		$scope.master = angular.copy(cohort);
		$scope.cohort = {};
		$http({
			url: "/api/addclass/",
			method: "POST",
			data: $scope.master
		});
	};
}]);
