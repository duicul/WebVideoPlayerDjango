var temp_opt={"temp1":{"name":"Temperature1","checked":true},"temp1_grad":{"name":"Temperature1 change","checked":false},"temp2":{"name":"Temperature2","checked":true},"temp2_grad":{"name":"Temperature2 change","checked":false},"temp_out":{"name":"Temperature outside","checked":true},"humid_out":{"name":"Humidity outside","checked":false}};
var volt_opt={"volt1":{"name":"Voltage","checked":false}};
var ac_opt={"voltage":{"name":"Voltage AC","checked":false},"current":{"name":"Current AC","checked":false},"power":{"name":"Power","checked":false},"energy":{"name":"Energy - KWh ","checked":false},"energyday":{"name":"Energy Daily - Wh","checked":false},"energyhour":{"name":"Energy Hourly - Wh","checked":false},"energysample":{"name":"Energy between Samples - Wh","checked":false},"energymonth":{"name":"Energy Monthly - KWh","checked":false}};

function show_opt(){
    data="";
    
    checked=temp_opt["temp_out"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state('temp_out',1,this)\">";
    data+="<label>"+temp_opt["temp_out"]["name"]+"</label></br>";
    
    checked=temp_opt["humid_out"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state('humid_out',1,this)\">";
    data+="<label>"+temp_opt["humid_out"]["name"]+"</label></br>";
    
    checked=temp_opt["temp1"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state('temp',1,this)\">";
    data+="<label>"+temp_opt["temp1"]["name"]+"</label></br>";
    
    checked=temp_opt["temp1_grad"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state('temp_grad',1,this)\">";
    data+="<label>"+temp_opt["temp1_grad"]["name"]+"</label></br>";
    
    checked=temp_opt["temp2"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state('temp',2,this)\">";
    data+="<label>"+temp_opt["temp2"]["name"]+"</label></br>";
    
    checked=temp_opt["temp2_grad"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state('temp_grad',2,this)\">";
    data+="<label>"+temp_opt["temp2_grad"]["name"]+"</label></br>";
    
    checked=volt_opt["volt1"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state('volt',1,this)\">";
    data+="<label>"+volt_opt["volt1"]["name"]+"</label></br>";
    
    $("#temp_volt_opt").html(data);
}

function show_opt_ac(){
    data="";
    checked=ac_opt["voltage"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state_ac('voltage',this)\">";
    data+="<label>"+ac_opt["voltage"]["name"]+"</label></br>";
    
    checked=ac_opt["current"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state_ac('current',this)\">";
    data+="<label>"+ac_opt["current"]["name"]+"</label></br>";
    
    checked=ac_opt["power"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state_ac('power',this)\">";
    data+="<label>"+ac_opt["power"]["name"]+"</label></br>";
    
    checked=ac_opt["energy"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state_ac('energy',this)\">";
    data+="<label>"+ac_opt["energy"]["name"]+"</label></br>";
    
    checked=ac_opt["energysample"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state_ac('energysample',this)\">";
    data+="<label>"+ac_opt["energysample"]["name"]+"</label></br>";
    
    checked=ac_opt["energyhour"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state_ac('energyhour',this)\">";
    data+="<label>"+ac_opt["energyhour"]["name"]+"</label></br>";
    
    checked=ac_opt["energyday"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state_ac('energyday',this)\">";
    data+="<label>"+ac_opt["energyday"]["name"]+"</label></br>";
    
    checked=ac_opt["energymonth"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state_ac('energymonth',this)\">";
    data+="<label>"+ac_opt["energymonth"]["name"]+"</label></br>";
    
    $("#ac_opt").html(data);
}

function check_state(type,index,elem){
    if(type=="temp_out")
         temp_opt["temp_out"]["checked"]=elem.checked
    if(type=="humid_out")
         temp_opt["humid_out"]["checked"]=elem.checked
    if(type=="temp"){
        if(index==1)
            temp_opt["temp1"]["checked"]=elem.checked
        else if(index==2)
            temp_opt["temp2"]["checked"]=elem.checked
    }
    else if(type=="temp_grad"){
        if(index==1)
            temp_opt["temp1_grad"]["checked"]=elem.checked
        else if(index==2)
            temp_opt["temp2_grad"]["checked"]=elem.checked
    }
    else if(type=="volt"){
            if(index==1)
                volt_opt["volt1"]["checked"]=elem.checked
            }
    //console.log(temp_opt)
    //console.log(volt_opt)
}   

function check_state_ac(type,elem){
    ac_opt[type]["checked"]=elem.checked
    //console.log(ac_opt)
} 

function init(){
	draw_gauge_temperature();
	draw_gauge_voltage();
	draw_gauge_ac();
	draw_graph_all();
	show_opt();
	show_opt_ac();
	draw_weather();
	display_rpi_data();
	setInterval(function(){ draw_gauge_temperature();
							draw_gauge_voltage();
							draw_gauge_ac()
							draw_weather();
							//draw_graph();
							}, 300000);
	setInterval(function(){ display_rpi_data();
                            }, 60000);
}

function force_refresh(){
$.ajax({url: "/force_poll", success: function(result){
	draw_gauge_temperature();
	draw_gauge_voltage();
	draw_gauge_ac();
	draw_graph();
	}});
}

function draw_gauge_temperature(){
$.ajax({url: "/temperature", success: function(result){
    //result=JSON.parse(result)
    result=eval(result)
    //console.log(result)
    //console.log(result[0])
    //console.log(result[1])
	div_html=""
	div_html+="Temperature "+result[0]["temp_id"]+" : "+new Date(result[0]["date"]).toString()+"</br>"
	div_html+="Temperature "+result[1]["temp_id"]+" : "+new Date(result[1]["date"]).toString()+"</br>"
	div_html+="<canvas id=\"gauge_temp_1\"></canvas>";
	div_html+="<canvas id=\"gauge_temp_2\"></canvas>";
    $("#draw_gauge_temperature").html(div_html);
    var radial1 = new RadialGauge({
							renderTo: 'gauge_temp_1',
							width: 200,
							height: 200,
							units: 'C',
							title: "Temperature "+result[0]["temp_id"],
							value: result[0]["temp"],
							minValue: -10,
							maxValue: 110,
							majorTicks: ['-10','5','20','35','50','65','80','95','110'],
							minorTicks: 4,
							strokeTicks: false,
							highlights: [
								{ from: -10, to: 5, color: 'rgba(0,0,255,.15)' },
								{ from: 5, to: 20, color: 'rgba(0,0,100,.15)' },
								{ from: 20, to: 35, color: 'rgba(0,200,0,.25)' },
								{ from: 35, to: 50, color: 'rgba(0,100,0,.25)' },
								{ from: 50, to: 65, color: 'rgba(50,100,0,.15)' },
								{ from: 65, to: 80, color: 'rgba(100,100,0,.15)' },
								{ from: 80, to: 95, color: 'rgba(150,100,0,.25)' },
								{ from: 95, to: 110, color: 'rgba(200,100,0,.25)' },
							],
							colorPlate: '#222',
							colorMajorTicks: '#f5f5f5',
							colorMinorTicks: '#ddd',
							colorTitle: '#fff',
							colorUnits: '#ccc',
							colorNumbers: '#eee',
							colorNeedle: 'rgba(240, 128, 128, 1)',
							colorNeedleEnd: 'rgba(255, 160, 122, .9)',
							valueBox: true,
							animationRule: 'bounce',
							animationDuration: 500
					});
	radial1.draw();
	var radial2 = new RadialGauge({
							renderTo: 'gauge_temp_2',
							width: 200,
							height: 200,
							units: 'C',
							title: "Temperature "+result[1]["temp_id"],
							value: result[1]["temp"],
							minValue: -10,
							maxValue: 110,
							majorTicks: ['-10','5','20','35','50','65','80','95','110'],
							minorTicks: 4,
							strokeTicks: false,
							highlights: [
								{ from: -10, to: 5, color: 'rgba(0,0,255,.15)' },
								{ from: 5, to: 20, color: 'rgba(0,0,100,.15)' },
								{ from: 20, to: 35, color: 'rgba(0,200,0,.25)' },
								{ from: 35, to: 50, color: 'rgba(0,100,0,.25)' },
								{ from: 50, to: 65, color: 'rgba(50,100,0,.15)' },
								{ from: 65, to: 80, color: 'rgba(100,100,0,.15)' },
								{ from: 80, to: 95, color: 'rgba(150,100,0,.25)' },
								{ from: 95, to: 110, color: 'rgba(200,100,0,.25)' },
							],
							colorPlate: '#222',
							colorMajorTicks: '#f5f5f5',
							colorMinorTicks: '#ddd',
							colorTitle: '#fff',
							colorUnits: '#ccc',
							colorNumbers: '#eee',
							colorNeedle: 'rgba(240, 128, 128, 1)',
							colorNeedleEnd: 'rgba(255, 160, 122, .9)',
							valueBox: true,
							animationRule: 'bounce',
							animationDuration: 500
					});
	radial2.draw();

    }});
}

function draw_weather(){
    $.ajax({url: "/weather", success: function(result){
        //console.log(result)
        const weather_data = JSON.parse(result);
        //console.log(weather_data)
        html_val="<div class=\"row\">"
        html_val+="<div class=\"col-md-2\">"
        html_val+="<img src=\"https://openweathermap.org/img/wn/"+weather_data["weather"][0]["icon"]+"@2x.png\" /><br/>"
        html_val+="</div>"
        html_val+="<div class=\"col-md-3\">"
        html_val+="Temp : "+weather_data["main"]["temp"]+" &#8451; <br/>"
        html_val+="Feels like : "+weather_data["main"]["feels_like"]+" &#8451; <br/>"
        html_val+="Humidity : "+weather_data["main"]["humidity"]+" % <br/>"
        html_val+="Wind : "+(weather_data["wind"]["speed"]*3.6).toFixed(2)+" km/h "+weather_data["wind"]["deg"]+"&#176; <br/>"
        html_val+="Clouds : "+weather_data["clouds"]["all"]+" % <br/>";
        html_val+="</div>"
        html_val+="<div class=\"col-md-7\">"
        html_val+="City : "+weather_data["name"]+"<br/>" 
        let sr=new Date(0);
        sr.setUTCSeconds(weather_data["sys"]["sunrise"])
        html_val+="Sunrise : "+sr+"<br/>"
        let ss=new Date(0);
        ss.setUTCSeconds(weather_data["sys"]["sunset"])
        html_val+="Sunset : "+ss+"<br/>"
        html_val+="</div></div>"
        $("#weather_status").html(html_val);
        }    
    });
}

function draw_gauge_voltage(){
    $.ajax({url: "/voltage", success: function(result){
	div_html=""
	div_html+=new Date(result["date"]).toString()+"</br>"
	div_html+="<canvas id=\"gauge_voltage\"></canvas>";
    $("#draw_gauge_voltage").html(div_html);
    var radial1 = new RadialGauge({
							renderTo: 'gauge_voltage',
							width: 200,
							height: 200,
							units: 'V',
							title: "Battery",
							value: result["volt1"],
							minValue: 0,
							maxValue: 40,
							majorTicks: ['0','10','20','30','40'],
							minorTicks: 10,
							strokeTicks: true,
							highlights: [
								{ from: 0, to: 10, color: 'rgba(0,0,155,.15)' },
								{ from: 10, to: 20, color: 'rgba(0,255,255,.15)' },
								{ from: 20, to: 30, color: 'rgba(0,155,0,.15)' },
								{ from: 30, to: 40, color: 'rgba(255,30,0,.25)' }
							],
							colorPlate: '#222',
							colorMajorTicks: '#f5f5f5',
							colorMinorTicks: '#ddd',
							colorTitle: '#fff',
							colorUnits: '#ccc',
							colorNumbers: '#eee',
							colorNeedle: 'rgba(240, 128, 128, 1)',
							colorNeedleEnd: 'rgba(255, 160, 122, .9)',
							valueBox: true,
							animationRule: 'bounce',
							animationDuration: 500
					});
	radial1.draw();
    }});
}

function draw_gauge_ac(){
    $.ajax({url: "/ac", success: function(result){
    div_html=""
    div_html+=new Date(result["date"]).toString()+"</br>"
    div_html+="<canvas id=\"gauge_ac_voltage\"></canvas>";
    div_html+="<canvas id=\"gauge_ac_current\"></canvas>";
    div_html+="<canvas id=\"gauge_ac_power\"></canvas>";
    div_html+="<canvas id=\"gauge_ac_energy\"></canvas>";
    $("#draw_gauge_ac").html(div_html);
    var radial1 = new RadialGauge({
                            renderTo: 'gauge_ac_voltage',
                            width: 200,
                            height: 200,
                            units: 'V',
                            title: "Voltage",
                            value: result["voltage"],
                            minValue: 0,
                            maxValue: 320,
                            majorTicks: ['0','80','160','240','320'],
                            minorTicks: 10,
                            strokeTicks: true,
                            highlights: [
                                { from: 0, to: 80, color: 'rgba(0,0,155,.15)' },
                                { from: 80, to: 160, color: 'rgba(0,255,255,.15)' },
                                { from: 160, to: 240, color: 'rgba(0,155,0,.15)' },
                                { from: 240, to: 320, color: 'rgba(255,30,0,.25)' }
                            ],
                            colorPlate: '#222',
                            colorMajorTicks: '#f5f5f5',
                            colorMinorTicks: '#ddd',
                            colorTitle: '#fff',
                            colorUnits: '#ccc',
                            colorNumbers: '#eee',
                            colorNeedle: 'rgba(240, 128, 128, 1)',
                            colorNeedleEnd: 'rgba(255, 160, 122, .9)',
                            valueBox: true,
                            animationRule: 'bounce',
                            animationDuration: 500
                    });
    radial1.draw();
    
    var radial2 = new RadialGauge({
                            renderTo: 'gauge_ac_current',
                            width: 200,
                            height: 200,
                            units: 'A',
                            title: "Current",
                            value: result["current"],
                            minValue: 0,
                            maxValue: 4,
                            majorTicks: ['0','1','2','3','4'],
                            minorTicks: 10,
                            strokeTicks: true,
                            highlights: [
                                { from: 0, to: 1, color: 'rgba(0,0,155,.15)' },
                                { from: 1, to: 2, color: 'rgba(0,255,255,.15)' },
                                { from: 2, to: 3, color: 'rgba(0,155,0,.15)' },
                                { from: 3, to: 4, color: 'rgba(255,30,0,.25)' }
                            ],
                            colorPlate: '#222',
                            colorMajorTicks: '#f5f5f5',
                            colorMinorTicks: '#ddd',
                            colorTitle: '#fff',
                            colorUnits: '#ccc',
                            colorNumbers: '#eee',
                            colorNeedle: 'rgba(240, 128, 128, 1)',
                            colorNeedleEnd: 'rgba(255, 160, 122, .9)',
                            valueBox: true,
                            animationRule: 'bounce',
                            animationDuration: 500
                    });
    radial2.draw();
    
    var radial3 = new RadialGauge({
                            renderTo: 'gauge_ac_power',
                            width: 200,
                            height: 200,
                            units: 'W',
                            title: "Power",
                            value: result["power"],
                            minValue: 0,
                            maxValue: 600,
                            majorTicks: ['0','100','200','300','400','500','600'],
                            minorTicks: 10,
                            strokeTicks: true,
                            highlights: [
                                { from: 0, to: 100, color: 'rgba(0,0,155,.15)' },
                                { from: 100, to: 200, color: 'rgba(0,255,255,.15)' },
                                { from: 200, to: 300, color: 'rgba(0,155,0,.15)' },
                                { from: 300, to: 400, color:  'rgba(255,230,0,.25)'},
                                { from: 400, to: 500, color: 'rgba(255,100,0,.25)' },
                                { from: 500, to: 600, color: 'rgba(255,30,0,.25)' }
                            ],
                            colorPlate: '#222',
                            colorMajorTicks: '#f5f5f5',
                            colorMinorTicks: '#ddd',
                            colorTitle: '#fff',
                            colorUnits: '#ccc',
                            colorNumbers: '#eee',
                            colorNeedle: 'rgba(240, 128, 128, 1)',
                            colorNeedleEnd: 'rgba(255, 160, 122, .9)',
                            valueBox: true,
                            animationRule: 'bounce',
                            animationDuration: 500
                    });
    radial3.draw();    
    
    energy_val=result["energy"]/1000
    floor_energy_val=Math.floor(energy_val/1000)*1000
    var radial4 = new RadialGauge({
                            renderTo: 'gauge_ac_energy',
                            width: 200,
                            height: 200,
                            units: 'KWh',
                            title: "Energy",
                            value: result["energy"]/1000,
                            minValue: floor_energy_val,
                            maxValue: floor_energy_val+1000,
                            majorTicks: [floor_energy_val,floor_energy_val+200,floor_energy_val+400,floor_energy_val+600,floor_energy_val+800,floor_energy_val+1000],
                            minorTicks: 10,
                            strokeTicks: true,
                            highlights: [
                                { from: floor_energy_val, to: floor_energy_val+200, color: 'rgba(0,0,155,.15)' },
                                { from: floor_energy_val+200, to: floor_energy_val+400, color: 'rgba(0,255,255,.15)' },
                                { from: floor_energy_val+400, to: floor_energy_val+600, color: 'rgba(0,155,0,.15)' },
                                { from: floor_energy_val+600, to: floor_energy_val+800, color: 'rgba(255,230,0,.25)' },
                                { from: floor_energy_val+800, to: floor_energy_val+1000, color: 'rgba(255,30,0,.25)' }
                            ],
                            colorPlate: '#222',
                            colorMajorTicks: '#f5f5f5',
                            colorMinorTicks: '#ddd',
                            colorTitle: '#fff',
                            colorUnits: '#ccc',
                            colorNumbers: '#eee',
                            colorNeedle: 'rgba(240, 128, 128, 1)',
                            colorNeedleEnd: 'rgba(255, 160, 122, .9)',
                            valueBox: true,
                            animationRule: 'bounce',
                            animationDuration: 500
                    });
    radial4.draw();
    
    }});
}



function draw_graph_all(){
    
    data_array=[]

    data_array[0]={type:"line",
            axisYType: "secondary",
            name: "Temperature1 [C]",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}

    data_array[1]={type:"line",
            axisYType: "secondary",
            name: "Temperature2 [C]",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}
            
    data_array[2]={type:"stepArea",
            axisYType: "secondary",
            name: "Temperature1 change [C]",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}
    
    data_array[3]={type:"stepArea",
            axisYType: "secondary",
            name: "Temperature2 change [C]",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}
    
    
    data_array[4]={type:"line",
            axisYType: "secondary",
            name: "Temperature1 predicted [C]",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}

    data_array[5]={type:"line",
            axisYType: "secondary",
            name: "Temperature2 predicted [C]",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}
    

    data_array[6]={type:"line",
            axisYType: "secondary",
            name: "Voltage DC [V]",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}
    
    data_array[7]={type:"line",
            axisYType: "secondary",
            name: "Voltage AC [V]",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}

    data_array[8]={type:"line",
            axisYType: "secondary",
            name: "Current AC [A]",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}

    data_array[9]={type:"line",
            axisYType: "secondary",
            name: "Power [W]",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}
            
    data_array[10]={type:"line",
            axisYType: "secondary",
            name: "Energy [KWh]",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}
    
    data_array[11]={type:"column",
            axisYType: "secondary",
            name: "Energy Daily [Wh]",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}
    
    data_array[12]={type:"column",
            axisYType: "secondary",
            name: "Energy Hourly [Wh]",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}
            
    data_array[13]={type:"line",
            axisYType: "secondary",
            name: "Energy between Samples [Wh]",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}
    
    data_array[14]={type:"column",
            axisYType: "secondary",
            name: "Energy Monthly [KWh]",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}
    
    data_array[15]={type:"line",
            axisYType: "secondary",
            name: "Temperature outside [C]",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}
            
    data_array[16]={type:"line",
            axisYType: "secondary",
            name: "Humidity Outside [%]",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}
            
    chart = new CanvasJS.Chart("graph", {
                    animationEnabled: true,
                    title:{ text: "Measurements"},
                    toolTip: {
                        shared: true,
                        contentFormatter: function(e){
                            //console.log(e.entries)
                            var str = "";
                            str = str.concat(e.entries[0].dataPoint.x);
                            str = str.concat("</br>");
                            for (var i = 0; i < e.entries.length; i++){
                                var  temp = "<div style=\"color: "+e.entries[i].dataSeries.color+";\">"+e.entries[i].dataSeries.name + " <strong>"+  e.entries[i].dataPoint.y + "</strong></div>" ; 
                                str = str.concat(temp);
                            }
                        return (str);
                        }
                    },
                    legend: {
                        horizontalAlign: "left", // "center" , "right"
                        verticalAlign: "top", //"center", "bottom"
                        fontSize: 15
                        },
                    axisX:{  
                        valueFormatString: "DD MMM HH:mm"
                    },
                    axisY:{includeZero: true},
                    data:eval(data_array)
                });
    draw_graph(chart,data_array);
    draw_graph_ac(chart,data_array);
}
function draw_graph(chart,data_array){
    items=$("#items_interval").val()
    
    url_temp="/home_station/temperature_data?items="+items
    url_volt="/home_station/voltage_data?items="+items
    
    //chart["data"]=eval(data_array)
    
    if(temp_opt["temp1"]["checked"] || temp_opt["temp2"]["checked"]||temp_opt["temp1_grad"]["checked"] || temp_opt["temp2_grad"]["checked"]|| temp_opt["humid_out"]["checked"]|| temp_opt["temp_out"]["checked"])        
    $.ajax({url: url_temp, success: function(result){
	    result_rec=JSON.parse(result)["recorded"]
	    temp1_data=result_rec[1]
        temp2_data=result_rec[2]
        temp3_temp_out=result_rec[3]
        temp4_humid_out=result_rec[4]
	    result_pred=JSON.parse(result)["predict"]
	    temp1_init=0
	    temp1_date=null
	    temp2_init=0
	    temp2_date=null
	    //console.log(result_rec)
	    temp1_data.forEach(function(item){
          if(item["value"]!=-127){
            if(temp_opt["temp1"]["checked"])
             data_array[0]["dataPoints"].push({x:new Date(item["date"]),y:item["value"]})
            if(temp_opt["temp1_grad"]["checked"]){
              if(temp1_date==null){
                  temp1_date=new Date(item["date"])
                  temp1_init=item["value"] 
                  }
               else {
                var diffMins = Math.round((((new Date(item["date"])-temp1_init) % 86400000) % 3600000) / 60000);
                data_array[2]["dataPoints"].push({x:temp1_date,y:item["value"]-temp1_init/*/diffMins*/})
                temp1_date=new Date(item["date"])
                temp1_init=item["value"]
              }
            }
          }
        })
        temp2_data.forEach(function(item){
          if(item["value"]!=-127){
            if(temp_opt["temp2"]["checked"])
             data_array[1]["dataPoints"].push({x:new Date(item["date"]),y:item["value"]})
            if(temp_opt["temp2_grad"]["checked"]){
              if(temp1_date==null){
                  temp1_date=new Date(item["date"])
                  temp1_init=item["value"] 
                  }
               else {
                var diffMins = Math.round((((new Date(item["date"])-temp1_init) % 86400000) % 3600000) / 60000);
                data_array[3]["dataPoints"].push({x:temp1_date,y:item["value"]-temp1_init/*/diffMins*/})
                temp1_date=new Date(item["date"])
                temp1_init=item["value"]
              }
            }
          }
        })
        
        if(temp_opt["temp_out"]["checked"])
            temp3_temp_out.forEach(function(item){        
             data_array[15]["dataPoints"].push({x:new Date(item["date"]),y:item["value"]})
             })
        
        if(temp_opt["humid_out"]["checked"])
            temp4_humid_out.forEach(function(item){        
             data_array[16]["dataPoints"].push({x:new Date(item["date"]),y:item["value"]})
             })
        
	    result_pred.forEach(function(item){
          if(item["temp_id"]==1&&item["temp"]!=-127 && temp_opt["temp1"]["checked"])
          if(item["temp_id"]==2&&item["temp"]!=-127 && temp_opt["temp2"]["checked"])
            data_array[5]["dataPoints"].push({x:new Date(item["date"]),y:item["temp2"]})
           })
	    console.log(data_array)
	    chart["data"]=eval(data_array)
	    chart.render();
	    
	}});
	
	if(volt_opt["volt1"]["checked"])
    $.ajax({url: url_volt, success: function(result){
        result=JSON.parse(result)
        result.forEach(function(item){
                if(volt_opt["volt1"]["checked"])
                    data_array[6]["dataPoints"].push({x:new Date(item["date"]),y:item["volt1"]})
        })
        console.log(data_array)
        chart["data"]=eval(data_array)
        chart.render();
        }});    
    }
    
    
function draw_graph_ac(chart,data_array){
    items=$("#items_interval").val()
    //console.log(items)
    url_ac="/home_station/ac_data?items="+items
    
    //console.log(chart["data"])
    //console.log(ac_opt)
    if(ac_opt["voltage"]["checked"] || ac_opt["current"]["checked"]||ac_opt["power"]["checked"] || ac_opt["energy"]["checked"] || ac_opt["energyday"]["checked"] || ac_opt["energyhour"]["checked"] || ac_opt["energysample"]["checked"] || ac_opt["energymonth"]["checked"])        
    $.ajax({url: url_ac, success: function(result){
        result=JSON.parse(result)
        
        var sample_energy=[];
        var daily_energy=[];
        var hourly_energy=[];
        var monthly_energy=[];
        
        result.forEach(function(item){
            d=new Date(item["date"])
            if(ac_opt["voltage"]["checked"])
                data_array[7]["dataPoints"].push({x:d,y:item["voltage"]})
            if(ac_opt["current"]["checked"])
                data_array[8]["dataPoints"].push({x:d,y:item["current"]})
            if(ac_opt["power"]["checked"])
                data_array[9]["dataPoints"].push({x:d,y:item["power"]})
            if(ac_opt["energy"]["checked"])
                data_array[10]["dataPoints"].push({x:d,y:item["energy"]/1000})
            
            if(ac_opt["energysample"]["checked"])
                if(sample_energy.length==0)
                    sample_energy.push({x:new Date(item["date"]),y:item["energy"]})
                else{
                    sample_energy[sample_energy.length-1].y=item["energy"]-sample_energy[sample_energy.length-1].y
                    sample_energy[sample_energy.length-1].x=new Date(item["date"])
                    sample_energy.push({x:new Date(item["date"]),y:item["energy"]})}
                
            if(ac_opt["energyday"]["checked"])
                if(daily_energy.length==0)
                    daily_energy.push({x:new Date(item["date"]),y:item["energy"]})
                else if(daily_energy[daily_energy.length-1].x.getDate()!=d.getDate()){
                    daily_energy[daily_energy.length-1].y=item["energy"]-daily_energy[daily_energy.length-1].y
                    daily_energy[daily_energy.length-1].x=new Date(item["date"])
                    daily_energy.push({x:new Date(item["date"]),y:item["energy"]})}
            
            if(ac_opt["energymonth"]["checked"]){    
                if(monthly_energy.length==0){
                    monthly_energy.push({x:new Date(item["date"]),y:item["energy"]});
                    //console.log(monthly_energy);
                    }
                else if(monthly_energy[monthly_energy.length-1].x.getMonth()!=d.getMonth()){
                    monthly_energy[monthly_energy.length-1].y=item["energy"]-monthly_energy[monthly_energy.length-1].y
                    monthly_energy[monthly_energy.length-1].x=new Date(item["date"])
                    monthly_energy.push({x:new Date(item["date"]),y:item["energy"]})}
            }   
                
            if(ac_opt["energyhour"]["checked"])    
                if(hourly_energy.length==0){
                    hourly_energy.push({x:new Date(item["date"]),y:item["energy"]})}
                else if(hourly_energy[hourly_energy.length-1].x.getDate()!=d.getDate()||hourly_energy[hourly_energy.length-1].x.getHours()!=d.getHours()){
                    hourly_energy[hourly_energy.length-1].y=item["energy"]-hourly_energy[hourly_energy.length-1].y
                    hourly_energy[hourly_energy.length-1].x=new Date(item["date"])
                    hourly_energy.push({x:new Date(item["date"]),y:item["energy"]})}         
            
           });
        
        
        last_item=result[result.length-1]
        
         if(ac_opt["energysample"]["checked"]&&sample_energy.length!=0){
            lt=sample_energy.pop()
            last_sample=sample_energy.length>0?sample_energy[sample_energy.length-1]:0
            sample_energy.push({x:new Date(lt["x"]),y:(last_sample["y"])})
            //console.log("last_sample ")
            //console.log(sample_energy)
            }
        
         if(ac_opt["energyday"]["checked"]&&daily_energy.length!=0){
            lt=daily_energy.pop()
            last_daily=daily_energy.length>0?daily_energy[daily_energy.length-1]:0
            daily_energy.push({x:new Date(lt["x"]),y:(last_daily["y"])})
            daily_energy.push({x:new Date(last_item["date"]),y:(last_item["energy"]-lt["y"])})
            //console.log("last_daily ")
            //console.log(daily_energy)
            }
        if(ac_opt["energymonth"]["checked"]&&monthly_energy.length!=0){
            if(monthly_energy.length==1){
                lt=monthly_energy.pop()
                monthly_energy.push({x:new Date(last_item["date"]),y:(last_item["energy"]-lt["y"])})}
            else {
                lt=monthly_energy.pop()
                //monthly_energy.push({x:new Date(lt["x"]),y:(lt["y"])})
                monthly_energy.push({x:new Date(last_item["date"]),y:(last_item["energy"]-lt["y"])})
                }
            //last_monthly=monthly_energy[monthly_energy.length-1]
            //console.log(last_monthly)
            
            console.log("last_monthly ")
            console.log(monthly_energy)
            }    
        
         if(ac_opt["energyhour"]["checked"]&&hourly_energy.length!=0){
            lt=hourly_energy.pop()
            last_hourly=hourly_energy.length>0?hourly_energy[hourly_energy.length-1]:0
            hourly_energy.push({x:new Date(lt["x"]),y:(last_hourly["y"])})
            hourly_energy.push({x:new Date(last_item["date"]),y:(last_item["energy"]-lt["y"])})
            //console.log("last_hourly ")
            //console.log(hourly_energy)
            }
        
        //console.log(last_item)
        //console.log(daily_energy)
        //console.log(hourly_energy)
        
        data_array[11]["dataPoints"]=daily_energy
        data_array[12]["dataPoints"]=hourly_energy
        data_array[13]["dataPoints"]=sample_energy
        data_array[14]["dataPoints"]=monthly_energy
        
        if(chart["data"]==null)
            chart["data"]=eval(data_array)
        else {
            chart["data"][7]=eval(data_array)[7]
            chart["data"][8]=eval(data_array)[8]
            chart["data"][9]=eval(data_array)[9]
            chart["data"][10]=eval(data_array)[10]
            chart["data"][11]=eval(data_array)[11]
            chart["data"][12]=eval(data_array)[12]
            chart["data"][13]=eval(data_array)[13]
            chart["data"][14]=eval(data_array)[14]}
        
        //console.log(data_array)
        chart.render();
    }});  
    
    
    }
	
function display_rpi_data(){
    $("#rpi_data").html("")
    $.ajax({url: "/memory_usage", success: function(result){
         $("#rpi_data").html($("#rpi_data").html()+"<br><hr>"+result);
        }});
    $.ajax({url: "/cpu_gpu_temp", success: function(result){
        $("#rpi_data").html($("#rpi_data").html()+"<br><hr>"+result);
        }});
     $.ajax({url: "/disk_usage", success: function(result){
         $("#rpi_data").html($("#rpi_data").html()+"<br><hr>"+result);
        }});
    
}