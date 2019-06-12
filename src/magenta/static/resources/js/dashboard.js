var selected_iot_id = 1;

(function() {
    var $iot_list = $('#iot_list');
    $.ajax({
        url: host_url + '/sensors_actuators/get_iots/',
        type: "POST",
        data: "{}",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        async: false,
        success: function(message) {
            var message_array = message['iot'];
            $.each(message_array, function(index, val) {
                var iot_id = val['id'];
                var iot_name = val['name'];

                var iot_li = $('<li>').appendTo($iot_list);
                $('<a>').attr('id', 'iot_li_' + iot_name).attr('href', '#').text(iot_name).on('click', function() { selected_iot_id = iot_id; }).appendTo(iot_li);
            });
        },
        error: function(error) {
            console.log(error);
        }
    });
})();

(function() {
    var StartDateTime;
    var EndDateTime;
    var dataObject = new Object;
    var label_array = [];
    var data_array = [];

    $('#startdatetimepicker').datetimepicker();
    $('#enddatetimepicker').datetimepicker();
    $('#refreshsensorchart').click(function(request) {
        StartDateTime = moment($('#startdatetimepicker').data('DateTimePicker').date());
        EndDateTime = moment($('#enddatetimepicker').data('DateTimePicker').date());

        dataObject.startPeriod = StartDateTime.format("YYYY-MM-DD HH:mm").toString();
        dataObject.endPeriod = EndDateTime.format("YYYY-MM-DD HH:mm").toString();
        dataObject.id = selected_iot_id
        if (dataObject.startPeriod != "Invalid date" && dataObject.endPeriod != "Invalid date") {
            // reset arrays
            label_array = [];
            data_array = [];

            $.ajax({
                url: host_url + '/sensors_actuators/getPeriodIntervalData/',
                type: 'POST',
                data: JSON.stringify(dataObject),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: true,
                success: function(message) {
                    // populate data and labels array
                    results_array = message['results'];
                    $.each(results_array, function(index, value) {
                        label_array.push(value['datetime']);
                        data_array.push(value['value']);
                    });
                    var ctx = $("#sensor_data_canvas");
                    var sensor_data = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: label_array,
                            datasets: [{
                                label: message['name'],
                                backgroundColor: "rgba(38, 185, 154, 0.31)",
                                borderColor: "rgba(38, 185, 154, 0.7)",
                                pointBorderColor: "rgba(38, 185, 154, 0.7)",
                                pointBackgroundColor: "rgba(38, 185, 154, 0.7)",
                                pointHoverBackgroundColor: "#fff",
                                pointHoverBorderColor: "rgba(220,220,220,1)",
                                pointBorderWidth: 1,
                                data: data_array
                            }]
                        },
                    });
                },
                error: function(error) {
                    console.log(error);
                }
            });
        } else
            alert("Please fill a start and an end date");
    });
})();

//notify user if a sensor missed the data sending in the last hour
(function() {
    $.ajax({
        url: host_url + '/sensors_actuators/getIotReadingErrors/',
        type: 'POST',
        data: '{}',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: false,
        success: function(message) {
            $.each(message['response'], function(index, value) {
                new PNotify({
                    title: 'Cannot read data from sensor ' + value,
                    text: 'Please investigate malfunction.',
                    type: 'error',
                    styling: 'bootstrap3'
                });
            });
        },
        error: function(error) {
            console.log(error);
        }
    });
})();

//populate data
// TODO -- update sensor number
(function() {
    $.ajax({
        url: host_url + '/sensors_actuators/json/1',
        type: 'POST',
        data: '{}',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: false,
        success: function(message) {
            $('#temp_room').text(message['value']);
        },
        error: function(error) {
            console.log(error);
        }
    });

    // TODO -- update sensor number
    $.ajax({
        url: host_url + '/sensors_actuators/json/2',
        type: 'POST',
        data: '{}',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: false,
        success: function(message) {
            $('#temp_room_2').text(message['value']);
        },
        error: function(error) {
            console.log(error);
        }
    });

    // TODO -- update sensor number
    $.ajax({
        url: host_url + '/sensors_actuators/json/3',
        type: 'POST',
        data: '{}',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: false,
        success: function(message) {
            $('#temp_outside').text(message['value']);
        },
        error: function(error) {
            console.log(error);
        }
    });

    // TODO -- update sensor number
    $.ajax({
        url: host_url + '/sensors_actuators/json/4',
        type: 'POST',
        data: '{}',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: false,
        success: function(message) {
            $('#pressure_outside').text(message['value']);
        },
        error: function(error) {
            console.log(error);
        }
    });
})();