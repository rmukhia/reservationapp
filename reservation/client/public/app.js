'use strict';

angular.module(AppConfig.app_name, AppConfig.app_dependencies);

// Setting HTML5 Location Mode
angular.module(AppConfig.app_name).config(['$locationProvider','$logProvider',
    function($locationProvider,$logProvider) {
        $locationProvider.hashPrefix('');
        $logProvider.debugEnabled(true);
    }
    
]);

//Then define the init function for starting up the application
angular.element(document).ready(function() {
    //Fixing facebook bug with redirect
    if (window.location.hash === '#_=_') window.location.hash = '#!';

    //Then init the app
    angular.bootstrap(document, [AppConfig.app_name]);
});

