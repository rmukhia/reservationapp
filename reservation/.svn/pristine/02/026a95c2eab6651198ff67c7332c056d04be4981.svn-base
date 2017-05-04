'use strict';

angular.module('RecordsModule')
.controller('RecordsController', ['$stateParams','$log', '$scope', '$location', '$state', '$interval', '$uibModal',
    'AuthService', 'RestInterfaceService',
    function($stateParams,$log, $scope, $location, $state, $interval, $uibModal, AuthService, RestInterfaceService) {


        $scope.AppConfig = AppConfig;
        $scope.AuthService = AuthService;
        $scope.RestInterfaceService = RestInterfaceService;
        $scope.records_table = {};
        $scope.submit = {};
        $scope.modal = {};
        $scope.modal.info = {};
        $scope.modal.remove = {};
        $scope.submit.start_time = {};
        $scope.submit.end_time = {};
        $scope.submit.invalid_input = false;

        $scope.submit.start_time.date_format = "dd-MMMM-yyyy";
        $scope.submit.start_time.min_date = new Date();
        $scope.submit.start_time.max_date = new Date(2020, 5, 22);
        $scope.submit.start_time.date = new Date();
        $scope.submit.start_time.time = new Date();

        $scope.submit.end_time.date_format = "dd-MMMM-yyyy";
        $scope.submit.end_time.min_date = new Date();
        $scope.submit.end_time.max_date = new Date(2020, 5, 22);
        $scope.submit.end_time.date = new Date();
        $scope.submit.end_time.time = new Date();
        $scope.submit.end_time.time.setHours(20);
        $scope.submit.end_time.time.setMinutes(0);



        var page = 1;
        var list_interval_promise
         // Authenticated User can view
        $scope.AuthService.logged_in(
            function(user){
                // Show list view if user is present
                if (user == null) {
                   return;
                }
                initialize_submit(user.groups);
                get_records(page);
                $log.debug("i am reaching here");
                var interval_time = 1000 * 15; // 30 seconds
                list_interval_promise = $interval(function(){
                    get_records($scope.records_table.page);
                    },
                    interval_time
                );
        },
            // Show home view if no user is logged in
            function(){
                $state.transitionTo('home');
            }
        );

        $scope.records_table.get_pagination_class = function(page) {
            return (page == $scope.records_table.page)? 'active': '';
        }

        function get_records(page){
            new  RestInterfaceService(
                AppConfig.rest_api_base + '/custom/records_view',
                'GET',
                {
                    page : page,
                    search_string : $scope.submit.search_string,
                },
                function(list) {
                    $scope.records_table.num_pages = parseInt(list.num_pages);
                    $scope.records_table.page = parseInt(list.page);
                    $log.debug("printing list.pages",parseInt(list.page));
                    $scope.records_table.total_records = parseInt(list.total_records);
                    $scope.records_table.records_per_page = parseInt(list.records_per_page);
                    $scope.records_table.records = list.records;
                    $log.debug(list);
                    // $scope.records_table.page += 1;
                }
            );
        }

        $scope.records_table.get_records = get_records;


        function populate_submit() {
            var blade_id = $stateParams.blade_id;
            var chassis_id = $stateParams.chassis_id;

            if (blade_id == undefined || blade_id == "" || chassis_id == undefined || chassis_id == "") {
                return;
            }

            if ($scope.submit.selected_blade != null && $scope.submit.selected_chassis != null) {
                $log.info($scope.submit.selected_blade,$scope.submit.selected_chassis,"here  i printed the stuff ...");
                return;
            }

            for (var index in $scope.submit.blade_list) {
                var blade = $scope.submit.blade_list[index];
                if (blade_id == blade.id) {
                    $scope.submit.selected_blade = blade;
                }
            }

            for (var index in $scope.submit.chassis_list) {
                var chassis = $scope.submit.chassis_list[index];
                if (chassis_id == chassis.id) {
                    $scope.submit.selected_chassis = chassis;
                }
            }
        }

        // List all the blades and chassis that belongs to users groups
        function initialize_submit(groups)
        {
            $scope.submit.blade_list = [];
            $scope.submit.chassis_list = [];
            $scope.submit.selected_start_time = "";
            $scope.submit.selected_end_time = "";
            var chassis_url = {};
            // loop over all the groups
            for (var id in groups) {
                var group = groups[id];
                new  RestInterfaceService(
                    AppConfig.rest_api_base + '/blades/search',
                    'GET',
                    {
                        group : group['id'],
                    },
                    function(blade_result) {
                        for (var key in blade_result) {
                            var blade = blade_result[key];
                            $scope.submit.blade_list.push(blade);
                            chassis_url[blade.chassis] = blade.chassis;
                        }

                        for(var url in chassis_url) {
                            new RestInterfaceService(
                                url,
                                "GET",
                                {},
                                function(chassis) {
                                    $log.debug(chassis.hostname,"printed chassis here ...");
                                    chassis['name'] =  chassis.name + " " + chassis.hostname;
                                    $scope.submit.chassis_list.push(chassis);
                                    $log.debug($scope.submit.chassis_list,"printed chassis list here ");
                                    populate_submit();
                                }
                            );

                        }
                    }
                );

            }
        };

        $scope.submit.initialize_submit = initialize_submit;

        $scope.submit.add = function() {
          if ($scope.submit.start_time.date && $scope.submit.end_time.date &&
            $scope.submit.start_time.time && $scope.submit.end_time.time &&
            $scope.submit.selected_blade && $scope.submit.selected_chassis)
          {
            var start_time = $scope.submit.start_time.time;
            start_time.setFullYear($scope.submit.start_time.date.getFullYear());
            start_time.setMonth($scope.submit.start_time.date.getMonth());
            start_time.setDate($scope.submit.start_time.date.getDate());
            start_time.setSeconds(0);

            var end_time =  $scope.submit.end_time.time;
            end_time.setFullYear($scope.submit.end_time.date.getFullYear());
            end_time.setMonth($scope.submit.end_time.date.getMonth());
            end_time.setDate($scope.submit.end_time.date.getDate());
            end_time.setSeconds(0);

            $log.debug(start_time,end_time,$scope.submit.selected_blade.id);
            new RestInterfaceService(
                AppConfig.rest_api_base + '/custom/record_submit',
                'POST',
                {
                    blade_id : $scope.submit.selected_blade.id,
                    start_time : start_time,
                    end_time : end_time
                },
                function(result) {
                    $log.debug(result);
                    var title = '';
                    var message = '';
                    switch (result['status']) {
                        case 'failed':
                            title = "Time Slot Already Reserved";
                            message = "The time slot you are requesting is already reserved by " +
                                    result['user'] + ".";
                            message += " Reservation will end at " + new Date(result['end_time']).toLocaleString();
                            break;
                        case 'invalid_input':
                            title = "Invalid Input";
                            message = "The start time is after the end time.";
                            break;
                        case 'success':
                            title = "Success";
                            message = "Added Successfully ..";
                            break;
                        default:
                            title = "Unknown Response";
                            message =  result['status'];
                    }
                    var modalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: AppConfig.base_path + 'modal/views/view-modal.htm',
                        controller: 'ModalInstanceCtrl',
                        resolve: {
                            data: function () {
                                return null;
                            },
                            title: function () {
                                return title;
                            },
                            message: function() {
                                return message;
                            },
                            show_cancel: function() {
                                return false;
                            },
                            ok_text: function() {
                                return "Ok";
                            },
                            cancel_text: function(){
                                return null;
                            }
                        }
                    });

                    modalInstance.result.then(function (data) {
                    }, function () {
                    });

                    $scope.submit.invalid_input = false;
                });
            }
            else {
                $scope.submit.invalid_input = true;
            }
            return false;
        };


        $scope.modal.remove.open = function (record) {
            var record_id = record.record.toString();
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: AppConfig.base_path + 'modal/views/view-modal.htm',
                controller: 'ModalInstanceCtrl',
                resolve: {
                    data: function () {
                        return record_id;
                    },
                    title: function () {
                        return "Delete";
                    },
                    message: function() {
                        return "Do you really want to delete?";
                    },
                    show_cancel: function() {
                        return true;
                    },
                    ok_text: function() {
                        return "Yes";
                    },
                    cancel_text: function() {
                        return "No";
                    }
                }
            });

            modalInstance.result.then(function (record_id) {
                new RestInterfaceService(
                AppConfig.rest_api_base + '/records/'+ record_id +'/',
                "DELETE",
                {},
                function(response)
                {
                    get_records($scope.records_table.page);
                   //success_callback
                },
                function(response)
                {
                   //faliure_callback
                   alert("something went wrong in deletion")
                });
            }, function () {
            });
        };


        $scope.disable = function (row){
            var btnclass = 'btn btn-primary';
            if(row.userid != $scope.AuthService.user.id)
            {
                btnclass += ' disabled';
            }


            return btnclass;
        }

        // Controller destroyed when view is changed.
        $scope.$on('$destroy', function () { $interval.cancel(list_interval_promise); });
    }
]);
