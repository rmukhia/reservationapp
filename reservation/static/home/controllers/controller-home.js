'use strict';

angular.module('HomeModule')
.controller('HomeController', ['$log', '$scope', '$location', '$state', '$interval', 'AuthService', 'RestInterfaceService','$sce',
    function($log, $scope, $location, $state, $interval, AuthService, RestInterfaceService,$sce) {

        $scope.htmlTooltip = $sce.trustAsHtml('I\'ve been made <b>bold</b>!');
        $scope.placement = {
                options: [
                  'top',
                  'top-left',
                  'top-right',
                  'bottom',
                  'bottom-left',
                  'bottom-right',
                  'left',
                  'left-top',
                  'left-bottom',
                  'right',
                  'right-top',
                  'right-bottom'
                ],
                selected: 'top'
        };

        $scope.active_class = "true";
        $scope.AppConfig = AppConfig;
        $scope.AuthService = AuthService;
        $scope.RestInterfaceService = RestInterfaceService;
        $scope.a = 123;
        $scope.submit = {};
        $scope.search= '';
        var page = 1;
        var list_interval_promise
         // Authenticated User can view
        $scope.AuthService.logged_in(
            function(user){
                // Show list view if user is present
                if (user == null) {
                   return;
                }

                get_list(page);

                var interval_time = 1000 * 15; // 30 seconds
                list_interval_promise = $interval(function(){
                    get_list(page);
                },
                interval_time
                );
        });


        $scope.submit.activate = function()
        {
          $scope.active_class = "false";
        }

        function get_list(page){
            new  RestInterfaceService(
                AppConfig.rest_api_base + '/custom/list_view',
                'GET',
                {
                    page : page
                },
                function(list) {
                    $scope.reservation_list = $.map(list, function(value, key) { return value });
                    $log.debug($scope.reservation_list+"hii..")
            }
                );
        }

        $scope.list = get_list;

        $scope.get_local_time = function(time) {
            $log.debug(time);
            var date = new Date(Date.parse(time));
            $log.debug(date)
            return date.toLocaleString();
        }


        // Controller destroyed when view is changed.
        $scope.$on('$destroy', function () { $interval.cancel(list_interval_promise); });

    }
]);
