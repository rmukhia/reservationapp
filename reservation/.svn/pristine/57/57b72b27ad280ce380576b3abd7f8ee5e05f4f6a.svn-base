'use strict';

angular.module('PreferenceModule')
.config(['$stateProvider','$httpProvider','$logProvider',
    function($stateProvider,$httpProvider,$logProvider) {
        
        $stateProvider.state('preference', {
            url: '/preference',
            templateUrl: AppConfig.base_path + 'preference/views/view-preference.htm',
            controller: 'PreferenceController'
        });

        $logProvider.debugEnabled(false);
    }
]);


// 'use strict';

// angular.module('RecordsModule')
// .config(['$stateProvider','$httpProvider',
//     function($stateProvider, $httpProvider) {
//         $stateProvider.state('records', {
//             url: '/records',
//             templateUrl: AppConfig.base_path + 'records/views/view-records.htm',
//             controller: 'RecordsController'
//         });
//         $httpProvider.defaults.xsrfCookieName = 'csrftoken';
//     	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
//     }
// ]);