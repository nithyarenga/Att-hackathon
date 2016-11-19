var map, heatmap;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 14,
    center: {lat: 32.775833, lng: -96.796667},
    mapTypeId: 'roadmap'
  });
  jQuery.getJSON("info.json", function(info) {
    heatmap = new google.maps.visualization.HeatmapLayer({
      data: getPoints(info),
      map: map,
      radius: 40,
      opacity: 0.8
    });
  });
}

function getPoints(json) 
{
  var arr = [];
  for(var i = 0; i < json.length; i++)
  {
    console.log(json[i].lat + " -  " + json[i].long + " - " + json[i].count * 1000);
    for(var j = 0; j < json[i].count * 1000; j++)
    {
      arr.push(new google.maps.LatLng(json[i].lat, json[i].long));
    }
  }
  console.log("done");
  return arr;
}