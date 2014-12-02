'use strict';

var clarityControllers = angular.module('clarityControllers', []);

clarityControllers.controller('SignupController', ['$scope', '$location', '$http', function($scope, $location, $http) {
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

clarityControllers.controller('LoginController', ['$scope', '$location', '$http', function($scope, $location, $http) {
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

clarityControllers.controller('LogoutController', ['$scope', '$location', '$http', function($scope, $location, $http) {

    $scope.logoutUser = function() {
        $http({
            url: "/api/logout/",
            method: "POST",
        }).success(function () {
            $location.path('/');
        });
    };
}]);

clarityControllers.controller('SettingsController', ['$scope', '$http', 'ModalService', function($scope, $http, ModalService){

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

    // $scope.onSave = function() {
    //     console.log($scope.cohorts);
    //     $scope.editorEnabled = false;
    // };

}]);


clarityControllers.controller('ReportsController', ['$scope', '$http', 'ModalService', function($scope, $http, ModalService) {

    $scope.selectedCohort = 0;
    $scope.selectedStudent = 0;

    $scope.onChange = function(value) {
        $scope.selectedStudent = null;
    };

    $scope.onStudChange = function(value) {
        $scope.selectedCohort = null;
    };

    $http.get("/api/getclasses/").success(function(data) {
        $scope.cohorts = data;
    });

    // Top standards students are struggling with
    $http.get("/api/allcohortstopfb/").success(function(data) {
        $scope.allCohortsTopFB = data.slice(0, 5);
        $scope.allCohortsTopFBAll = data;
        $scope.orderByField = 'percent';
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

    // Get all cohort data by cohort
    $http.get("/api/allsinglecohortdata/").success(function(data) {
        $scope.cohortDataByCohort = data;
    });

    // Get all student data by student
    $http.get("/api/allsinglestudentdata/").success(function(data) {
        $scope.studentDataByStudent = data;
    });

}]);
