ticker_names = {
	"USD000UTSTOM": "USD/RUB",
	"EUR_RUB__TOM": "EUR/RUB",
	"CNYRUB_TOM": "CNY/RUB",
	"USDCNY_TOM": "USD/CNY",
	"KZTRUB_TOM": "KZT/RUB",
	"HKDRUB_TOM": "HKD/RUB",
	"TRYRUB_TOM": "TRY/RUB",
	"EURUSD000TOM": "EUR/USD"
}

var tickers = ["USD000UTSTOM", "EUR_RUB__TOM", "CNYRUB_TOM", "USDCNY_TOM", "KZTRUB_TOM", "HKDRUB_TOM", "TRYRUB_TOM", "EURUSD000TOM"];
var nicks = ["Доллар", "Евро", "Юань", "Доллар/Юань", "Тенге", "Гонконг доллар", "Лира", "Евро/Доллар"];
var divids = ["stdout1", "stdout2", "stdout3", "stdout4", "stdout5", "stdout6", "stdout7", "stdout8"];
var images = ["usd", "eur", "cny", "usdcny", "kzt", "hkd", "try", "eurusd"];

for(var i=0;i<tickers.length;i++){
    d3.select('#allfx').append('div')
        .attr("class", "minch")
        .append('a')
        .attr("id", divids[i])
        .attr("href", "trade/"+tickers[i]);
}

function draw(){
	var margin = {top: 0, right: 0, bottom: 0, left: 0},
		width = 160 - margin.left - margin.right,
		height = 100 - margin.top - margin.bottom;

	// parse the date / time
	var parseTime = d3.timeParse("%Y-%m-%dT%H:%M:%S%Z");

	var colorScale = d3.scaleLinear().domain([-2, -1.5,-1, -0.5, 0, 0.5, 1, 1.5, 2])
			.range(['rgb(246, 53, 56)', 'rgb(246, 53, 56)', 'rgb(191, 64, 69)', 'rgb(139, 68, 78)',
			'rgb(65, 69, 84)', 'rgb(53, 118, 78)', 'rgb(47, 158, 79)', 'rgb(48, 204, 90)', 'rgb(48, 204, 90)']);

	d3.json("instruments").then(function(alldata) {

        const x_offset = 10;

        for(var i=0;i<tickers.length;i++){
            const pos = i;
            var ticker = tickers[pos];
            data = alldata[ticker];

            data.forEach(function(d) {
              d.valid_time = parseTime(d.valid_time);
            });

            var svg = d3.select("#"+divids[pos]).append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            // set the ranges
            var x = d3.scaleTime()
                        .domain(data.map(d => d.valid_time))
                        .range(d3.range(3+x_offset, width-50));

            var y = d3.scaleLinear().range([height-35, 35]);

            // define the line
            var valueline = d3.line()
                .x(function(d) { return x(d.valid_time); })
                .y(function(d) { return y(d.pr_close); });

          // Scale the range of the data
          //x.domain(d3.extent(data, function(d) { return d.end; }));
          const y_min = d3.min(data, function(d) { return d.pr_close; });
          const y_max = d3.max(data, function(d) { return d.pr_close; });
          const y_first = data[0]["pr_close"];
          const y_last = data[data.length-1]["pr_close"];
          const x_last = data[data.length-1]["valid_time"];
          const chg = Math.round(10000 * (y_last - y_first) / y_first) / 100;
          const chg2 = Math.round(10000 * (y_max - y_min) / y_min) / 100;

          y.domain([y_min, y_max]);

        // img rocket for gainers
        svg.append("image")
            .attr('xlink:href', '../../static/image/'+images[pos]+'.png')
            .attr('width', 32+x_offset)
            .attr('height', 32)
            .attr('x', 0)
            .attr('y', 0);

        //Ticker
        svg.append("g")
            .append("text")
            .attr("x", 32+x_offset)
            .attr("y", 16)
            .text(ticker_names[ticker])
            .attr("font-size", "14px")
            .attr("font-weight", "bold")
            .attr("fill", "black");

        //Name
        svg.append("g")
            .append("text")
            .attr("x", 32+x_offset)
            .attr("y", 29)
            .text(nicks[pos])
            .attr("font-size", "11px")
            .attr("fill", "black");


        //Last price
        svg.append("g")
            .append("text")
            .attr("x", x(x_last)+5)
            .attr("y", y(y_last)+5)
            .text(Math.round(y_last*100)/100)
            .attr("font-size", "12px")
            .attr("font-weight", "bold")
            .attr("fill", "black");
            //.attr("fill", "#F8F8F8");

        //Chg %
        svg.append("g")
            .append("text")
            .attr("x", 105+x_offset)
            .attr("y", 16)
            .text(function(){if(chg>0){return "+" + chg + "%";} return chg + "%";})
            .attr("font-size", "11px")
            .attr("font-weight", "bold")
            .attr("fill", colorScale(chg));


          // Add the valueline path.
          svg.append("path")
              .data([data])
              .attr("class", "line")
              .attr("d", valueline)
              .attr("stroke", colorScale(chg));

          }

	});
}

draw();