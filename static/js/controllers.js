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
			$location.path('/login/');
		});
	};
}]);

loopControllers.controller('LoginController', ['$scope', '$location', '$http', function($scope, $location, $http) {
	$scope.user_to_login = {};

	$scope.loginUser = function(user) {
		$scope.user_to_login = angular.copy(user);
		$scope.user = {};
		$http({
			url: "/api/login/",
			method: "POST",
			data: $scope.user_to_login
		}).success(function (data) {
			$location.path('/reports/');
		});
	};
}]);

loopControllers.controller('LogoutController', ['$scope', '$location', function($scope, $location) {

	$scope.logoutUser = function() {
		$location.path('/');
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
