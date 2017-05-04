'use strict';

angular.module('DevelopModule')
.config(['$stateProvider',
    function($stateProvider) {
        $stateProvider.state('develop', {
            url: '/develop',
            templateUrl: AppConfig.base_path + 'develop/views/view-develop.htm',
            controller: 'DevelopController'
        });
    }
]);
