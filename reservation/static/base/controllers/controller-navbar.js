'use strict';

angular.module('BaseModule').controller('NavbarController', ['$scope', '$location', 'AuthService',
    function($scope, $location, AuthService) {
        
        // Set the title       
        $scope.AppConfig = AppConfig;

        $scope.AuthService = AuthService;

        $scope.AuthService.logged_in(); 
        // Active class
        $scope.navbar_link = function(page){
                var currentRoute = $location.path().split("/")[1] || 'home'; 
                return page == currentRoute ? 'active': '';
        };
        
    }
]);