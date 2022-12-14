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

fx_dict = {
	"USD000UTSTOM": {"name": "USD/RUB", "base": "RUB", "asset": "USD", "lot": 1000, "symbol": "$"},
	"EUR_RUB__TOM": {"name": "EUR/RUB", "base": "RUB", "asset": "EUR", "lot": 1000, "symbol": "€"},
	"CNYRUB_TOM": {"name": "CNY/RUB", "base": "RUB", "asset": "CNY", "lot": 1000, "symbol": "¥"},
	"USDCNY_TOM": {"name": "USD/CNY", "base": "CNY", "asset": "USD", "lot": 1000, "symbol": "$"},
	"KZTRUB_TOM": {"name": "KZT/RUB", "base": "RUB", "asset": "KZT", "lot": 1000, "symbol": "₸"},
	"HKDRUB_TOM": {"name": "HKD/RUB", "base": "RUB", "asset": "HKD", "lot": 1000, "symbol": "HK$"},
	"TRYRUB_TOM": {"name": "TRY/RUB", "base": "RUB", "asset": "TRY", "lot": 1000, "symbol": "₤"},
	"EURUSD000TOM": {"name": "EUR/USD", "base": "USD", "asset": "EUR", "lot": 1000, "symbol": "€"},
}


function draw(ticker, divid="#stdout"){
    //var x_width = Math.min(window.innerWidth, 800);
    var x_width = 360;
	var margin = {top: 0, right: 60, bottom: 0, left: 0},
		width = x_width - margin.left - margin.right,
		height = x_width*0.67 - margin.top - margin.bottom;

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

        ob = data['ob'];
        data = data['candle'];
        draw_buttons(ticker, ob);

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

function draw_buttons(ticker, ob){
    var levels = ['⚡ По рынку', 'Лучшая цена', '#5 уровень', '#10 уровень', 'Своя цена'];
    var levels_code = ['market', 'bbo', '5', '10', 'limit'];
    var buy_prices = ['0', ob['buy'][0]['price'], ob['buy'][4]['price'], ob['buy'][9]['price'], '0'];
    var sell_prices = ['0', ob['sell'][0]['price'], ob['sell'][4]['price'], ob['sell'][9]['price'], '0'];

    const buy_avg = Math.round(ob['buy_avg']*1000)/1000;
    const sell_avg = Math.round(ob['sell_avg']*1000)/1000;
    const buy_vol = ob['buy_vol'];
    const sell_vol = ob['sell_vol'];


    //var out = '<p>Можно купить $' + buy_vol + 'k за ' + buy_avg + ' руб</p>';
    //out += '<p>Можно продать $' + sell_vol + 'k за ' + sell_avg + ' руб</p>';
    var out = '<div class="w3-row">';
        out +=     '<div class="w3-col s3 bs w3-center"><b>Продать</b></div>';
        out +=     '<div class="w3-col s6 bs w3-center">Тип заявки</div>';
        out +=     '<div class="w3-col s3 bs w3-center"><b>Купить</b></div>';
    out += '</div>';

    for(let i=0;i<5;i++){
        out += '<div class="w3-row" style="min-height:35px">';
        out += '<div class="w3-col s3">';
        out += '<button class="btn_sell w3-button w3-medium w3-padding-small w3-round-large" onclick="fill_order_details(\''+ticker+'\',\'S\', '+sell_prices[i]+', \''+levels_code[i]+'\', '+sell_prices[1]+')">'+sell_prices[i]+'</button>';
        out += '</div>';
        out += '<div class="w3-col s6 bs-text w3-center">'+levels[i]+'</div>';
        out += '<div class="w3-col s3">';
        out += '<button class="btn_buy w3-button w3-medium w3-padding-small w3-round-large" onclick="fill_order_details(\''+ticker+'\', \'B\', '+buy_prices[i]+',\''+levels_code[i]+'\', '+sell_prices[1]+')">'+buy_prices[i]+'</button>';
        out += '</div>';
        out += '</div>';
    }

    d3.select("#bs-buttons").html(out);

}

function show_modal(id){
    document.getElementById(id).style.display='block';
}

function hide_modal(id){
    document.getElementById(id).style.display='none';
    d3.select("#price_input").attr('disabled', null);
}

function fill_order_details(ticker, buysell, price, lvl, margin_price){
    show_modal('id01');
    const pair = fx_dict[ticker];
    d3.json("../get_balance", {
        method: "POST",
        body: JSON.stringify({
            customerID: getCookie('customerID')
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            'X-CSRFToken': getCookie('csrftoken'),
        }
    }).then(function(data) {
        var max_lots = 0;
        if(buysell=='B'){
            max_lots = Math.floor(data[pair['base']]/margin_price/1000);
            var out = '<button class="w3-button w3-block w3-green w3-section w3-padding w3-round-large" onclick="submit_order(\''+ticker+'\', \'B\', \''+max_lots+'\')">Купить</button>';
            d3.select("#submit_button_type").html(out);
        }else if(buysell=='S'){
            max_lots = Math.floor(data[pair['asset']]/1000);
            var out = '<button class="w3-button w3-block w3-red w3-section w3-padding w3-round-large" onclick="submit_order(\''+ticker+'\', \'S\', \''+max_lots+'\')">Продать</button>';
            d3.select("#submit_button_type").html(out);
        }

        if(lvl=='market'){
            d3.select("#price_input").property("value", "");
            d3.select("#price_input").property("placeholder", "Цена по рынку");
            d3.select("#price_input").attr('disabled', true);
        }else if(lvl=='limit'){

        }else{
            d3.select("#price_input").property("value", price);
        }


        d3.select("#max_lots").html("1 лот = 1000 "+pair['symbol']+"<br>Доступно: "+max_lots);
    });

}


function submit_order(ticker, buysell, max_lots){
    const price = Number(d3.select("#price_input").property("value"));
    const quantity = Number(d3.select("#quantity").property("value"));
    if(quantity>max_lots){
        alert('Недостаточно средств. Максимум ' + max_lots);
    }else if(quantity==0){
        alert('Укажите кол-во лотов');
    }else{
        d3.json("../submit_order", {
            method: "POST",
            body: JSON.stringify({
                customerID: getCookie('customerID'),
                ticker: ticker,
                price: price,
                quantity: quantity,
                buysell: buysell
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });
        hide_modal('id01');
        order_sent();
    }
}

function order_sent(){
    show_modal('id02');
}
