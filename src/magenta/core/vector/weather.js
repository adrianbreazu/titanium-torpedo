"use strict";
// trigger the debugger so that you can easily set breakpoints
debugger;


var request = require('request');
var VectorWatch = require('vectorwatch-sdk');
var vectorWatch = new VectorWatch();

var logger = vectorWatch.logger;

var location_1 = "http://ADD_YOUR_EXTERNAL_IP_AND_PORT_HERE/sensors_actuators/json/temperature/";
var sensor = [1,2];


vectorWatch.on('config', function(event, response) {
    // your stream was just dragged onto a watch face
    logger.info('on config');

    var location = response.createGridList('Location');
    location.addOption('Location 1');

    var sensor = response.createGridList('Sensor')
    sensor.addOption('Temperature 1');
    sensor.addOption('Temperature 2');

    response.send();

    logger.info('exit config');
});

vectorWatch.on('subscribe', function(event, response) {
    // your stream was added to a watch face
    logger.info('on subscribe');
    var streamText;
    var settings = event.getUserSettings().settings;

    try {
        getTemperature(settings['Location'].name, settings['Sensor'].name).then(function(body) {
            streamText = body.value;
            logger.info('you should see this value: ' + streamText);

            response.setValue(streamText);
            response.send();
        }).catch(function(e) {
            logger.error("error on subscribe: " + e);
            response.setValue("Error");
            response.send();
        });
    } catch (err) {
        streamText = err.message;
        logger.error('on subscribe - error: ' + err.message);
        response.setValue(streamText);
        response.send();
    }
    logger.info('exit subscribe');
});


function getTemperature(location, id) {
    logger.info('on getTemperature');
    var url;

    if (location === "Location 1") {
        url = location_1;
    }

    switch (id) {
        case 'Temperature 1':
            url = url + sensor[0];
            break;
        case 'Temperature 2':
            url = url + sensor[1];
            break;
    }

    logger.info('on getTemperature, use URL: ' + url);

    return new Promise(function (resolve, reject) {
        logger.info('on promise');
        request(url, function(error, httpResponse, body) {
            if (error) {
                logger.error('on promiss error'+ error);
                return;
            }
            try {
                body = JSON.parse(body);
                resolve(body);
            } catch(err) {
                reject("error message: " + err.message);
                return "Error JSON";
            }
        });
    });
}

vectorWatch.on('unsubscribe', function(event, response) {
    // your stream was removed from a watch face
    logger.info('on unsubscribe');

    response.send();
    logger.info('exit unsubscribe');
});

vectorWatch.on('schedule', function(records) {
    logger.info('on schdedule');

    records.forEach(function(record) {
        var settings = record.userSettings;
        try {
            getTemperature(settings['Location'].name, settings['Sensor'].name).then(function(body) {
                var streamText = body.value;
                logger.info('you should see this value: ' + streamText);
                record.pushUpdate(streamText);
            }).catch(function(e) {
                logger.error("on schedule: " + e);
            });
        } catch(err) {
            logger.error('on push user settings: ' + err.message);
        }
    });
});
