'use strict';

var loopControllers = angular.module('loopControllers', []);

loopControllers.controller('SignupController', ['$scope', '$location', '$http', function($scope, $location, $http) {
	$scope.new_user = {};

	$scope.addUser = function(user) {
		$scope.new_user = angular.copy(user);
		$scope.user = {};
		$http({
			url: "/api/signup/",
			method: "POST",
			data: $scope.new_user
		}).success(function (data) {
			// alert("You created an account! Click LOG IN to log into your new account.")
			$location.path('/login/');
		});
	};
}]);

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
