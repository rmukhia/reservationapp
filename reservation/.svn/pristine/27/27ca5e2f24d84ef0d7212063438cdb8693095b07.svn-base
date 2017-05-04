'use strict';

angular.module('DevelopModule')
.controller('DevelopController', ['$log', '$scope', '$location', '$state', 'AuthService', 'RestInterfaceService',
    function($log, $scope, $location, $state, AuthService, RestInterfaceService) {
        
        $scope.AppConfig = AppConfig;
        $scope.AuthService = AuthService;

        // Check if user is logged in
        if (AuthService.user === null) {
            $state.transitionTo('home');
        }

        var api_endpoint = new  RestInterfaceService(
            '/' + AppConfig.rest_api_base  + '/', 
            'GET',
            {}, 
            function(m){
                $log.info(m);
                $scope.models = m;
            });

        api_endpoint = null;
    }
]);