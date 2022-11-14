ticker_names = {
	"USD000UTSTOM": "USD/RUB",
	"EUR_RUB__TOM": "EUR/RUB",
	"CNYRUB_TOM": "CNY/RUB",
	"USDCNY_TOM": "USD/CNY",
	"KZTRUB_TOM": "KZT/RUB",
	"HKDRUB_TOM": "HKD/TOM",
	"TRYRUB_TOM": "TRY/RUB",
	"EURUSD000TOM": "EUR/USD"
}

function draw(ticker, divid="#stdout"){
	var margin = {top: 0, right: 60, bottom: 0, left: 0},
		width = 360 - margin.left - margin.right,
		height = 230 - margin.top - margin.bottom;

	var x = d3.scaleBand().range([0, width-30]).padding(0.2);
	var y = d3.scaleLinear().range([0.8*height, 0]);
	var y_vol = d3.scaleLinear().range([height, 0.8*height]);

	// parse the date / time
	var parseTime = d3.timeParse("%Y-%m-%dT%H:%M:%S%Z");

	var svg = d3.select(divid).append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
	  .append("g")
		.attr("transform",
			  "translate(" + margin.left + "," + margin.top + ")");

	var x_timeline = [];

	var colorScale = d3.scaleLinear().domain([-2, -1.5,-1, -0.5, 0, 0.5, 1, 1.5, 2])
			.range(['rgb(246, 53, 56)', 'rgb(246, 53, 56)', 'rgb(191, 64, 69)', 'rgb(139, 68, 78)',
			'rgb(65, 69, 84)', 'rgb(53, 118, 78)', 'rgb(47, 158, 79)', 'rgb(48, 204, 90)', 'rgb(48, 204, 90)']);


	d3.json("../candle/"+ticker).then(function(data) {

        data = data['candle'];
		console.log(data);

		data.forEach(function(d) {
		  d.valid_time = parseTime(d.valid_time);
		  x_timeline.push(d.valid_time);
		});

		x.domain(x_timeline);


		// Scale the range of the data
		//x.domain(d3.extent(data, function(d) { return d.end; }));
		y_min = d3.min(data, function(d) { return d.pr_low; });
		y_max = d3.max(data, function(d) { return d.pr_high; });
		y_first = data[0]["pr_open"];
		y_last = Math.round(data[data.length-1]["pr_close"]*1000)/1000;
		x_last = data[data.length-1]["valid_time"];
		chg = Math.round(10000 * (y_last - y_first) / y_first) / 100;
		chg2 = Math.round(10000 * (y_max - y_min) / y_min) / 100;

		y.domain([y_min, y_max]);
		y_vol.domain([0, d3.max(data, function(d) { return d.volume; })]);

		var x_offset = 2;

		//grid y lines
		svg.append("g")
			.selectAll("line")
			.data(y.ticks())
			.enter()
		.append("line")
			.style("stroke", "grey")
			.style("stroke-width", 1)
			.attr("stroke-dasharray", "4")
			.style("stroke-opacity", 0.2)
				.attr("y1", d => 0.5 + y(d))
				.attr("y2", d => 0.5 + y(d))
				.attr("x1", 0)
				.attr("x2", width);

		// candle min max line
		svg.selectAll("line3")
			.data(data)
			.enter()
			.append("line")
			.style("stroke", "black")
			.style("stroke-width", 1)
			.attr("x1", function(d) { return x(d.valid_time) + x_offset; })
			.attr("y1", function(d) { return y(d.pr_low); })
			.attr("x2", function(d) { return x(d.valid_time) + x_offset; })
			.attr("y2", function(d) { return y(d.pr_high); });

		// append the rectangles for the bar chart
		svg.selectAll(".candlebar")
			.data(data)
			.enter()
			.append("rect")
			.style("stroke", "black")
			.style("stroke-width", 0.5)
			.attr("x", function(d) { return x(d.valid_time); })
			.attr("width", x.bandwidth())
			.attr("y", function(d) { return y(d3.max([d.pr_open, d.pr_close])); })
			.attr("height", function(d) { return y(d3.min([d.pr_open, d.pr_close])) - y(d3.max([d.pr_open, d.pr_close])) + 0.1; })
			.attr("fill", function(d) {if(d.pr_open > d.pr_close){return "#FF3131"}; return "#4CBB17";})
			.attr("opacity", 1);


			// volume bars bar chart
		svg.append("g")
			.selectAll(".volume_bar")
			.data(data)
			.enter()
			.append("rect")
			.attr("x", function(d) { return x(d.valid_time); })
			.attr("width", x.bandwidth())
			.attr("y", function(d) { return y_vol(d.volume);})
			.attr("height", function(d) { return height - y_vol(d.volume); })
			.attr("fill", function(d) {if(d.pr_open > d.pr_close){return "#FF3131"}; return "#4CBB17";})
			.attr("opacity", 0.5);

		// Add the y Axis
		svg.append("g")
			.attr("transform", "translate("+width+",0)")
			.call(d3.axisRight(y))
			.call(g => g.select(".domain").remove());


		// price level line
		svg.append("line")
			.style("stroke", "#117A65")
			.style("stroke-width", 1)
			.attr("stroke-dasharray", "4")
			.style("stroke-opacity", 0.8)
			.attr("x1", function(d) { return x(x_last)+5; })
			.attr("y1", function(d) { return y(y_last); })
			.attr("x2", function(d) { return width+20;})
			.attr("y2", function(d) { return y(y_last); });


		svg.append("rect")
			.attr("x", width+5)
			.attr("width", 35)
			.attr("y", function(d) { return y(y_last)-1;})
			.attr("height", 17)
			.attr("fill", "black")
			.attr("opacity", 1);


		//Last price
        svg.append("g")
            .append("text")
            .attr("x", width+8)
            .attr("y", y(y_last)+11)
            .text(y_last)
            .attr("font-size", "9px")
            .attr("font-weight", "bold")
            .attr("fill", "white");





	});
}
