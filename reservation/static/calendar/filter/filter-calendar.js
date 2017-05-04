angular.module('CalendarModule').filter('get_Date',function()
{
	return function(time_string)
	{
		if(time_string)
		{
			var date = new Date(time_string);
			return date.getDate()+"-"+parseInt(date.getMonth()+1)+"-"+date.getFullYear();
		}
		else
		{
			return '';
		}
	}
});