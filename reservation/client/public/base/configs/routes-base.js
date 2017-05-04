'use strict';

angular.module('BaseModule')
.config(['$urlRouterProvider',
    function($urlRouterProvider) {
        $urlRouterProvider.otherwise('/home');
    }
]);