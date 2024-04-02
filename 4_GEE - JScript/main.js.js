var AOI = rectangle;

Map.addLayer(AOI);

Map.centerObject(AOI);

print('Area of Interest', AOI);

// defining the study period

var startYear = 2007;

var endYear = 2021;

var startMonth = 1;

var endMonth = 12;

var startDate = ee.Date.fromYMD(startYear, startMonth, 1);

var endDate = ee.Date.fromYMD(endYear, endMonth, 31);

var years = ee.List.sequence(startYear, endYear);

var months = ee.List.sequence(1, 12);

var CRS = ee.String('EPSG: 32632')

// to avoid later issues while using MODIS data

var f_ET = ee.ImageCollection("MODIS/061/MOD16A2GF")

    .filterBounds(AOI)

    .filterDate(startDate, endDate)

    .select(['ET', 'PET'])

    .map(function(img) {

        return img.divide(10).reproject({

            crs: CRS,

            scale: 500

        }).clip(AOI).copyProperties(img, ['system:time_start'])

    }) // needs time_start to avoid loosing the date of the image collected

    .map(function(img) {

        return img.select('ET').divide(img.select('PET')).rename('f_ET').copyProperties(img, ['system:time_start']).set('system:id', img.date().format('YYYY-MM-dd'))

    })

print(f_ET)

Map.addLayer(f_ET, {

    min: 0.2,

    max: 0.9

}, 'f_ET_8-Day') // 0.2 & 0.9 are parameters for visualisation

// Create monthly f_ET.

var monthly_fET = ee.ImageCollection.fromImages(

    years.map(function(y) {

        return months.map(function(m) {

            var filtered = f_ET

                .filter(ee.Filter.calendarRange(y, y, 'year'))

                .filter(ee.Filter.calendarRange(m, m, 'month'))

                .mean();

            return filtered.set({

                'month': m,

                'year': y,

                'system:id': ee.Date.fromYMD(y, m, 1).format('YYYY-MM'),

                'system:time_start': ee.Date.fromYMD(y, m, 1).millis()

            });

        });

    }).flatten() // convert a collection of image collections into a single image collection

);

print(monthly_fET, 'f_ET_Monthly')

Map.addLayer(monthly_fET, {

    min: 0.2,

    max: 0.9

}, 'f_ET_Monthly')

// Compute monthly series.

var meanMonthlyfET_LongTerm = ee.ImageCollection.fromImages(

    ee.List.sequence(1, 12).map(function(m) {

        var filtered_mean = monthly_fET.filter(ee.Filter.eq('month', m)).mean().rename('mean_LT');

        var filtered_STD = monthly_fET.filter(ee.Filter.eq('month', m)).reduce(ee.Reducer.stdDev()).rename('stdDev_LT');

        return filtered_mean.addBands(filtered_STD).set({

            'month': m,

            'system:id': m

        });

    })

);

print(meanMonthlyfET_LongTerm)

Map.addLayer(meanMonthlyfET_LongTerm.select('mean_LT'), {

    min: 0.2,

    max: 0.9

}, 'f_ET_Monthly_LongTerm')

var Anomaly_fET = monthly_fET.map(function(image) {

    // Get the month of the image.

    var year = image.date().get('year');

    var month = image.date().get('month');

    // Get the corresponding reference image for the month.

    var referenceImage = meanMonthlyfET_LongTerm.filter(

        ee.Filter.eq('month', month)).first();

    // Check if the images have bands

    var hasBands = image.bandNames().size().gt(0);

    // Compute the anomaly by subtracting reference image from input image.

    var anomalyImage = ee.Algorithms.If(

        hasBands,

        (image.subtract(referenceImage.select('mean_LT'))).divide(referenceImage.select('stdDev_LT')),

        image

    );

    return ee.Image(anomalyImage).rename('Anomaly_fET').set(

        'system:time_start', ee.Date.fromYMD(year, month, 1).millis());

});

print(Anomaly_fET)

Map.addLayer(Anomaly_fET, {}, 'fET Anomaly')

print(ui.Chart.image.seriesByRegion(Anomaly_fET, AOI, ee.Reducer.mean(), 0, 500))

// var ATI = LST & Albedo.

// To get the LST data.

var LST = ee.ImageCollection("MODIS/061/MOD11A2")

    .filterBounds(AOI)

    .filterDate(startDate, endDate)

    .select('LST_Day_1km')

    .map(function(img) {

        return img.divide(200).reproject({

            crs: CRS,

            scale: 500

        }).clip(AOI).copyProperties(img, ['system:time_start'])

            .set('system:id', img.date().format('YYYY-MM-dd'))

    });

print(LST)

Map.addLayer(LST, {

    min: 0.2,

    max: 0.9

}, 'LST_8_days')

// Calculating the Delta_LST for later use.

var Delta_LST = ee.ImageCollection("MODIS/061/MOD11A2")

    .filterBounds(AOI)

    .filterDate(startDate, endDate)

    .select(['LST_Day_1km', 'LST_Night_1km'])

    .map(function(img) {

        return img.divide(200).reproject({

            crs: CRS,

            scale: 500

        }).clip(AOI).copyProperties(img, ['system:time_start'])

            .set('system:id', img.date().format('YYYY-MM-dd'))

    })

    .map(function(img) {

        return img.select('LST_Day_1km').subtract(img.select('LST_Night_1km')).rename('Delta_LST').copyProperties(img, ['system:time_start']).set('system:id', img.date().format('YYYY-MM-dd'))

    });

print(Delta_LST, 'Delta LST')

Map.addLayer(Delta_LST, {

    min: 0.2,

    max: 0.9

}, 'Delta_LST')

// Extract Albedo data.

var Albedo = ee.ImageCollection('MODIS/061/MCD43A3')

    .filterBounds(AOI)

    .filterDate(startDate, endDate)

    .select('Albedo_BSA_shortwave')

    .map(function(img) {

        return img.divide(1000).reproject({

            crs: CRS,

            scale: 500

        }).clip(AOI).copyProperties(img, ['system:time_start'])

            .set('system:id', img.date().format('YYYY-MM-dd'))

    });

// Define the filter for the join

var filterTimeEq = ee.Filter.equals({

    leftField: 'system:time_start',

    rightField: 'system:time_start'

});

// Create the inner join object

var innerJoin = ee.Join.inner();

// Apply the inner join

var joinedCollection = innerJoin.apply(Albedo, Delta_LST, filterTimeE