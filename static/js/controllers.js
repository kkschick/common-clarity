'use strict';

var loopControllers = angular.module('loopControllers', []);

function IndexCtrl($scope) {

}

function AboutCtrl($scope) {

}

function SignupCtrl($scope) {

}

function LoginCtrl($scope) {

}

function SettingsCtrl($scope) {

}

function ReportsCtrl($scope) {

}

// loopControllers.controller('PhoneListCtrl', ['$scope', 'Phone',
//   function($scope, Phone) {
//     $scope.phones = Phone.query();
//     $scope.orderProp = 'age';
//   }]);

// loopControllers.controller('PhoneDetailCtrl', ['$scope', '$routeParams', 'Phone',
//   function($scope, $routeParams, Phone) {
//     $scope.phone = Phone.get({phoneId: $routeParams.phoneId}, function(phone) {
//       $scope.mainImageUrl = phone.images[0];
//     });

//     $scope.setImage = function(imageUrl) {
//       $scope.mainImageUrl = imageUrl;
//     }
//   }]);
