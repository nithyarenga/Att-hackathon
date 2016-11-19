var express = require('express');
var app = express();
var path = require('path');
var http = require("http");
var request = require("request");
var endPoint = "http://50.97.82.230:8080/alerts";

app.get('/', function (req, res) {
    request(endPoint, function (error, response, body) {
        if (!error && response.statusCode == 200) 
        {
		var data = JSON.parse(body);
                var html = "<html>";
		var html = html + "<meta http-equiv='refresh' content='5' >";
                html = html + "<body style='background-color:" + data.color  + "\;'>";
                // for(var i = 0; i < data.text.length; i++)
                // {
                    html = html + "<center><h1>" + data.text + "</h1></center>";
                // }
                html = html + "</body></html>";
                console.log("success");
                res.send(html);
  	}
	else
	{
		console.log(error);
	}
    })
});

app.listen(8080, function () {
    console.log('App listening on port 8080.');
});


