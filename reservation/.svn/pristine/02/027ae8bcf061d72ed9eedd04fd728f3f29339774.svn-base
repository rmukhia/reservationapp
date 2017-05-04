'use strict';

/* 
 * url: url
 * method: GET, POST, PUT, OPTION
 * params: request params
 * success_callback: returns success object with 
 */

angular.module('RestInterfaceModule')
.factory('RestInterfaceService', ['$log', '$http', 
    function($log, $http){
        return function(url, method, params, success_callback, failed_callback, function_params) {
            var obj = {};
            var http_config = {
                url: url,
                method: method
            } 

            if (method == "GET" || method=="DELETE") {
                http_config.params = params;
            }
            else if(method == "POST" || method=="PUT") {
                http_config.data = params;
            }

            $http(http_config).then(
                    function successCallback(response) {
                        var m = {};
                        for(var model in response.data) {
                            m[model] = response.data[model];
                        }
                        // This is module load callback function
                        if (success_callback) {
                            success_callback(m, function_params);
                        }
                    },
                    /* jshint unused:vars */ 
                    function errorCallback(response) {
                        if (failed_callback) {
                            failed_callback();
                        }
                        console.log('Initial api population failed');
                    }
                );
            return obj;
            };
        }
]);