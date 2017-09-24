(function () {
    // get window height and width
    var height = window.innerHeight,
        width = document.body.clientWidth,
        coords = [],
        api_key = "AIzaSyDNiwIGMuu9c6arwtK2Th11L2hm4mmXtGM";
    // set svg canvas
    var svg = d3.select("#map")
        .append("svg")
        .append("g")
    // load map data, call ready function when complete
    d3.queue()
        .defer(d3.json, "static/data/countries.topojson")
        .await(ready)
    // map object
    var projection = d3.geoMercator()
        .translate([width / 2, height / 2 + 120])
        .scale(170)
    // path object
    var path = d3.geoPath()
        .projection(projection)
    // set up tooltip div
    var tooltip = d3.select("body")
        .append("div")
        .attr("class", "inactive")
    // main function to complete on data load
    function ready(error, data) {
        // get country paths from topojson data
        var countries = topojson.feature(data, data.objects.subunits).features
        // trace country paths on map
        svg.selectAll(".country")
            .data(countries)
            .enter().append("path")
            .attr("class", "country")
            .attr("d", path)
            .attr("data-toggle", "false")
            // highlights country on click
            .on("click", function (d) {
                coords = []
                coords.push(projection.invert(d3.mouse(this))[0], projection.invert(d3.mouse(this))[1])
                console.log("coords", coords);
                toggle = (d3.select(this).attr("data-toggle") == "true")
                if (toggle) {
                    d3.select(this)
                        .classed("selected", false)
                        .attr("data-toggle", "false")
                } else {
                    d3.select(this)
                        .classed("selected", true)
                        .attr("data-toggle", "true");
                }
                // uncomment for zoom on click. needs work. does not toggle
                // var centroid = path.centroid(d);
                // x = centroid[0];
                // y = centroid[1];
                // d3.select("g").transition()
                //     .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + 4 + ")translate(" + -x + "," + -y + ")")
            })
            // show tooltip when country is moused-over
            .on("mouseover", function (d) {
                tooltip.attr("class", "active-tip")
                    .html("<p class='tooltip-text'>" + d.properties.name + "</p>");
                d3.select(".active-tip")
                    .style("top", d3.event.pageY + "px")
                    .style("left", d3.event.pageX + "px")
            })
            // dismiss on mouse-out
            .on("mouseout", function (d) {
                tooltip.attr("class", "inactive");
            });
        // add circles to svg
        // var coord1 = [-122.490402, 37.786453];
        // var coord2 = [-99.912437, 16.848824];
        // var locales = { "San Francisco": { lat: -122.4194, lon: 37.7749, avg: 25, num: 89 }, "Acapulco": { lat: -99.912437, lon: 16.848824, avg: 12, num: 120 }, "Mozambique": { lat: -25.953724, lon: 32.588711, avg: 8, num: 12 }, "Prague": { lat: -50.0755, lon: -14.4378, avg: 34, num: 78 } }
        // test data for setting up markers
        var locales = {
            coords: [[-122.4194, 37.7749, 25, 89], [-99.912437, 16.848824, 12, 120], [25.953724, 32.588711, 8, 12], [14.4378005, 50.0755381, 34, 78]]
        }
        // drop markers
        svg.selectAll("circle")
            .data(locales.coords).enter()
            .append("circle")
            .attr("cx", function (d) { return projection(d)[0]; })
            .attr("cy", function (d) { return projection(d)[1]; })
            .attr("r", function (d) { return d[2]})
            .attr("fill", "#e53935")
            .style("opacity", 0.3)
            .on("click", function(d){
                coords = []
                coords.push(d[1],d[0])
                
            })
        // timer for marker pulse
        // setInterval(function(){
        //     svg.selectAll("circle")
        //         .transition()
        //         .duration(1000)
        //         .attr('r', function (d) {
        //             // console.log(d)
        //             return d[2]
        //         })
        //         .on("end", function (d) {
        //             svg.selectAll("circle")
        //                 .transition()
        //                 .duration(1000)
        //                 .attr('r', function (d) {
        //                     // console.log(d)
        //                     return 2
        //                 })
        //         })
        // }, 1000)
        // d3.select("svg").on("mousedown.log", function () {
        //     console.log(projection.invert(d3.mouse(this)));
        // });
    }
    // materialize modal trigger
    $('.modal').modal({dismissible: true});
    // collect form data and make ajax call
    $(".sub").click(function(){
        
    })

})();