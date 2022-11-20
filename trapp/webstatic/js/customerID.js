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

fx_symbols = {
    "USD":"$",
    "EUR":"€",
    "RUB":"₽"
}

function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

function setCookie(cname, cvalue, exdays){
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 3600 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname){
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for(let i=0;i<ca.length;i++){
        let c = ca[i];
        while (c.charAt(0) == ' '){
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0){
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function register_user(){
    var uid = getCookie('customerID');

    if(uid == ''){
        const reg_date = Math.floor(Date.now()/1000);
        const customerID = makeid(4) + '_' + reg_date;

        setCookie('customerID', customerID, 2);

        // save to db
        fetch('register_customer', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "customerID": customerID,
                "name": "Tim",
                "phone": "+7945879124",
                "email": "fxworld@ya.ru",
                "reg_date": reg_date }
            )
        })
    }
}


function show_balance(){

    d3.json("get_balance", {
        method: "POST",
        body: JSON.stringify({
            customerID: getCookie('customerID')
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(function(data) {
        console.log(data);

        var table_header = '<h4>Портфель</h4><br><table id="rates" class="w3-table w3-large" style="width:100%;">' +
			'<thead>' +
			  //'<tr style="background-color: #ff0508;color:white" >' +
			  '<tr class="w3-light-grey">' +
				'<th style="text-align: left"></th>' +
				'<th style="text-align: left">Валюта</th>' +
				'<th style="text-align: left">Кол-во</th>' +
			  '</tr>' +
			'</thead>';

		var table_content = '';
		var assets = ['RUB', 'USD', 'EUR'];
		for(var i=0;i<assets.length;i++){
			 table_content = table_content +
			 '<tr class="chg">' +
			  '<td class="ticker" style="text-align: left"><img src="../../static/image/'+assets[i]+'.png" border=3 height=50 width=50></img></td>' +
			  '<td class="ticker" style="text-align: left;padding-top:20px">' + assets[i] + '</td>' +
			  '<td style="text-align: left;padding-top:20px">' + data[assets[i]] + ' ' + fx_symbols[assets[i]] + '</td>' +
			 '</tr>';
		}

		table_end = '</table>' +
					'</div>';

		d3.select("#myposition").html(table_header+table_content+table_end);
    });

}

function show_position(){

    d3.json("position", {
        method: "POST",
        body: JSON.stringify({
            customerID: getCookie('customerID')
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(function(data) {
        console.log(data);
        var table_header = '<table id="rates" class="w3-table w3-striped w3-bordered w3-small" style="width:100%;">' +
			'<thead>' +
			  //'<tr style="background-color: #ff0508;color:white" >' +
			  '<tr class="w3-light-grey">' +
				'<th style="text-align: left">TICKER</th>' +
				'<th style="text-align: left">POSITION</th>' +
			  '</tr>' +
			'</thead>';

		var table_content = '';
		for(var i=0;i<data.length;i++){
			 table_content = table_content +
			 '<tr class="chg">' +
			  '<td class="ticker" style="text-align: left">' + ticker_names[data[i]['ticker']] + '</td>' +
			  '<td style="text-align: left">' + data[i]['pos'] + '</td>' +
			 '</tr>';
		}

		table_end = '</table>' +
					'</div>';

		d3.select("#myposition").html(table_header+table_content+table_end);
    });

}

function increase(amount=1){
    var quantity = Number(d3.select("#quantity").property("value"));
    quantity += amount;
    d3.select("#quantity").property("value", quantity);

    update_net_value(quantity*1000*60.42);
}

function decrease(amount=1){
    var quantity = Number(d3.select("#quantity").property("value"));
    quantity -= amount;
    quantity = Math.max(0, quantity);
    d3.select("#quantity").property("value", quantity);

    update_net_value(quantity*1000*60.42);
}

function update_net_value(val){
    console.log(val);
    d3.select("#net_value").html(val);
}


