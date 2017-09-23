(function () {
    var height = window.innerHeight,
        width = document.body.clientWidth;

    var svg = d3.select("#map")
        .append("svg")
        .append("g")

    d3.queue()
        .defer(d3.json, "static/data/countries.topojson")
        .await(ready)

    var projection = d3.geoMercator()
        .translate([width / 2, height / 2 + 120])
        .scale(170)

    var path = d3.geoPath()
        .projection(projection)

    var tooltip = d3.select("body")
        .append("div")
        .attr("class", "inactive")

    function ready(error, data) {
        console.log(data)
        var countries = topojson.feature(data, data.objects.subunits).features
        svg.selectAll(".country")
            .data(countries)
            .enter().append("path")
            .attr("class", "country")
            .attr("d", path)
            .attr("data-toggle", "false")
            .on("click", function (d) {
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
            .on("mouseover", function (d) {
                tooltip.attr("class", "active")
                    .html("<p class='tooltip-text'>" + d.properties.name + "</p>");
                d3.select(".active")
                    .style("top", d3.event.pageY + "px")
                    .style("left", d3.event.pageX + "px")
            })
            .on("mouseout", function (d) {
                tooltip.attr("class", "inactive");
            });
        ;
    }
})();