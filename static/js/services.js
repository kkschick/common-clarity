'use strict';

/* Services */

var loopServices = angular.module('loopServices', ['ngResource']);

loopServices.factory('Phone', ['$resource',
  function($resource){
    return $resource('phones/:phoneId.json', {}, {
      query: {method:'GET', params:{phoneId:'phones'}, isArray:true}
    });
  }]);
