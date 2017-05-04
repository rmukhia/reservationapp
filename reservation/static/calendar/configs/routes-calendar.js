'use strict';

angular.module('CalendarModule')
.config(['$stateProvider','$logProvider',
    function($stateProvider,$logProvider) {
        $stateProvider.state('calendar', {
            url: '/calendar/:chassis_id?blade_id?hostname?flag',
            templateUrl: AppConfig.base_path + 'calendar/views/view-calendar.htm',
            controller: 'CalendarController'
        });

        $logProvider.debugEnabled(false);
    }
]);

