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
        url: 'http://192.168.1.11:8000/sensors_actuators/get_temp_data/',
        type: "POST",
        data: JSON.stringify({"period":period_data,"type":"temperature", "id":"1"}),
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
        error: function (error) {
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