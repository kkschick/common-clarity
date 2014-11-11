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

loopControllers.controller('LogoutController', ['$scope', '$location', '$http', function($scope, $location, $http) {

    $scope.logoutUser = function() {
        $http({
            url: "/api/logout/",
            method: "POST",
        }).success(function () {
            $location.path('/');
        });
    };
}]);

loopControllers.controller('SettingsController', ['$scope', '$http', function($scope, $http){

    $scope.new_cohort = {};
    $scope.students = [];
    $scope.new_cohort.students = $scope.students;

    $scope.addRow = function(user) {
        $scope.students.push(user);
        $scope.user = {};
    };

    $scope.submitCohort = function(cohort, user) {
        $scope.new_cohort.cohort = cohort;
        $scope.cohort = {};

        $scope.students.push(user);
        $scope.user = {};

        $http({
            url: "/api/addclass/",
            method: "POST",
            data: $scope.new_cohort
        });

        $scope.sent = true;
        $scope.new_cohort = {};
        $scope.students = [];
        $scope.new_cohort.students = $scope.students;

        $http.get("/api/getclasses/").success(function(data) {
            $scope.cohorts = data;
    });
    };

    $http.get("/api/getclasses/").success(function(data) {
        $scope.cohorts = data;
    });

}]);


loopControllers.controller('ReportsController', ['$scope', '$http', function($scope, $http){

    $scope.import_clicked_button = true;

    $http.get("/api/getclasses/").success(function(data) {
        $scope.cohorts = data;

    });

    $scope.changeClick = function() {
        if ($scope.import_clicked === true) {
            $scope.import_clicked = false;
            $scope.import_clicked_button = true;
        }
        else {
            $scope.import_clicked = true;
            $scope.import_clicked_button = false;
        }
    };

    $scope.viewReport = function(selectedCohort, selectedStudent) {


        if ($scope.selectedStudent) {
            $scope.selectedUser = $scope.selectedStudent;
            $scope.cohort_selected = true;
            $scope.all_selected = false;
        }

        else if ($scope.selectedCohort > 0) {
            $scope.selectedUser = $scope.cohorts[$scope.selectedCohort - 1].name;
            $scope.cohort_selected = true;
            $scope.all_selected = false;
        }

        else {
            $scope.cohort_selected = false;
            $scope.all_selected = true;
        }



    };


}]);










