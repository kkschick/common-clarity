'use strict';

var loopApp = angular.module('loopApp', [
  'ngRoute',
  // 'loopAnimations',

  'loopControllers',
  // 'loopFilters',
  // 'loopServices'
]);

loopApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        templateUrl: '../static/partials/home.html',
        // controller: 'IndexCtrl'
      }).
      when('/about', {
        templateUrl: '../static/partials/about.html',
        // controller: 'AboutCtrl'
      }).
      when('/login', {
        templateUrl: '../static/partials/login.html',
        controller: 'LoginController'
      }).
      when('/signup', {
        templateUrl: '../static/partials/signup.html',
        controller: 'SignupController'
      }).
      when('/settings', {
        templateUrl: '../static/partials/settings.html',
        controller: 'SettingsController'
      }).
      when('/reports', {
        templateUrl: '../static/partials/reports.html',
        // controller: 'ReportsCtrl'
      }).
      otherwise({
        redirectTo: '/'
      });
  }]);
