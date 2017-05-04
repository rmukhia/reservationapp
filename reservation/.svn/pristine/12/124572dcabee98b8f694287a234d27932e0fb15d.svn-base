angular.module('BaseModule').filter("get_locale_time", function(){
   return function(time_string){
    if (time_string) {
    	// $log.info("time string in base.filter"+time_string);
      var date = new Date(time_string);
      return date.toLocaleString();
    }
    else {
        return '';
    }
   }
});