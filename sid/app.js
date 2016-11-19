var express = require('express');
var app = express();
var path = require("path");
var request = require("request");
var fs = require("fs");
var mapendpoint = "http://50.97.82.230:8080/dashboard_";
var sosendpoint = "http://50.97.82.230:8080/sos";

app.use('/', express.static(path.join(__dirname, 'gentelella')));

app.get('/map', function (req, res) {
	var query = req.query.value;
	var url = mapendpoint + query;
	console.log(url);
	request(url, function (error, response, body) {
	  if (!error && response.statusCode == 200) {
	  	fs.writeFileSync("gentelella/production/info.json", JSON.stringify(JSON.parse(body)[query]), { flag : 'w' });
	    res.redirect('/production/map.html');
	  }
	  else
	  {
	  	console.log(error)
	  }
	});
})

app.get('/sos', function (req, res) {
	console.log(sosendpoint);
	request(sosendpoint, function (error, response, body) {
		if (!error && response.statusCode == 200) 
		{
			if(body != "")
			{
				res.send(body);
			}
		}
	});
});

app.listen(3000, function () {
  console.log('Example app listening on port 3000!')
});