$(document).ready(function () {

    // alert('heyooo');

    function initialize() {
        var input = document.getElementById('searchTextField');
        var autocomplete = new google.maps.places.Autocomplete(input);


        google.maps.event.addListener(autocomplete, 'place_changed', function () {
            var place = autocomplete.getPlace();
            console.log(place)
            $('#searchTextField').attr("data-lat", place.geometry.location.lat()).attr("data-long", place.geometry.location.lng())
            var formattedAddress = place.formatted_address;
            var individualAddressComponents = formattedAddress.split(',');
            var stateString = individualAddressComponents[2];
            var state = stateString.substring(0, 3);
            var zip = stateString.substring(4, 9)
        });
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                var geolocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                var circle = new google.maps.Circle({
                    center: geolocation,
                    radius: position.coords.accuracy
                });
                autocomplete.setBounds(circle.getBounds());
            });
        }
    }
    google.maps.event.addDomListener(window, 'load', initialize);
    $('#image_update').click(function () {
        console.log('clicked_image')
        $('#images').click();
    });

    var centreGot = false;
})
