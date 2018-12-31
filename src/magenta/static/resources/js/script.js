var selected_iot_id = 1;

(function() {
    var $iot_tag = $('#iot_tag');
    var $iot_list = $('#iot_list');

    $.ajax({
        url: 'http://127.0.0.1:8080/sensors_actuators/get_iots/',
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
                var iot_date;
                var iot_value;

                var iot_li = $('<li>').appendTo($iot_list);
                $('<a>').attr('id', 'iot_li_' + iot_name).attr('href', '#').text(iot_name).on('click', function() { selected_iot_id = iot_id; }).appendTo(iot_li);

                $.ajax({
                    url: 'http://127.0.0.1:8080/sensors_actuators/json/' + iot_id,
                    type: "POST",
                    data: "{}",
                    contentType: "application/json",
                    dataType: "json",
                    async: false,
                    success: function(response) {
                        iot_value = response['value'];
                        iot_date = response['datetime'];
                    },
                    error: function(error) {
                        console.log("Error in get iot value");
                        console.log(error)
                        iot_value = "Unknown";
                        iot_date = "Unknown";
                    }
                });

                var div_animated = $('<div>').addClass('animated flipInY col-md-4 col-sm-4 col-xs-4 tile_stats_count').appendTo($iot_tag);
                $('<div>').addClass('left').appendTo(div_animated);
                var div_right = $('<div>').addClass('right').appendTo(div_animated);
                var span = $('<span>').addClass('count_top').text(iot_name).appendTo(div_right);
                //$('<i>').addClass('fa fa-university').appendTo(span);
                $('<div>').addClass('count').text(iot_value).appendTo(div_right);
                $('<span>').addClass('count_bottom').text(iot_date).appendTo(div_right);
            });
        },
        error: function(error) {
            console.log("Error in get iot list");
            console.log(error);
        }
    });
})();

(function() {
    var $ctx = $('#temp_canvas');
    var $data = [];
    var $label = [];
    var lineChart;

    var period_data = "24";
    reload_data();

    function clear_data() {
        $data = [];
        $label = [];
        lineChart.destroy();
    }

    $('#24_read').click(function() {
        period_data = "24";
        clear_data();
        reload_data();
    });
    $('#48_read').click(function() {
        period_data = "48";
        clear_data();
        reload_data();
    });
    $('#360_read').click(function() {
        period_data = "360";
        clear_data();
        reload_data();
    });
    $('#720_read').click(function() {
        period_data = "720";
        clear_data();
        reload_data();
    });


    function reload_data() {
        // make ajax call
        $.ajax({
            url: 'http://127.0.0.1:8080/sensors_actuators/get_temp_data/',
            type: "POST",
            data: JSON.stringify({ "period": period_data, "id": selected_iot_id.toString() }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            async: false,
            success: function(message) {
                var message_array = message['read'];
                $.each(message_array, function(index, val) {
                    $data.push(val['value']);
                    $label.push(val['datetime']);
                });
            },
            error: function(error) {
                console.log("Error");
                console.log(error);
            }
        });

        lineChart = new Chart($ctx, {
            type: 'line',
            data: {
                labels: $label,
                datasets: [{
                    label: "Temperature",
                    backgroundColor: "rgba(38, 185, 154, 0.31)",
                    borderColor: "rgba(38, 185, 154, 0.7)",
                    data: $data
                }]
            },
        });
    }

})();