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

    $scope.importClickedButton = true;

    $http.get("/api/getclasses/").success(function(data) {
        $scope.cohorts = data;

    });

    $scope.changeClick = function() {
        if ($scope.importClicked === true) {
            $scope.importClicked = false;
            $scope.importClickedButton = true;
        }
        else {
            $scope.importClicked = true;
            $scope.importClickedButton = false;
        }
    };

    $scope.viewReport = function() {

        $scope.selectedUser = null;

        $scope.studentSelected = false;
        $scope.cohortSelected = false;
        $scope.allSelected = false;

        $scope.viewReportClicked = true;

        if ($scope.selectedStudent) {
            $scope.viewReportClicked = false;
            var student = JSON.parse($scope.selectedStudent);
            $scope.selectedUser = student.name;
            $scope.studentSelected = true;
            $scope.cohortSelected = false;
            $scope.allSelected = false;

            $http.get("/api/singlestudentcounts/", { params: {id: student.id }}).success(function(data){
                $scope.oneStudentData = data;
            });
            $scope.selectedStudent = null;
        }

        else if ($scope.selectedCohort > 0) {
            $scope.selectedUser = $scope.cohorts[$scope.selectedCohort - 1].name;
            $scope.selectedSubReport = "overall";
            $scope.studentSelected = false;
            $scope.cohortSelected = true;
            $scope.allSelected = false;

            $http.get("/api/singlecohortcounts/", {params: { id: $scope.selectedCohort }}).success(function(data) {
                $scope.oneCohortData = data;
            });

            $http.get("/api/mostrecentcohort/", {params: { id: $scope.selectedCohort }}).success(function(data) {
                $scope.cohortStandard = data;
            });
        }

        else {

            $scope.selectedSubReport = "overall";
            $scope.studentSelected = false;
            $scope.cohortSelected = false;
            $scope.allSelected = true;

            $http.get("/api/allcohortcounts/").success(function(data) {
                $scope.allCohortsData = data;
            });

            $http.get("/api/mostrecentall/").success(function(data) {
                $scope.allStandard = data;
            });
        }

    };

}]);
