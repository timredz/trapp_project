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

function get_mytrades(){

    const parseTime = d3.timeParse("%Y-%m-%dT%H:%M:%S%Z");
    const formatTime = d3.timeFormat("%H:%M");

    d3.json("../my_trades", {
        method: "POST",
        body: JSON.stringify({
            customerID: getCookie('customerID')
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(function(data) {

        data.forEach(function(d) {
          d.tradetime = parseTime(d.tradetime);
        });

        var table_header = '<table id="rates" class="w3-table w3-striped w3-bordered w3-small" style="width:100%;">' +
			'<thead>' +
			  //'<tr style="background-color: #ff0508;color:white" >' +
			  '<tr class="w3-light-grey">' +
				'<th style="text-align: right">BS</th>' +
				'<th style="text-align: left">TICKER</th>' +
				'<th style="text-align: left">PRICE</th>' +
				'<th style="text-align: right">QNTY</th>' +
				'<th style="text-align: right">TIME</th>' +
			  '</tr>' +
			'</thead>';

		var table_content = '';
		for(var i=0;i<data.length;i++){
			 table_content = table_content +
			 '<tr class="chg">' +
			  '<td style="text-align: right">' + data[i]['buysell'] + '</td>' +
			  '<td class="ticker" style="text-align: left">' + ticker_names[data[i]['ticker']] + '</td>' +
			  '<td style="text-align: left">' + data[i]['price'] + '</td>' +
			  '<td style="text-align: right">' + data[i]['quantity'] + '</td>' +
			  '<td style="text-align: right">' + formatTime(data[i]['tradetime']) + '</td>' +
			'</tr>';
		}

		table_end = '</table>' +
					'</div>';

		d3.select("#mytrades").html(table_header+table_content+table_end);


    });
}


function get_myorders(){

    const parseTime = d3.timeParse("%Y-%m-%dT%H:%M:%S%Z");
    const formatTime = d3.timeFormat("%H %M");

    d3.json("../my_orders", {
        method: "POST",
        body: JSON.stringify({
            customerID: getCookie('customerID')
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(function(data) {

        data.forEach(function(d) {
          d.status = "исполнена";
          if(d.balance == d.quantity){
            d.status = "активна";
          }
        });

        var table_header = '<table id="rates" class="w3-table w3-striped w3-bordered w3-small" style="width:100%;">' +
			'<thead>' +
			  //'<tr style="background-color: #ff0508;color:white" >' +
			  '<tr class="w3-light-grey">' +
				'<th style="text-align: right">BS</th>' +
				'<th style="text-align: left">TICKER</th>' +
				'<th style="text-align: left">PRICE</th>' +
				'<th style="text-align: right">QNTY</th>' +
				'<th style="text-align: right">STATUS</th>' +
			  '</tr>' +
			'</thead>';

		var table_content = '';
		for(var i=0;i<data.length;i++){
			 table_content = table_content +
			 '<tr class="chg">' +
			  '<td style="text-align: right">' + data[i]['buysell'] + '</td>' +
			  '<td class="ticker" style="text-align: left">' + ticker_names[data[i]['ticker']] + '</td>' +
			  '<td style="text-align: left">' + data[i]['price'] + '</td>' +
			  '<td style="text-align: right">' + data[i]['quantity'] + '</td>' +
			  '<td style="text-align: right">' + data[i]['status'] + '</td>' +
			'</tr>';
		}

		table_end = '</table>' +
					'</div>';

		d3.select("#myorders").html(table_header+table_content+table_end);

		console.log(data);


    });
}