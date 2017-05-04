'use strict';

angular.module('RecordsModule')
.config(['$stateProvider','$httpProvider','$logProvider',
    function($stateProvider, $httpProvider,$logProvider) {
        $stateProvider.state('records', {
            url: '/records/:chassis_id?blade_id',
            templateUrl: AppConfig.base_path + 'records/views/view-records.htm',
            controller: 'RecordsController'
        });
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
		$logProvider.debugEnabled(true);
    }
]);
