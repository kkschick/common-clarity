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

loopControllers.controller('SettingsController', ['$scope', '$http', 'ModalService', function($scope, $http, ModalService){

    $scope.selectedMethod = 'upload';

    $scope.new_cohort = {};
    $scope.students = [];
    $scope.new_cohort.students = $scope.students;

    $scope.display = false;

    $scope.showModal = function() {
        $scope.display = true;
    };


    $scope.close = function() {
        $scope.display = false;
        close();
    };

    $scope.showCustom = function() {

        ModalService.showModal({
          templateUrl: "custom/custom.html",
          controller: "CustomController"
        }).then(function(modal) {
          modal.close.then(function(result) {
            $scope.customResult = "All good!";
          });
        });

    };

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

    $scope.allSelected = true;
    $scope.selectedCohort = 0;
    $scope.selectedStudent = 0;

    $http.get("/api/getclasses/").success(function(data) {
        $scope.cohorts = data;
    });

    // Top standards students are struggling with
    $http.get("/api/allcohortstopfb/").success(function(data) {
        $scope.allCohortsTopFB = data.slice(0, 5);
        $scope.allCohortsTopFBAll = data;
        $scope.orderByField = 'Percent';
    });

    // Overall pie chart data of most recent test
    $http.get("/api/allcohortspie/").success(function(data) {
        $scope.allCohortsPie = data;
    });

    // Bar graph data comparing all students to school/district
    $http.get("/api/allcohortsnorm/").success(function(data) {
        $scope.allCohortsNorm = data;
    });

    // All data from all tests for stacked bar graph
    $http.get("/api/allcohortscounts/").success(function(data) {
        $scope.allCohortsData = data;
    });

    // Most recent test broken out by standard
    $http.get("/api/allcohortsbystandard/").success(function(data) {
        $scope.allStandard = data;
        $scope.tableStandard = angular.copy(data);
    });

    // Top students who are struggling to meet standards
    $http.get("/api/allcohortsstudents/").success(function(data) {
        $scope.allCohortsStudents = data.slice(0,10);
        $scope.orderByValue = '-total';
    });

    $scope.viewReport = function() {

        $scope.selectedUser = null;

        $scope.studentSelected = false;
        $scope.cohortSelected = false;
        $scope.allSelected = false;
        $scope.showByStudent = false;

        $scope.viewReportClicked = true;

        if ($scope.selectedStudent) {
            $scope.viewReportClicked = false;
            var student = JSON.parse($scope.selectedStudent);
            $scope.selectedUser = student.name;
            $scope.studentSelected = true;
            $scope.cohortSelected = false;
            $scope.allSelected = false;

            // $http.get("/api/singlestudentcounts/", { params: {id: student.id }}).success(function(data){
            //     $scope.oneStudentData = data;
            // });
            $scope.selectedStudent = null;
        }

        else if ($scope.selectedCohort > 0) {
            $scope.selectedStudent = 0;
            $scope.showByStudent = true;
            $scope.selectedUser = $scope.cohorts[$scope.selectedCohort - 1].name;
            $scope.studentSelected = false;
            $scope.cohortSelected = true;
            $scope.allSelected = false;

            // Top standards students are struggling with
            $http.get("/api/singlecohorttopfb/", {params: { id: $scope.selectedCohort }}).success(function(data) {
                $scope.oneCohortTopFB = data.slice(0, 5);
                $scope.oneCohortTopFBAll = data;
                $scope.orderByField = 'Percent';
            });

            // $http.get("/api/singlecohortcounts/", {params: { id: $scope.selectedCohort }}).success(function(data) {
            //     $scope.oneCohortData = data;
            // });

            // $http.get("/api/mostrecentcohort/", {params: { id: $scope.selectedCohort }}).success(function(data) {
            //     $scope.cohortStandard = data;
            //     $scope.tableCohortStandard = angular.copy(data);
            // });
        }

        else {
            $scope.studentSelected = false;
            $scope.cohortSelected = false;
            $scope.allSelected = true;
            $scope.selectedStudent = 0;
        }

    };

}]);
