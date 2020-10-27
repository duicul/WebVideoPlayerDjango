var apis=[{"name":"covid19api","display":"api.covid19api.com","regions":false},{"name":"geospatial","display":"covid19.geo-spatial (Romania)","regions":true}]

//var states=[{"state":"Confirmed","checked":true}]
var states=[{"state":"Confirmed","display":"Confirmed","checked":true,"api":["geospatial","covid19api"]},
			{"state":"Active","display":"Active","checked":false,"api":["geospatial","covid19api"]},
			{"state":"Recovered","display":"Recovered","checked":false,"api":["geospatial","covid19api"]},
			{"state":"Dead","display":"Dead","checked":false,"api":["geospatial"]},
			{"state":"Tests","display":"Tests","checked":false,"api":["geospatial"]},
			{"state":"TestsperCase","display":"New Tests per Daily Case </br> (no differential is applied)","checked":false,"api":["geospatial"]},
			{"state":"CasesperTest","display":"Daily cases per new Tests </br> (no differential is applied)","checked":false,"api":["geospatial"]},
			{"state":"Quarantined","display":"Quarantined","checked":false,"api":["geospatial"]},
			{"state":"Isolated","display":"Isolated","checked":false,"api":["geospatial"]},
			{"state":"NotSeparated","display":"From population<br> Not Isolated/Quarantined","checked":false,"api":["geospatial"]}]

var region_states=[{"state":"Confirmed","display":"Confirmed","checked":true,"api":["geospatial"],"r":100,"g":200,"b":200,"a":1},
					{"state":"Recuperated","display":"Recuperated","checked":false,"api":["geospatial"],"r":20,"g":250,"b":250,"a":1},
					{"state":"Dead","display":"Dead","checked":false,"api":["geospatial"],"r":250,"g":50,"b":10,"a":1},
					{"state":"DeathRate","display":"DeathRate","checked":false,"api":["geospatial"],"r":250,"g":100,"b":200,"a":1}]

function draw_gauge(){
$.ajax({url: "/read_sensor/dummy/43", success: function(result){
    //console.log(result);
    gauges=[];
    div_html="";
    result=JSON.parse(result)
    result.forEach(function(item,index){
                      div_html+=item["name"]+"  "+item["val"]+"</br>";
		      div_html+="<div id=\"gauge"+item["name"]+"\"></div></br>";}
                   );
    $("#graphdiv").html(div_html);
	result.forEach(function(item,index){
                      var radial = new RadialGauge({
							renderTo: 'gauge-id',
							width: 400,
							height: 400,
							units: 'Km/h',
							title: false,
							value: item["val"],
							minValue: 0,
							maxValue: 220,
							majorTicks: ['-10','-5','0','5','10','15','20','25','30','35','40'],
							minorTicks: 2,
							strokeTicks: false,
							highlights: [
								{ from: 0, to: 50, color: 'rgba(0,255,0,.15)' },
								{ from: 50, to: 100, color: 'rgba(255,255,0,.15)' },
								{ from: 100, to: 150, color: 'rgba(255,30,0,.25)' },
								{ from: 150, to: 200, color: 'rgba(255,0,225,.25)' },
								{ from: 200, to: 220, color: 'rgba(0,0,255,.25)' }
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
					radial.draw();
					}
                   );

    }});
}


function draw_graph(){
	countries_checked=verifycheck();
	var data=[]
	//console.log(countries_checked)
	countries_checked.forEach(function(item,index){
		
		$.ajax({url:"https://api.covid19api.com/dayone/country/"+item+"/status/confirmed/live",success : function(result)
	    {	datapdata=[]
			datapgrowth=[]
			datapgrowthchange=[]
			prev_val=0
			prev_growth=0
			result.forEach(function(item){
				if(item["Province"] ==""){
					date_now= new Date(item["Date"]);
					year=date_now.getFullYear()
					if(year==2020 || year==2021){
						growth=item["Cases"]-prev_val
						datapdata.push({x: new Date(item["Date"]),y:item["Cases"]});
						datapgrowth.push({x: new Date(item["Date"]),y:(growth)});
						datapgrowthchange.push({x: new Date(item["Date"]),y:(growth-prev_growth)});
						prev_val=item["Cases"];
						prev_growth=growth;
					}
				
				}
			});
			$("#graph").html("");
			datapdata.pop()
			datapgrowth.pop()
			datapgrowthchange.pop()
			data_type=$("#data_type").val()
			if(data_type == "data"){
				count_data={type: "line",dataPoints:datapdata,name: item,showInLegend: true,};
				data.push(count_data);
			}
			if(data_type == "growth"){
				count_growth={type: "line",dataPoints:datapgrowth,name: item+" growth",showInLegend: true,};
				data.push(count_growth);
			}
			if(data_type == "growthchange"){
				count_growthchange={type: "line",dataPoints:datapgrowthchange,name: item,showInLegend: true,};
				data.push(count_growthchange);
			}
			
			//console.log(data);
			if(data.length==countries_checked.length){
				var chart = new CanvasJS.Chart("graph", {
					animationEnabled: true,
					title:{	text: "Cases"},
					toolTip: {
						shared: true
					},
					legend: {
						horizontalAlign: "left", // "center" , "right"
						verticalAlign: "center",  // "top" , "bottom"
						fontSize: 15
						},
					axisY:{includeZero: true},
					data:eval(data)
				});
				chart.render();
			}
		}
	    });
		
		
	});	
}
function draw_graph_local(){
	api=$("#api_source").val();
	countries_checked=[]
	if(api=="covid19api")
		countries_checked=verifycheck();
	var data=[]
	data_type=$("#data_type").val()
	pol_grade=$("#pol_grade").val()
	
	checked_states=[]
	data_response=[]
	states.forEach(function(item,index){
		//console.log(item)
		if(item["api"].includes(api) && item["checked"]==true){
			checked_states.push(item["state"])}
	});
	var responses=0;
	//console.log(checked_states)
	checked_states.forEach(function(item,index){
		
		var url="/covid_data/"+item+"/"+api+"/"+data_type;
		
		if(pol_grade!="None"){
			pred_len=$("#pred_select").val()
			url="/covid_data_all/"+item+"/"+api+"/"+data_type+"/"+pred_len+"/"+pol_grade;}
		
		var xmlhttp = new XMLHttpRequest();
		xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
				responses+=1;
				eval(xmlhttp.responseText).forEach(function(item){
					data_response.push(item);
				})
				//data_response.concat(eval(xmlhttp.responseText));
				//console.log(responses+" "+data_response)
				if(responses==checked_states.length){
					//console.log(responses+" "+eval(xmlhttp.responseText))
					$("#graph").html("");
					//console.log(xmlhttp.responseText)
					//console.log(eval(xmlhttp.responseText))
					var chart = new CanvasJS.Chart("graph", {
						animationEnabled: true,
						title:{	text: "Cases"},
						toolTip: {
							shared: true
						},
						legend: {
							horizontalAlign: "center", // "left" , "right"
							verticalAlign: "bottom",  // "top" , "center"
							fontSize: 15
						},
						axisY:{includeZero: true},
						data: data_response
					});
				    $("#graph").css({"height":""});
					chart.render();
				}
			}
        };
		var formData = new FormData();
		formData.append("countries",JSON.stringify(countries_checked));
		xmlhttp.open("POST",url, true);
		xmlhttp.send(formData);});
}

function load_region_data(){
	api=$("#api_source").val();
	countries_checked=[]

	var responses=0;  

	region_state=$("#region_state").val()
	countries_checked=[]
	
	checked_states=[]
	data_response=[]
	region_states.forEach(function(item,index){
		//console.log(item)
		if(item["api"].includes(api) && item["checked"]==true){
			checked_states.push(item)}
	});
	
		
	//console.log(checked_states)
	checked_states.forEach(function(item,index){
		
		var url="/regions/"+item["state"]+"/"+api+"/"+"data";
		
		var xmlhttp = new XMLHttpRequest();
		xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
				responses+=1;
				data_response_aux=[]
				eval(xmlhttp.responseText).forEach(function(item){
					data_response_aux.push(item);
				})
				
				
				region_state={type: "bar",
							  name: item["state"],
							  color: "rgba("+item["r"]+","+item["g"]+","+item["b"]+","+item["a"]+")",
						   	  axisYType: "secondary",
							  showInLegend: true,
							  dataPoints: data_response_aux}
							  
				console.log(region_state)
				data_response.push(region_state)
				//data_response.concat(eval(xmlhttp.responseText));
				//console.log(responses+" "+data_response)
				if(responses==checked_states.length){
					if(checked_states.length==1){
						average=0
						data_response[0]["dataPoints"].forEach(function(itema){
						if(itema["label"]=="Average"){
							average=itema["y"]
							itema["color"]="rgba("+item["r"]+","+item["g"]+","+item["b"]+","+item["a"]+")";}
						});
						console.log(average)
						data_response[0]["dataPoints"].forEach(function(itema){
							if(itema["y"]<average)
								itema["color"]="rgba("+(item["r"]+100)+","+(item["g"]+50)+","+(item["b"]+100)+","+item["a"]+")";
							if(itema["y"]>average)
								itema["color"]="rgba("+(item["r"]-100)+","+(item["g"]-50)+","+(item["b"]-100)+","+item["a"]+")";
							if((itema["y"]==average))
								itema["color"]="rgba("+item["r"]+","+item["g"]+","+item["b"]+","+item["a"]+")";
							});
						
						data_response[0]["dataPoints"].sort(function(a,b){return (a["y"]>b["y"]);});}
					//console.log(responses+" "+eval(xmlhttp.responseText))
					$("#graph").html("");
					//console.log(xmlhttp.responseText)
					//console.log(eval(xmlhttp.responseText))
					//console.log(data_response);
					var chart = new CanvasJS.Chart("graph", {
														animationEnabled: true,
													title:{text:"Regions"},
													axisX:{interval: 1},
													toolTip: {
														shared: true,
														content: toolTipFormatter},
													legend: {
														horizontalAlign: "center", // "left" , "right"
														verticalAlign: "bottom",  // "top" , "center"
														fontSize: 15
													},
													axisY2:{interlacedColor: "rgba(1,77,101,.2)",
															gridColor: "rgba(1,77,101,.1)",
															title: "Regions bar graph"},
													data: data_response});
					$("#graph").css({"height":"180%"});
					chart.render();
				}
			}
        };
		var formData = new FormData();
		formData.append("countries",JSON.stringify(countries_checked));
		xmlhttp.open("POST",url, true);
		xmlhttp.send(formData);});
}

function toolTipFormatter(e) {
	var str = "";
	var total = 0 ;
	var str3;
	var str2 ;
	for (var i = 0; i < e.entries.length; i++){
		var str1 = "<span style= \"color:"+e.entries[i].dataSeries.color + "\">" + e.entries[i].dataSeries.name + "</span>: <strong>"+  e.entries[i].dataPoint.y + "</strong> <br/>" ;
		total = e.entries[i].dataPoint.y + total;
		str = str.concat(str1);
	}
	str2 = "<strong>" + e.entries[0].dataPoint.label + "</strong> <br/>";
	return (str2.concat(str));
}

var prev_pol="None"
function displaypredlength(){
pol_grade=$("#pol_grade").val()
//console.log(pol_grade)
if(pol_grade=="None"){
	$("#pred_len").html("");
	prev_pol=pol_grade
	return;}
if(prev_pol=="None"){
	data="Prediction length : </br>";
	data+="<select id=\"pred_select\">";
	for(i=1;i<=30;i++){
		data+="<option value=\""+i*10+"\">";
		data+=i*10+" Days</option>";
	}
	$("#pred_len").html(data);}
prev_pol=pol_grade
}



function show_api_options(){
api=$("#api_source").val()
if(api=="covid19api"){
	if(prev_api=="geospatial"){
		search_box="<input type=\"text\" id=\"search_country\" placeholder=\"Search Country\" onkeyup=\"load_countries();\"></input>";
		search_box+="<button type=\"button\" class=\"btn btn-primary\" onclick=\"uncheck_all();\">Uncheck All</button>";
		$("#searchbox").html(search_box);}
	load_countries();}
else if(api=="geospatial"){
		if(prev_api=="covid19api"){
			$("#searchbox").html("");}
		$("#country_list").html("");}
	
data="Case Type: </br>";
states.forEach(function(item,index){
		if(item["api"].includes(api)){
			checked=item["checked"]==true? "checked=\"checked\"" : ""
			data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state("+index+",this,'"+api+"')\">";
			data+="<label>"+item["display"]+"</label></br>";}});
data+="<hr>";

regions=false
apis.forEach(function (item){if(item["name"]==api && item["regions"]==true)
								regions=true;
	});
if(regions==true){
	data+="<button class=\"btn btn-primary\" onclick=\"load_region_data()\">Display Regions</button></br>"
	data+="Regions: </br>"
	region_states.forEach(function(item,index){
		if(item["api"].includes(api)){
					checked=item["checked"]==true? "checked=\"checked\"" : ""
					data+="<input type=\"checkbox\" "+checked+" onchange=\"check_region_state("+index+",this,'"+api+"')\">";
					data+="<label>"+item["display"]+"</label></br>";}
				});				
data+="<hr>"	
}

$("#case_type").html(data)

prev_api=api;
}



function check_state(index,elem,api){
if(states[index]["api"].includes(api)){
	states[index]["checked"]=elem.checked
	//console.log(states)
	//console.log(api)
}
}

function check_region_state(index,elem,api){
if(region_states[index]["api"].includes(api)){
	region_states[index]["checked"]=elem.checked
	//console.log(region_states)
	//console.log(api)
}
}

function load_main_menu(){
		data="<button class=\"btn btn-primary\" onClick=\"draw_graph_local()\">Display</button></br> ";
		data+="Data to show: </br>";
                data+="<select id=\"data_type\">";
		data+="<option value=\"data\">";
		data+="Cases data</option>";
		data+="<option value=\"growth\">";
		data+="Cases growth</option>";
		data+="<option value=\"growth_change\">";
		data+="Cases growth change</option>";
		data+="</select><hr>";
		
		data+="Polinomial Aproximation : </br>";
        data+="<select id=\"pol_grade\" onchange=displaypredlength();>";
		data+="<option value=\"None\">";
		data+="None</option>";
		for(i=1;i<=10;i++){
			data+="<option value=\""+i+"\">";
			data+="Grade "+i+"</option>";}
		data+="</select>";
		data+="<div id=\"pred_len\"></div>";
		data+="<hr>";
		
		data+="<div id=\"case_type\">"
		//data+="Case Type: </br>";
        //data+="<select id=\"case_type_select\">";
		
		//data+="<option value=\"Confirmed\">";
		//data+="Confirmed</option>";
		//data+="</select><hr>";
		data+="</div></br>"
		
		data+="API source : </br>";
        data+="<select id=\"api_source\" onchange=show_api_options();>";
		for(i=0;i<apis.length;i++){
			data+="<option value=\""+apis[i]["name"]+"\">";
			data+=apis[i]["display"]+"</option>";}
		data+="</select></br>"
		
		
		data+="<div id=\"searchbox\"><input type=\"text\" id=\"search_country\" placeholder=\"Search Country\" onkeyup=\"load_countries();\"></input>";
		data+="<button type=\"button\" class=\"btn btn-primary\" onclick=\"uncheck_all();\">Uncheck All</button></div>";
		data+="<div id=\"country_list\"></br>";
		data+="</div></br>";
		
		$("#main_menu").html(data);
		
		show_api_options();
}
function check_country(index,elem){
 if(countries.length<=index)
	 return;
 
 if(elem.checked){
 countries[index]["checked"]=true;}
 else countries[index]["checked"]=false;
 //console.log(countries[index]);
}

function uncheck_all(){
      countries.forEach(function(item,index){
			item["checked"]=false;			
		});
		load_countries();
}

var countries=[];
var prev_api="";
function load_countries(){
	api=$("#api_source").val()
	if(api!="covid19api")
		return;
	if(countries.length<=0){
	$.ajax({url:"https://api.covid19api.com/countries",success : function(result)
	    {
		result.sort(function(a,b){return (a["Country"].localeCompare(b["Country"]));});
		result.forEach(function(item,index){
			item["checked"]=false;
			countries.push(item);
			
		});	
		load_countries();
		}
	});}
	//console.log("countries len "+countries.length);
	data="<div class=\"\" style=\"width:300px;height:500px;overflow:auto;\">";
	countries.forEach(function(item,index){
		search_val=$("#search_country").val();
		//console.log(search_val.toLowerCase())
		//console.log(item["Country"].toLowerCase())
		if(item["Country"].toLowerCase().match(""+search_val.toLowerCase()+"")!=null){
			let checkbox_id="country"+item["Slug"];
			check=item["checked"]==true ? "checked":"unchecked";
			data+="<input type=\"checkbox\" id=\""+checkbox_id+"\" checked=\""+check+"\" onchange=\"check_country("+index+",this)\">";
			data+="<label>"+item["Country"]+"</label>";
			data+="</br>";}
	});
	data+="</div> ";
	$("#country_list").html(data);
	countries.forEach(function(item,index){
		search_val=$("#search_country").val();
		//console.log(search_val.toLowerCase())
		//console.log(item["Country"].toLowerCase())
		if(item["Country"].toLowerCase().match(""+search_val.toLowerCase()+"")!=null){
			let checkbox_id="country"+item["Slug"];
			$("#"+checkbox_id).prop("checked", item["checked"]);
			}
	});
	prev_api=api;
}

function verifycheck(){
	checked=[]
	countries.forEach(function (item,index){
		if(item["checked"]==true){
			//console.log("checked "+item);
			checked.push(item["Slug"]);
		}
	});
	return checked;
}
