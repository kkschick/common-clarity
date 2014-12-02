'use strict';

var clarityControllers = angular.module('clarityControllers', []);


////////////////////////////////
//// Controller for sign-up ////
////////////////////////////////

clarityControllers.controller('SignupController', ['$scope', '$location', '$http', function($scope, $location, $http) {

    $scope.new_user = {};

    // Add user function
    $scope.addUser = function(user) {
        $scope.new_user = angular.copy(user);

        // Clear out form
        $scope.user = {};

        // Send user info to signup endpoint
        $http({
            url: "/api/signup/",
            method: "POST",
            data: $scope.new_user
        }).success(function (data) {
            // Redirect to login upon success
            $location.path('/login/');
        });
    };
}]);


///////////////////////////////
//// Controller for log-in ////
///////////////////////////////

clarityControllers.controller('LoginController', ['$scope', '$location', '$http', function($scope, $location, $http) {

    $scope.user_to_login = {};

    // Function to log in user
    $scope.loginUser = function(user) {
        $scope.user_to_login = angular.copy(user);

        // Clear out form
        $scope.user = {};

        // Send credentials to login endpoint
        $http({
            url: "/api/login/",
            method: "POST",
            data: $scope.user_to_login
        }).success(function (data) {
            // Redirect to reports dashboard upon success
            $location.path('/reports/');
        });
    };
}]);


////////////////////////////////
//// Controller for log out ////
////////////////////////////////

clarityControllers.controller('LogoutController', ['$scope', '$location', '$http', function($scope, $location, $http) {

    // Function to log user out
    $scope.logoutUser = function() {
        $http({
            url: "/api/logout/",
            method: "POST",
        }).success(function () {
            $location.path('/');
        });
    };
}]);


/////////////////////////////////
//// Controller for settings ////
/////////////////////////////////

clarityControllers.controller('SettingsController', ['$scope', '$http', 'ModalService', function($scope, $http, ModalService){

    // Default to upload method selected
    $scope.selectedMethod = 'upload';

    $scope.new_cohort = {};
    $scope.students = [];
    $scope.new_cohort.students = $scope.students;

    $scope.display = false;

    // Show/hide modal functions for upload instructions
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
            $scope.customResult = "Done!";
          });
        });
    };

    // When button clicked, add prior user to $scope.students and clear out form
    $scope.addRow = function(user) {
        $scope.students.push(user);
        $scope.user = {};
    };

    // Function to add class using manual process
    $scope.submitCohort = function(cohort, user) {
        $scope.new_cohort.cohort = cohort;
        $scope.cohort = {};

        $scope.students.push(user);
        $scope.user = {};

        // Send new cohort to add to add class endpoint
        $http({
            url: "/api/addclass/",
            method: "POST",
            data: $scope.new_cohort
        });

        // Clear out form
        $scope.sent = true;
        $scope.new_cohort = {};
        $scope.students = [];
        $scope.new_cohort.students = $scope.students;

        // Get and display classes
        $http.get("/api/getclasses/").success(function(data) {
            $scope.cohorts = data;
        });
    };

    // Get and display classes
    $http.get("/api/getclasses/").success(function(data) {
        $scope.cohorts = data;
    });

}]);


////////////////////////////////
//// Controller for reports ////
////////////////////////////////

clarityControllers.controller('ReportsController', ['$scope', '$http', 'ModalService', function($scope, $http, ModalService) {

    // Default selections to zero
    $scope.selectedCohort = 0;
    $scope.selectedStudent = 0;

    // When cohort is changed, set student value to null
    $scope.onChange = function(value) {
        $scope.selectedStudent = null;
    };

    // When student is change, set cohort value to null
    $scope.onStudChange = function(value) {
        $scope.selectedCohort = null;
    };

    // Get the teacher's cohorts
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
