(function() {
    var $relay_div = $("#relays_div");
    // create relay divs
    $.ajax({
        url: 'http://127.0.0.1:8080/sensors_actuators/getRelayStatus/',
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: "{}",
        async: false,
        success: function(response) {
            // set Relay A
            var div_relay_A = $('<div>').addClass("checkbox").appendTo($relay_div);
            $("<input>").attr('type', 'checkbox').attr('data-toggle', 'toggle').
            attr('data-on', 'Relay A started').attr('data-off', 'Relay A stopped').
            attr('data-onstyle', 'danger').attr('data-offstyle', 'success').
            attr('id', 'relay_A').attr('data-relay-name', 'A').appendTo(div_relay_A);
            // set Relay B
            var div_relay_B = $('<div>').addClass("checkbox").appendTo($relay_div);
            $("<input>").attr('type', 'checkbox').attr('data-toggle', 'toggle').
            attr('data-on', 'Relay B started').attr('data-off', 'Relay B stopped').
            attr('data-onstyle', 'danger').attr('data-offstyle', 'success').
            attr('id', 'relay_B').attr('data-relay-name', 'B').appendTo(div_relay_B);
            // set Relay C
            var div_relay_C = $('<div>').addClass("checkbox").appendTo($relay_div);
            $("<input>").attr('type', 'checkbox').attr('data-toggle', 'toggle').
            attr('data-on', 'Relay C started').attr('data-off', 'Relay C stopped').
            attr('data-onstyle', 'danger').attr('data-offstyle', 'success').
            attr('id', 'relay_C').attr('data-relay-name', 'C').appendTo(div_relay_C);
            // set Relay D
            var div_relay_D = $('<div>').addClass("checkbox").appendTo($relay_div);
            $("<input>").attr('type', 'checkbox').attr('data-toggle', 'toggle').
            attr('data-on', 'Relay D started').attr('data-off', 'Relay D stopped').
            attr('data-onstyle', 'danger').attr('data-offstyle', 'success').
            attr('id', 'relay_D').attr('data-relay-name', 'D').appendTo(div_relay_D);
            // set Relay E
            var div_relay_E = $('<div>').addClass("checkbox").appendTo($relay_div);
            $("<input>").attr('type', 'checkbox').attr('data-toggle', 'toggle').
            attr('data-on', 'Relay E started').attr('data-off', 'Relay E stopped').
            attr('data-onstyle', 'danger').attr('data-offstyle', 'success').
            attr('id', 'relay_E').attr('data-relay-name', 'E').appendTo(div_relay_E);
            // set Relay Reset
            var div_relay_Reset = $('<div>').addClass("checkbox").appendTo($relay_div);
            $("<input>").attr('type', 'checkbox').attr('data-toggle', 'toggle').
            attr('data-on', 'Reset all started').attr('data-off', 'Reset all stopped').
            attr('data-onstyle', 'danger').attr('data-offstyle', 'success').
            attr('id', 'relay_Reset').attr('data-relay-name', 'Reset').appendTo(div_relay_Reset);

            //set status
            if (response['Relay_A'] == 0)
                $('#relay_A').bootstrapToggle('off');
            else
                $('#relay_A').bootstrapToggle('on');
            if (response['Relay_B'] == 0)
                $('#relay_B').bootstrapToggle('off');
            else
                $('#relay_B').bootstrapToggle('on');
            if (response['Relay_C'] == 0)
                $('#relay_C').bootstrapToggle('off');
            else
                $('#relay_C').bootstrapToggle('on');
            if (response['Relay_D'] == 0)
                $('#relay_D').bootstrapToggle('off');
            else
                $('#relay_D').bootstrapToggle('on');
            if (response['Relay_E'] == 0)
                $('#relay_E').bootstrapToggle('off');
            else
                $('#relay_E').bootstrapToggle('on');
            $('#relay_Reset').bootstrapToggle('off');
        },
        error: function(error) {
            console.log(error);
        }
    });

    $("#relay_A").change(function() {
        $.ajax({
            url: 'http://127.0.0.1:8080/sensors_actuators/setRelayStatus/',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: '{"Relay":"A", "Status":' + $(this).prop('checked') + '}',
            async: false,
            success: function(response) {
                console.log(response)
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $("#relay_B").change(function() {
        $.ajax({
            url: 'http://127.0.0.1:8080/sensors_actuators/setRelayStatus/',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: '{"Relay":"B", "Status":' + $(this).prop('checked') + '}',
            async: false,
            success: function(response) {
                console.log(response)
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $("#relay_C").change(function() {
        $.ajax({
            url: 'http://127.0.0.1:8080/sensors_actuators/setRelayStatus/',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: '{"Relay":"C", "Status":' + $(this).prop('checked') + '}',
            async: false,
            success: function(response) {
                console.log(response)
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $("#relay_D").change(function() {
        $.ajax({
            url: 'http://127.0.0.1:8080/sensors_actuators/setRelayStatus/',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: '{"Relay":"D", "Status":' + $(this).prop('checked') + '}',
            async: false,
            success: function(response) {
                console.log(response)
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $("#relay_E").change(function() {
        $.ajax({
            url: 'http://127.0.0.1:8080/sensors_actuators/setRelayStatus/',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: '{"Relay":"E", "Status":' + $(this).prop('checked') + '}',
            async: false,
            success: function(response) {
                console.log(response)
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $("#relay_Reset").change(function() {
        if ($(this).prop('checked'))
            $.ajax({
                url: 'http://127.0.0.1:8080/sensors_actuators/resetRelays/',
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json',
                data: '{}',
                async: false,
                success: function(response) {
                    setTimeout(function() {
                        if (response['Relay_A'] == 0)
                            $('#relay_A').bootstrapToggle('off');
                        else
                            $('#relay_A').bootstrapToggle('on');
                        if (response['Relay_B'] == 0)
                            $('#relay_B').bootstrapToggle('off');
                        else
                            $('#relay_B').bootstrapToggle('on');
                        if (response['Relay_C'] == 0)
                            $('#relay_C').bootstrapToggle('off');
                        else
                            $('#relay_C').bootstrapToggle('on');
                        if (response['Relay_D'] == 0)
                            $('#relay_D').bootstrapToggle('off');
                        else
                            $('#relay_D').bootstrapToggle('on');
                        if (response['Relay_E'] == 0)
                            $('#relay_E').bootstrapToggle('off');
                        else
                            $('#relay_E').bootstrapToggle('on');
                        $('#relay_Reset').bootstrapToggle('off');
                    }, 1000);
                },
                error: function(error) {
                    console.log(error);
                }
            });
    });

})();