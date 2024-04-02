// Import the Earth Engine library
var ee = require('ee');

// Create a UI root
var ui = ui.root();

// Define a panel to hold the map
var mapPanel = ui.panel({
  widgets: [
    ui.map({
      mapOptions: {
        center: AOI.geometry().centroid().coordinates().reverse(),
        zoom: 8
      }
    })
  ],
  style: {
    position: 'bottom-left',
    width: '70%',
    height: '600px'
  }
});

// Define a panel to hold the legend
var legendPanel = ui.panel({
  widgets: [
    ui.label('Legend', {fontWeight: 'bold'}),
    ui.renderLegendImage(Anomaly_EWDI, {min: -2, max: 2, palette: ['blue', 'white', 'red']})
  ],
  style: {
    position: 'bottom-right',
    width: '25%',
    padding: '8px 15px'
  }
});

// Add layers to the map
var layers = [
  ui.layers.addLayer(Anomaly_EWDI, {min: -2, max: 2, palette: ['blue', 'white', 'red']}, 'EWDI Anomaly'),
  ui.layers.addLayer(AOI, {}, 'Area of Interest')
];

// Add the map and legend to the UI root
ui.root.widgets().reset([mapPanel, legendPanel]);
ui.root.setLayout(ui.root.widgets());

// Reset the map layers
layers.forEach(function(layer) {
  layer();
});
