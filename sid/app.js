var express = require('express');
var app = express();
var path = require("path");
var request = require("request");
var fs = require("fs");
var mapendpoint = "http://50.97.82.230:8080/dashboard_";
var sosendpoint = "http://50.97.82.230:8080/sos";
var trendsendpoint = "http://50.97.82.230:8080/trends";

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
	  	res.redirect('/production/map.html');
	  }
	});
})

app.get('/sos', function (req, res) {
	console.log(sosendpoint);
	request(sosendpoint, function (error, response, body) {
		console.log(response.statusCode);
		if (!error && response.statusCode == 200) 
		{
			if(body)
			{
				res.send(body);
			}
			else
			{
				res.send("");	
			}
		}
		else
		{
			res.send("");	
			console.log(error);
		}		
	});
});

app.get('/trends', function (req, res) {
	console.log(trendsendpoint);
	request(trendsendpoint, function (error, response, body) {
		if (!error && response.statusCode == 200) 
		{
			if(body != "")
			{
				res.send(body);
			}
			else
			{
				res.send("");	
			}
		}
		else
		{
			res.send("");
			console.log(error);
		}
		
	});
});

app.listen(3000, function () {
  console.log('Example app listening on port 3000!')
});