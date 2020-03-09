var lat = 40.7128;
var long = 74.0060;
$(function(){
	$('button').click(function(){
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                lat = position.coords.latitude;
                long = position.coords.longitude;
            });
        }
		$.ajax({
			url: '/getlocation',
            data: {'location' : lat + "," + long},
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});

