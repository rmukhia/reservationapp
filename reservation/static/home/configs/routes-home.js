'use strict';

angular.module('HomeModule')
.config(['$stateProvider','$logProvider',
    function($stateProvider,$logProvider) {
        
        $stateProvider.state('home', {
            url: '/home',
            templateUrl: AppConfig.base_path + 'home/views/view-home.htm',
            controller: 'HomeController'
        });

        $logProvider.debugEnabled(false);
    }
]);
