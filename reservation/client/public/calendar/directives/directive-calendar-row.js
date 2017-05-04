'use strict';

angular.module('CalendarModule')
.directive('customCalendarRow', function() {
  return {
    templateUrl: AppConfig.base_path + 'calendar/views/view-calendar-row.htm'
  };
});