(function() {
var $ctx = $('#temp_canvas');
var $data = [];
var $label = [];


$.ajax({
    url: 'http://localhost:8000/sensors_actuators/get_temp_data/',
    type: "POST",
    data: JSON.stringify({"period":"24","type":"temperature", "id":"1"}),
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

var lineChart = new Chart($ctx, {
    type: 'line',
    data: {
        labels: $label,
        datasets: [{
          label: "Temperature",
          backgroundColor: "rgba(38, 185, 154, 0.31)",
          borderColor: "rgba(38, 185, 154, 0.7)",
          pointBorderColor: "rgba(38, 185, 154, 0.7)",
          pointBackgroundColor: "rgba(38, 185, 154, 0.7)",
          pointHoverBackgroundColor: "#fff",
          pointHoverBorderColor: "rgba(220,220,220,1)",
          pointBorderWidth: 1,
          data: $data
        }]
      },
    });
})();