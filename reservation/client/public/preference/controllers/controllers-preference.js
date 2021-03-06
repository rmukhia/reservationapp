'use strict';

angular.module('PreferenceModule')
.controller('PreferenceController', ['$log', '$scope', '$location', '$state', '$interval', 'AuthService', 'RestInterfaceService','$http','$uibModal','Upload','$timeout','$window',
    function($log, $scope, $location, $state, $interval, AuthService, RestInterfaceService,$http,$uibModal,Upload,$timeout,$window) {
        
         
        $scope.AppConfig = AppConfig;
        $scope.AuthService = AuthService;
        $scope.RestInterfaceService = RestInterfaceService;
        $scope._ = _;
        $scope.submit = {};
        $scope.submit.timezone = {};
        var bool_value;
        $scope.submit.info = {};
        $scope.submit.password = {};
        $scope.modal = {};


 
         // Authenticated User can view      
        $scope.AuthService.logged_in(
            function(user){
                // Show list view if user is present
                if (user == null) {
                   return;
                }
                initialize_submit(user);
            },
            // Show home view if no user is logged in
            function(){
                $state.transitionTo('home');
            }
        );

        function initialize_submit(user){
            // Initialize the user info
            $scope.submit.info.first_name = user.first_name;
            $scope.submit.info.last_name = user.last_name;
            $scope.submit.info.email = user.email;

            new RestInterfaceService(
                AppConfig.rest_api_base + '/preferences/search/',
                'GET',
                {
                    user : user.id,
                },
                function(result){
                    console.log(result[0],"printed the console");
                    switch (result['url']) {
                        case 'failed':
                            $scope.submit.timezone.positive  = "true";
                            $scope.submit.timezone.hours  = 0;
                            $scope.submit.timezone.minutes  = 0;
                            $scope.submit.notification = 'true';
                            $scope.submit.mail_group = 'aa';
                            break;
                        default:
                            $scope.submit.timezone.positive  = result[0].timezone_positive.toString();
                            $scope.submit.timezone.hours  = result[0].timezone_hours;
                            $scope.submit.timezone.minutes  = result[0].timezone_minutes;
                            $scope.submit.notification = result[0].mail_status.toString();
                            $scope.submit.mail_group = result[0].dl_group;
                    }
                    
                });      
        }

        $scope.submit.basic_info = function ()
        {
             var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: AppConfig.base_path + 'modal/views/view-modal.htm',
                controller: 'ModalInstanceCtrl',
                resolve: { 
                     data: function () {
                        return null;
                    },
                    title: function () {
                      return "Update Basic Info";
                    },

                    message: function() {
                      return "Do you really want to Update?";
                    },

                    show_cancel: function() {
                      return true;
                    },

                    ok_text: function() {
                        return "Ok";
                    },
                    cancel_text: function(){
                        return "Cancel";
                    }
                }
            });
            modalInstance.result.then(function ()
               {
                 new RestInterfaceService(
                    AppConfig.rest_api_base + '/custom/basic_info_submit',
                    'PUT',
                    {
                        first_name:$scope.submit.info.first_name,
                        last_name:$scope.submit.info.last_name,
                        email:$scope.submit.info.email,
                    },
                    function(status)
                    {
                       alert("Successfully updated");
                    }
                );
             },
             function () {
            });
        };


        $scope.submit.timezone.update_info = function()
        {
			var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: AppConfig.base_path + 'modal/views/view-modal.htm',
                controller: 'ModalInstanceCtrl',
                resolve: { 
                     data: function () {
                        return null;
                    },
                    title: function () {
                      return "Update Timezone";
                    },

                    message: function() {
                      return "Do you really want to Update Timezone?";
                    },

                    show_cancel: function() {
                      return true;
                    },

                    ok_text: function() {
                        return "Ok";
                    },
                    cancel_text: function(){
                        return "Cancel";
                    },
                }
            });
		modalInstance.result.then(function ()
		{
            console.log($scope.submit.mail_group,"printed the mail group");
            if($scope.submit.mail_group == undefined)
            {
                $scope.submit.mail_group = '';
            }
            new RestInterfaceService(
                AppConfig.rest_api_base + '/custom/preference_submit',
                 'PUT',
                {
                    timezone_positive:$scope.submit.timezone.positive,
                    timezone_hours: $scope.submit.timezone.hours,
                    timezone_minutes: $scope.submit.timezone.minutes,
                    notification_status : $scope.submit.notification,
                    dl_group : $scope.submit.mail_group,
                 },
                function()
                {
                    alert("Successfully updated..");
                    
                }
            );
		},
		function(){

        });
};

     $scope.submit.update_password = function()
     {
        var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: AppConfig.base_path + 'modal/views/view-modal.htm',
                controller: 'ModalInstanceCtrl',
                resolve: { 
                     data: function () {
                        return null;
                    },
                    title: function () {
                      return "Update Password";
                    },

                    message: function() {
                      return "Do you really want to Update Password?";
                    },

                    show_cancel: function() {
                      return true;
                    },

                    ok_text: function() {
                        return "Ok";
                    },
                    cancel_text: function(){
                        return "Cancel";
                    },
                }
            });

        modalInstance.result.then(function ()
        {
            if($scope.submit.password === $scope.submit.re_password)
            {
                new RestInterfaceService(
                    AppConfig.rest_api_base + '/custom/password_submit',
                    'PUT',
                    {
                        password:$scope.submit.password,
                    },
                    function(status)
                    {
                        alert("You are now Logged Out ...!! Login with new Password");
                        $scope.AuthService.logged_in(
                        function(user){
                        // Show list view if user is present
                        if (user == null) {
                            return;
                        }
                         initialize_submit(user);
                        },
                    // Show home view if no user is logged in
                        function(){
                            $state.transitionTo('home');
                        }
                     ); 
                        
                    }

                );
            }
            else
            {
                alert("Password Mismatched ...");
            }
        },
        function(){

        });
    };


    $scope.uploadFiles = function(file, errFiles) {
        $scope.f = file;
        $scope.errFile = errFiles && errFiles[0];
        if (file) {
            file.upload = Upload.upload({
                url:  AppConfig.rest_api_base + '/custom/image_submit',
                data: {file: file}
            });

            file.upload.then(function (response) {
                // $window.location.href = 'http://ixin-bitwise:8000/#/preference';
                var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: AppConfig.base_path + 'modal/views/view-modal.htm',
                controller: 'ModalInstanceCtrl',
                resolve: { 
                     data: function () {
                        return null;
                    },
                    title: function () {
                      return "Photo Upload";
                    },

                    message: function() {
                      return "Photo Uploaded Successfully .. ";
                    },

                    show_cancel: function() {
                      return false;
                    },

                    ok_text: function() {
                        return "Ok";
                    },
                    cancel_text: function(){
                        return "Cancel";
                    },
                }
                });

                $timeout(function () {
                    file.result = response.data;

                });

                $scope.AuthService.logged_in(
                    function(user){
                    // Show list view if user is present
                    if (user == null) {
                        return;
                    }
                    initialize_submit(user);
                },
                // Show home view if no user is logged in
                function(){
                    $state.transitionTo('home');
                }
            );    
            }, function (response) {
                if (response.status > 0)
                    $scope.errorMsg = response.status + ': ' + response.data;
            }, function (evt) {
                 file.progress = Math.min(100, parseInt(100.0 * 
                                         evt.loaded / evt.total));
                 $log.debug("i am here ...");
                 
            }
          );
        }   
    }


    }
]);






