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
            body: JSON.stringify({ "customerID": customerID, "reg_date": reg_date })
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
        var out = '<p>Баланс: ' + data['total_value'] + ' руб.';
        out += '<p>Стоимость позиции: ' + data['posvalue'] + ' руб</p>';

        d3.select("#stdout").html(out);
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


