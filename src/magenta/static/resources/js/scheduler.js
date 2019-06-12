json_string = JSON.stringify(json_msg);
json_content = JSON.parse(json_string);

$('#start-time').val(json_content['StartTime']);
$('#skip-days').val(json_content['SkipDays']);

if (json_content['Schedule']['Monday'] == 'false')
    $('#monday').removeAttr('checked');
else
    $('#monday').attr('checked', 'checked');
if (json_content['Schedule']['Tuesday'] == 'false')
    $('#tuesday').removeAttr('checked');
else
    $('#tuesday').attr('checked', 'checked');
if (json_content['Schedule']['Wednesday'] == 'false')
    $('#wednesday').removeAttr('checked');
else
    $('#wednesday').attr('checked', 'checked');
if (json_content['Schedule']['Thursday'] == 'false')
    $('#thursday').removeAttr('checked');
else
    $('#thursday').attr('checked', 'checked');
if (json_content['Schedule']['Friday'] == 'false')
    $('#friday').removeAttr('checked');
else
    $('#friday').attr('checked', 'checked');
if (json_content['Schedule']['Saturday'] == 'false')
    $('#saturday').removeAttr('checked');
else
    $('#saturday').attr('checked', 'checked');
if (json_content['Schedule']['Sunday'] == 'false')
    $('#sunday').removeAttr('checked');
else
    $('#sunday').attr('checked', 'checked');

$('#front').val(json_content['Duration']['Front']);
$('#back').val(json_content['Duration']['Back']);
$('#side').val(json_content['Duration']['Side']);
$('#flowers').val(json_content['Duration']['Flowers']);


$('#submit').click(function() {
    // create JSON response
    var json_response = new Object();
    var schedule_object = new Object();
    var duration_object = new Object();

    json_response.StartTime = $('#start-time').val();
    json_response.SkipDays = $('#skip-days').val();

    if ($('#monday').is(':checked'))
        schedule_object.Monday = "true";
    else
        schedule_object.Monday = "false";
    if ($('#tuesday').is(':checked'))
        schedule_object.Tuesday = "true";
    else
        schedule_object.Tuesday = "false";
    if ($('#wednesday').is(':checked'))
        schedule_object.Wednesday = "true";
    else
        schedule_object.Wednesday = "false";
    if ($('#thursday').is(':checked'))
        schedule_object.Thursday = "true";
    else
        schedule_object.Thursday = "false";
    if ($('#friday').is(':checked'))
        schedule_object.Friday = "true";
    else
        schedule_object.Friday = "false";
    if ($('#saturday').is(':checked'))
        schedule_object.Saturday = "true";
    else
        schedule_object.Saturday = "false";
    if ($('#sunday').is(':checked'))
        schedule_object.Sunday = "true";
    else
        schedule_object.Sunday = "false";
    json_response.Schedule = schedule_object;

    duration_object.Front = $('#front').val();
    duration_object.Back = $('#back').val();
    duration_object.Side = $('#side').val();
    duration_object.Flowers = $('#flowers').val();
    json_response.Duration = duration_object;
    $.ajax({
        url: host_url + '/sensors_actuators/store_scheduler/',
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(json_response),
        async: false,
        success: function() {},
        error: function(error) {
            console.log(error);
        }
    });
});