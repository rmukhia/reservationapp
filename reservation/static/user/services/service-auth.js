'use strict';

/*
 * User authentication
 * If user is not authenciated, user will be null.
 */
angular.module('UserModule')
.factory('AuthService', ['$log', '$http', '$location', '$window', 'RestInterfaceService',
    function($log, $http, $location, $window, RestInterfaceService){
    
    var obj = {};

    obj.user = null;


    obj.login = function(){
        var login = '/api-auth/login/?next=/';
        // $log.debug('login: ' + login);
        $window.location.href = login;
        //$location.url(login);
    };

    obj.logout = function() {
        $http({
            method: 'GET',
            url: '/api-auth/logout'
            }).then(
            /* jshint unused:vars */ 
            function successCallback(response) {
                obj.user = null;
                // $log.debug('logout');
                $window.location.href = '#';
            },
            /* jshint unused:vars */ 
            function errorCallback(response) {
                $log.error('logout failed');
            });
    };
    

    obj.logged_in = function(success_callback, failure_callback) {
        $http({
            method: 'GET',
            url: '/api-auth/logged_in?format=json'
            }).then(
            function successCallback(response) {
                // $log.debug("printed response ..",response);
                new RestInterfaceService(
                AppConfig.rest_api_base + '/preferences/search/',
                'GET',
                {
                    user : response.data.id,
                },
                function(result){
                        $log.debug(result,"printed result here ...!!");
                        obj.user.preferences = result;
                        // if image is null
                        
                        if(obj.user.preferences[0].image.match(/media\/0/))
                        {
                            // $log.debug("here i am .."+obj.user.preferences[0].image);
                            obj.user.preferences[0].image = null;
                        }
                 });  
                // $log.debug('login validated');
                obj.user = response.data;
                obj.user.url = '/' + AppConfig.rest_api_base + '/users/' + obj.user.id + '/';
                // $log.debug("hello... iam here logged in");
                
                if (success_callback) {
                    success_callback(obj.user);
                }
            },
            /* jshint unused:vars */ 
            function errorCallback(response) {
                obj.user = null;
                if (failure_callback) {
                    failure_callback();
                }
            });
    };

    return obj;

}]);
