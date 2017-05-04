'use strict';

angular.module('CalendarModule')
.controller('CalendarController', ['$stateParams','$log', '$scope', '$location', '$state', 'AuthService', 'RestInterfaceService','$uibModal',
    function($stateParams,$log, $scope, $location, $state, AuthService, RestInterfaceService,$uibModal) {

        $scope.AppConfig = AppConfig;
        $scope.AuthService = AuthService;
        $scope.range = _.range;
        $scope.submit = {};
        $scope.select_hide = true;
        $scope.start_iteration = -1;
        $scope.end_iteration = 49;
        var user_name = "";
        var total_time_slot = [];
        var not_opened = true;
        $scope.submit.current_date = new Date();
        var already_added_blade = {}

        $scope.submit.selected_chassis = null;
        $scope.submit.selected_blade = null;


         $scope.AuthService.logged_in(
            function(user){
                // Show list view if user is present
                if (user == null) {
                   return;
                }
                user_name = user.username;
                initialize_submit(user.groups);
            },
            // Show home view if no user is logged in
            function(){
                $state.transitionTo('home');
            }
        );

        function is_already_added(val)
        {
            if(already_added_blade[val]==1)
            {
                return true;
            }
            else
            {
                already_added_blade[val] = 1;
                return false;
            }
        }
        function populate_submit() {

            var blade_id = $stateParams.blade_id;
            var chassis_id = $stateParams.chassis_id;
            var hostname = $stateParams.hostname;
            var flag = $stateParams.flag ;
            console.log("Inside populate function blade_id :",blade_id,"chassis id:",chassis_id,"hostname :",hostname,"flag :",flag);
            if (blade_id == undefined || blade_id == "" || chassis_id == undefined || chassis_id == "") {
                return;
            }

            if (flag == 0 && $scope.calendar.blades.length > 0) {
                console.log("returning  .. flag == 0 here ");
                return;
            }

            $scope.submit.selected_blade = null;
            $scope.submit.selected_chassis = null;

            for (var index in $scope.submit.chassis_list) {
                var chassis = $scope.submit.chassis_list[index];
                if (chassis_id == chassis.id) {
                    $scope.submit.selected_chassis = chassis;
                }
            }

            if($scope.submit.selected_chassis != null)
            {

                for (var index in $scope.submit.blade_list) {
                    var blade = $scope.submit.blade_list[index];
                    if (blade_id == blade.id && flag==0) {
                        $scope.submit.selected_blade = blade;
                        console.log("only one slot is slected ..right ??");
                        break;
                    }
                    if(flag == 1 && blade.chassis.split("/")[5] == chassis_id)
                    {
                        if(is_already_added(blade.id))
                        {
                            console.log("already added blade status : ",already_added_blade,"bladde_id: ",blade.id,"continuing the loop");
                            continue;
                        }
                        console.log("chassis_id: ",blade.chassis.split("/")[5],chassis_id,blade.chassis);
                        $scope.submit.selected_blade = blade;
                         if ($scope.submit.selected_blade != null && $scope.submit.selected_chassis != null) {
                             $scope.submit.add_blade();
                             $scope.submit.selected_blade = null;
                        }
                    }
                }
            }


            if ($scope.submit.selected_blade == null || $scope.submit.selected_chassis == null) {
                return;
            }

            console.log("it is going to add_blade ",$scope.submit.selected_blade,$scope.submit.selected_chassis,"no null here .. i think");

            $scope.submit.add_blade();
        }


        function initialize_submit(groups) {
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
                            // console.log(blade);
                            $scope.submit.blade_list.push(blade);
                            chassis_url[blade.chassis] = blade.chassis;
                        }

                        for(var url in chassis_url) {
                            new RestInterfaceService(
                                chassis_url[url],
                                "GET",
                                {},
                                function(chassis) {
                                    $log.debug(chassis.hostname ,chassis.name,"printed the chassis list in calendar contoller ");
                                    chassis.name = chassis.name + " " + chassis.hostname;
                                    $scope.submit.chassis_list.push(chassis);
                                    $log.debug($scope.submit);
                                    populate_submit();
                                }
                            );
                        }
                    }
                );

            }
        };

        function slot_add(array, n) {
            array[n] = 1;
        }

        function slot_delete(array, n) {
            array[n] = 0;
        }

        function slot_has(array, n) {
            return array[n] == 1;
        }

        function get_offset(n)
        {
            if(n==15)
                return 1;
            if(n==30)
                return 2;
            if(n==45)
                return 3;
            if(n==0)
                return 0;
        }



        $scope.calendar = {

            time_slots : [
            '00:15','00:30','00:45','1:00',
            '1:15', '1:30', '1:45','2:00',
            '2:15', '2:30', '2:45','3:00',
            '3:15', '3:30', '3:45','4:00',
            '4:15', '4:30', '4:45','5:00',
            '5:15', '5:30', '5:45','6:00',
            '6:15', '6:30', '6:45','7:00',
            '7:15', '7:30', '7:45','8:00',
            '8:15', '8:30', '8:45','9:00',
            '9:15', '9:30', '9:45','10:00',
            '10:15', '10:30', '10:45','11:00',
            '11:15', '11:30', '11:45','12:00',
            ],

            blades : [],

            period: 'am',

            mouse_is_down : false,

            mouse_up : function() {
                $scope.calendar.mouse_is_down = false;
                $log.debug($scope.calendar.mouse_is_down);
            },

            mouse_down : function() {
                $scope.calendar.mouse_is_down = true;
                $log.debug($scope.calendar.mouse_is_down);
            },

            label_mark : function(n,blade)
            {
              if (n < 0  || n > 47) {
                   return "";
              }

              if ($scope.calendar.period == "pm" ) {
                  n += 48;
              }

               return blade.label_name[n];

            },

            time_slot_class : function (n, blade){
                // Decides what type of slot to present

                // Do not cross the timeslot limit.
                if (n < 0  || n > 47) {
                     return "";
                }


                if ($scope.calendar.period == "pm" ) {
                    n += 48;
                }


                var css_class = "calendar_time_slot_side_border ";

                if (slot_has(blade.other_reserved_slot.reserved_slot, n)){
                    css_class = "calendar_time_slot_other_reserved ";
                }
                else if (slot_has(blade.user_reserved_slot.reserved_slot,n)) {
                    css_class = "calendar_time_slot_user_reserved";
                }
                else if(slot_has(blade.selected_slot.reserved_slot,n)) {
                    css_class += "calendar_time_slot_selected "
                }
                else {
                    // Logic to render empty slot
                    css_class += "calendar_time_slot ";
                    if (n % 2 == 1){
                        css_class += "calendar_time_slot_bottom_border ";
                    }


                    if (n == 0 || n == 48) {
                        css_class += "calendar_time_slot_top_border "
                    }
                    // End of logic
                }

                return css_class;
            },

            add_slot : function(n, blade){
                // Adds a clicked slot into blade selected_slot

                $log.debug(n,"printed the indices",blade.user_reserved_slot.reserved_slot[n],"hiiii");
                $log.debug(blade.selected_slot.reserved_slot[n]);

                // Do not cross the timeslot limit.
                if (n < 0  || n > 47) {
                     return;
                }

                if($scope.calendar.period=='pm')
                {
                    n += 48;
               }

                if (slot_has(blade.user_reserved_slot.reserved_slot,n)||slot_has(blade.other_reserved_slot.reserved_slot,n)){
                    slot_delete(blade.selected_slot.reserved_slot,n);
                }
                else if(slot_has(blade.selected_slot.reserved_slot,n))
                {
                    slot_delete(blade.selected_slot.reserved_slot,n);
                }
                else {
                    slot_add(blade.selected_slot.reserved_slot,n);
                }

                 $log.debug(blade.selected_slot.reserved_slot[n]);

            },

            add_drag_slot: function(n, blade){

                 if ($scope.calendar.mouse_is_down == false) {
                    // If mouse is not down, do nothing
                    return;
                }
                this.add_slot(n, blade);
            },

            reserve_slots : function()
            {
                var modified = 0;
                for (var id in this.blades)
                {
                    var blade = this.blades[id];
                    $log.debug("i have printed the blade",blade);
                    var start_time = [],end_time = [] ;
                    for (var i = 0;i<=96 ;i++)
                    {
                        total_time_slot[i] = 0;

                    }

                    $log.debug(id,blade,"Outer loop");

                    for (var i=0;i<=96;i++)
                    {
                        if(blade.selected_slot.reserved_slot[i]==1)  // can be modified more ...!!
                        {
                            total_time_slot[i] = 1;
                            modified = 1;
                            $log.debug(i);
                        }
                    }
                    var flag = 0;
                    var k = 0,j=0;
                    $log.debug(blade+"printed the blade here  ",total_time_slot);
                    if(modified==1)
                    {
                        for(var i=0;i<=96;i++)
                        {
                            if(total_time_slot[i]==1&&flag==0)
                            {
                                if(i>47)
                                {
                                    var c =  parseInt($scope.calendar.time_slots[i - 48].split(":")[0]) + 12;
                                    start_time[k++] = c.toString() + ":" + $scope.calendar.time_slots[i - 48].split(":")[1];
                                    $log.debug("Index of start_Time is :",i,$scope.calendar.time_slots[i-48]);
                                    flag = 1;
                                }
                                else
                                {
                                    start_time[k++] = $scope.calendar.time_slots[i];
                                    $log.debug("Index of start_Time is :",i,$scope.calendar.time_slots[i]);
                                    flag = 1;
                                }
                            }
                            if(total_time_slot[i]==0&&flag==1)
                            {
                                if(i>48)
                                {
                                    var c =  parseInt($scope.calendar.time_slots[i - 49].split(":")[0]) + 12;
                                    end_time[j++] = c.toString() + ":" + $scope.calendar.time_slots[i - 49].split(":")[1];
                                    $log.debug("Index of end_time is :",i,$scope.calendar.time_slots[i-49]);
                                    flag = 0;
                                }
                                else
                                {
                                    end_time[j++] = $scope.calendar.time_slots[i-1];
                                    $log.debug("Index of end_time is :",i,$scope.calendar.time_slots[i]);
                                    flag = 0;
                                }
                            }
                        }

                        if(k==j)
                        {
                            $log.debug("yes both are always same",k-1);
                        }
                        else
                        {
                            $log.debug("No both are not same");
                        }



                        for(var i = 0;i<start_time.length;i++)
                        {
                            var start_datetime = new Date();
                            var end_datetime = new Date();

                            start_datetime.setMonth($scope.submit.current_date.getMonth());
                            start_datetime.setYear($scope.submit.current_date.getFullYear());
                            start_datetime.setDate($scope.submit.current_date.getDate());

                            end_datetime.setMonth($scope.submit.current_date.getMonth());
                            end_datetime.setYear($scope.submit.current_date.getFullYear());
                            end_datetime.setDate($scope.submit.current_date.getDate());

                            $log.debug(end_time[i],start_time[i],"this is one");


                            start_datetime.setHours(parseInt(start_time[i].split(':')[0]));
                            end_datetime.setHours(parseInt(end_time[i].split(":")[0]));
                            $log.debug("i am here",start_datetime,end_datetime,2);

                            start_datetime.setMinutes(parseInt(start_time[i].split(":")[1]) - 15);
                            start_datetime.setSeconds(0);
                            $log.debug(start_datetime);

                            end_datetime.setMinutes(end_time[i].split(':')[1]);
                            end_datetime.setSeconds(0);

                            $log.debug("going to call rest api now ...",blade.id,start_datetime,end_datetime);
                            new RestInterfaceService(
                                AppConfig.rest_api_base + '/custom/record_submit',
                                'POST',
                                {
                                     blade_id : blade.id,
                                     start_time : start_datetime,
                                     end_time : end_datetime,
                                },
                                function(result,current_blade)
                                {
                                    $log.debug(result);

                                    if(result['status']=='failed')
                                    {

                                        for (var i=0;i<=96;i++)  //This bug is fixed just use start_time.indexOf() to end_time.indexOf()
                                        {

                                            if(blade.selected_slot.reserved_slot[i]==1&&(!slot_has(blade.user_reserved_slot.reserved_slot,i)))
                                            {
                                                slot_delete(blade.selected_slot.reserved_slot,i);
                                                slot_delete(blade.user_reserved_slot.reserved_slot,i);
                                            }
                                        }

                                        alert("failed request",result.start_time,result.end_time);
                                    }
                                    if(result['status']=='success')
                                    {
                                        $log.debug("inside success block",current_blade);

                                        for (var i=0;i<=96;i++)
                                        {
                                            if(current_blade.selected_slot.reserved_slot[i]==1)
                                            {
                                                $log.debug(i,start_time[i],blade);
                                                // slot_add(blade.user_reserved_slot.reserved_slot,i);
                                                current_blade.user_reserved_slot.reserved_slot[i] = 1;
                                                current_blade.selected_slot.reserved_slot[i] = 0;
                                            }

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
                                                return "Chassis Reserved";
                                            },
                                            message: function()
                                            {
                                                return "Added Successfully .. ";
                                            }
                                            ,
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

                                        $log.debug(result.status);
                                    }
                                },
                                function()
                                {

                                },
                                blade
                            );

                        }  // different bundle in a blade
                        modified = 0;

                    }  // modified block

                } // iterating for number of blades added

            }   // end of reserve  slot function


        }; // scope.calendar end


        $scope.submit.add_blade = function()
        {
            $scope.select_hide = false;
            var name = $scope.submit.selected_blade;
            if(name != null || $scope.submit.selected_chassis != null) {
                is_already_open($scope.submit.selected_blade,$scope.submit.selected_chassis.hostname);
                if (!not_opened) {
                    // check to ensure that if there is already opened instance is there ...!!  
                    return;
                }
                var blade = {};
                // to get the hostname to display in web-page
                for(var i=0;i<$scope.submit.chassis_list.length;i++)
                {
                    if($scope.submit.selected_blade.chassis===$scope.submit.chassis_list[i].url)
                    {
                        $log.debug("yes matched",$scope.submit.selected_blade.name,$scope.submit.chassis_list[i].hostname);
                        blade.hostname = $scope.submit.chassis_list[i].hostname;
                    }
                }

                blade.id = $scope.submit.selected_blade.id;
                blade.name = $scope.submit.selected_blade.name;

                blade.selected_slot = {};
                blade.selected_slot.reserved_slot = [];

                blade.other_reserved_slot = {};
                blade.other_reserved_slot.reserved_slot = [];

                blade.user_reserved_slot = {};
                blade.user_reserved_slot.reserved_slot = [];

                blade.label_name = [];
                load_data(blade);
                $scope.calendar.blades.push(blade);
                //$scope.submit.selected_blade = null;


            }
            else
            {
                alert("Please Select Chassis and Blade for which you want to add ..");
            }

        };

        $scope.submit.date_increase_decrease = function(value)
        {
            $log.debug("Entered the arena");
            $scope.submit.current_date.setDate($scope.submit.current_date.getDate() + value);
            var j = 0;
            $log.debug($scope.calendar.blades.length,$scope.calendar.blades,$scope.calendar.blades[0]);
            for(j = 0; j < $scope.calendar.blades.length ; j++)
            {
                $log.debug(j,$scope.calendar.blades[j].user_reserved_slot,$scope.calendar.blades[j].user_reserved_slot.reserved_slot[4],"printed here before call to rest interface");
                load_data($scope.calendar.blades[j]);
            }
        }

        function load_data(blade)
        {

            $scope.submit.current_date.setHours(0);
            $scope.submit.current_date.setMinutes(0);
            function populate(username,blade_username,start_index,end_index,blade)
            {
              if(username == blade_username)
              {

                  for (var k=start_index ; k<=end_index;k++)
                  {

                      blade.user_reserved_slot.reserved_slot[k] = 1;
                  }

              }
              else
              {
                  for (var k=start_index ; k<=end_index;k++)
                  {
                      if(k==start_index)
                      {
                        blade.label_name[k] = blade_username;
                      }
                      blade.other_reserved_slot.reserved_slot[k] = 1;
                  }
              }
            }

            for (var i=0;i<96;i++)
            {
              blade.user_reserved_slot.reserved_slot[i] = 0;
              blade.other_reserved_slot.reserved_slot[i] = 0;
              blade.selected_slot.reserved_slot[i] = 0;
              blade.label_name[i] = null;
            }
            // var blade = $scope.calendar.blades[j];

            new RestInterfaceService(
                     AppConfig.rest_api_base + '/custom/calendar_view',
                                'GET',
                                {
                                    blade_id :blade.id,
                                    date:$scope.submit.current_date,
                                },
                                function(result)
                                {
                                    for(i in result)
                                    {


                                            // $log.debug(typeof(result[i].case),typeof(result[i].start_time),username);

                                            var start_time = new Date(result[i].start_time);
                                            $log.debug(start_time);
                                            start_time.setMinutes(start_time.getMinutes() - (start_time.getMinutes()%15));

                                            var end_time = new Date(result[i].end_time);
                                            end_time.setMinutes((end_time.getMinutes()%15)!=0 ? end_time.getMinutes() + (15 - (end_time.getMinutes()%15)) : end_time.getMinutes());
                                            $log.debug(end_time.getMinutes(),"this is minutes");
                                            var start_index = 0, start_offset = 0, end_index = 0, end_offset = 0;

                                            // Case 1: when start time and end time is in betwwen todays start_time and end_time
                                            if(result[i].case == 1)
                                            {

                                                start_offset = get_offset(start_time.getMinutes());
                                                start_index = start_time.getHours()*4 + start_offset ;

                                                end_offset = get_offset(end_time.getMinutes());
                                                end_index = end_time.getHours()*4 + end_offset - 1;
                                                populate(user_name,result[i].user_name,start_index,end_index,blade);
                                                $log.debug("i  came here ",end_time,end_time.getHours(),start_index,end_index,start_offset,start_time,start_time.getMinutes());




                                            }
                                            // Case 2: when start time is less than todays start time but end_time is in between start time and end_time
                                            else if(result[i].case == 2 )
                                            {


                                                start_index = 0;
                                                end_offset = get_offset(end_time.getMinutes());
                                                end_index = end_time.getHours()*4 + end_offset - 1;
                                                populate(user_name,result[i].user_name,start_index,end_index,blade);
                                                $log.debug(start_time.getHours(),"we are in case 2",start_index,end_index);

                                            }
                                            // Case 3: when start time is in between todays start time and end time ... and end time is greater than today end time
                                            else if(result[i].case == 3)
                                            {

                                                $log.debug(start_time.getHours());
                                                start_offset = get_offset(start_time.getMinutes());
                                                start_index = start_time.getHours()*4 + start_offset ;
                                                end_index = 96;
                                                populate(user_name,result[i].user_name,start_index,end_index,blade);

                                            }
                                            // Case 4: when start time is less than todays start time and end time is greater than todays end time
                                            else if(result[i].case == 4)
                                            {
                                                $log.debug(start_time.getHours());
                                                start_index = 0;
                                                end_index = 96;
                                                populate(user_name,result[i].user_name,start_index,end_index,blade);

                                            }

                                            // 0 2/29/2016, 5:44:57 PM 3/1/2016, 5:44:57 PM aaaa
                                    }

                                    $log.debug("Succesfully reserved",result);
                                }
                            );
        }


        function is_already_open(blade,hostname)
        {
            for(var i = 0; i< $scope.calendar.blades.length ; i++)
            {
                if(blade == null||($scope.calendar.blades[i].id == blade.id))
                {
                    // alert("there is already opened instance for the same or chassis is not selected ...");
                    var modalInstance = $uibModal.open({
                                        animation: true,
                                        templateUrl: AppConfig.base_path + 'modal/views/view-modal.htm',
                                        controller: 'ModalInstanceCtrl',
                                        resolve: {
                                            data: function () {
                                                return null;
                                            },
                                            title: function () {
                                                return "Already Opened";
                                            },
                                            message: function()
                                            {
                                                return "There is already a opened instance for the same request ..! ";
                                            }
                                            ,
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
                    not_opened = false;
                    return;

                }
                else{
                    $log.debug("not matched",$scope.calendar.blades[i].name,blade.name,$scope.calendar.blades[i].hostname,hostname);
                }
            }

            not_opened = true;
            return;
        }


    // };

    }
]);
