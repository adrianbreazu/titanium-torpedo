// attach click events
(function() {
    $('#grass_front').click(function() {
        if ($(this).attr('class') != "select-area") {
            startRelay('A', 1);
            $(this).attr('class', 'select-area');
        } else {
            startRelay('A', 0);
            $(this).attr('class', '');
        }
    });

    $('#grass_back').click(function() {
        if ($(this).attr('class') != "select-area") {
            startRelay('B', 1);
            $(this).attr('class', 'select-area');
        } else {
            startRelay('B', 0);
            $(this).attr('class', '');
        }
    });

    $('#flowers').click(function() {
        if ($(this).attr('class') != "select-area") {
            startRelay('D', 1);
            $(this).attr('class', 'select-area');
        } else {
            startRelay('D', 0);
            $(this).attr('class', '');
        }
    });

    $('#grass_side').click(function() {
        if ($(this).attr('class') != "select-area") {
            startRelay('C', 1);
            $(this).attr('class', 'select-area');
        } else {
            startRelay('C', 0);
            $(this).attr('class', '');
        }
    });
})();

// getRelay status on first run
(function() {
    $.ajax({
        url: 'http://127.0.0.1:8080/sensors_actuators/getRelayStatus/',
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: "{}",
        async: false,
        success: function(response) {
            //set status
            if (response['Relay_A'] == 0)
                $('#grass_front').attr('class', '');
            else
                $('#grass_front').attr('class', 'select-area');

            if (response['Relay_B'] == 0)
                $('#grass_back').attr('class', '');
            else
                $('#grass_back').attr('class', 'select-area');

            if (response['Relay_D'] == 0)
                $('#flowers').attr('class', '');
            else
                $('#flowers').attr('class', 'select-area');

            if (response['Relay_C'] == 0)
                $('#grass_side').attr('class', '');
            else
                $('#grass_side').attr('class', 'select-area');

        },
        error: function(error) {
            console.log(error);
        }
    });
})();

// setRelay code
function startRelay(relayId, status) {
    $.ajax({
        url: 'http://127.0.0.1:8080/sensors_actuators/setRelayStatus/',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: '{"Relay":\"' + relayId + '\", "Status":' + status + '}',
        async: false,
        success: function(response) {},
        error: function(error) {
            console.log(error);
        }
    });
}