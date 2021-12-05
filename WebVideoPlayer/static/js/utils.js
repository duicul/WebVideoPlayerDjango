var ids=[];

function videoPlayerInit(){
    vol = sessionStorage.getItem('playerAudioVolume');
    vol = parseFloat(vol);
    if(! isNaN(val)){
    try{
        let player = videojs('my-video');
        console.log('load vol='+vol);
        player.volume(vol);
    } catch (error) {
        console.error(error + ' vol='+vol);
    }
    }
}

function list_dir(path,parent_el){
   var path_url="";
   if(path!==undefined)
     path_url="?path="+path;
   var url_list_dir="/utils/list_dir"+path_url;
   console.log(url_list_dir);
   $.ajax({url: url_list_dir, success: function(result){
        console.log(result);
        var ret_str="<div class=\"list-group\">";
        var space_ind=0;
        console.log(Object.keys(result));
        result.forEach(function(item_par){
            ret_str+="<div class='list-group-item' onclick='list_dir('"+item_par+"',this);' >"+item_par;
            ret_str+="</div>";
        }
        
        );
        ret_str+="</div>";
        if(parent_el===undefined)
            $("#list_dir").html(ret_str);
        else 
            parent_el.innerHTML=ret_str;

   }
   });
}

function load_modal(){
        var  modal="<div class=\"modal fade\" id=\"descriptionModal\" tabindex=\"-1\" role=\"dialog\" aria-labelledby=\"exampleModalLabel\" aria-hidden=\"true\">";
         modal+="<div style=\"width:70%;\"  class=\"modal-dialog\" role=\"document\">";
        modal+="<div  class=\"modal-content\">";
        modal+=" <div class=\"modal-header\">";
        modal+="<div id=\"description_title\"></div>";
        modal+="<button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\">";
        modal+="  <span aria-hidden=\"true\">&times;</span>";
        modal+="</button>";
        modal+="</div>";
        modal+="<div class=\"modal-body\" id=\"description_body\">";
        modal+="</div>";
        //modal+="<div class=\"modal-footer\">";
        //modal+="<button type=\"button\" class=\"btn btn-secondary\" data-dismiss=\"modal\">Close</button>";
       // modal+="<button type=\"button\" class=\"btn btn-primary\">Save changes</button>";
        //modal+="</div>";
        modal+="</div>";
        modal+="</div>";
        modal+="</div>";
        
        
        $("#modal_desc").html(modal);
    
}

function load_season(uuid){
    var url_list_dir="/utils/list_items?type=season&uuid="+uuid;

    $.ajax({url: url_list_dir, success: function(result){
        let img_w=250;
        let img_h=250;
        let ret_str=""; 
        ret_str+="<div class=\"row\">";
        ret_str+="<div class=\"col-2\"></div>";
        ret_str+="<div class=\"col-8\">";
        
        result.forEach(function(season){
            let season_img=season["img_url"];
            season["episodes"].forEach(function(episode){
                ret_str+="<div>";
                ret_str+="<span onclick=\"load_description('"+episode["unique_id"]+"','episode');\" style=\"cursor: pointer;\" title=\"Info\" data-toggle=\"modal\" data-target=\"#descriptionModal\">";
                ret_str+="<svg width=\"1em\" height=\"1em\" viewBox=\"0 0 16 16\" class=\"bi bi-info-square\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\">";
                ret_str+="<path fill-rule=\"evenodd\" d=\"M14 1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z\"/>";
                ret_str+="<path fill-rule=\"evenodd\" d=\"M14 1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z\"/>";
                ret_str+="<path d=\"M8.93 6.588l-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588z\"/>";
                ret_str+="<circle cx=\"8\" cy=\"4.5\" r=\"1\"/></svg>";
                ret_str+="</span>";
                
                ret_str+="<a data-toggle=\"tooltip\" title=\""+episode["name"]+"\" href=\"/video_player/?play="+episode["unique_id"]+"&type=episode\">";
                ret_str+="<img style=\"border-radius: 8%;cursor: pointer;\" src=\""+season_img;
                ret_str+="\" alt=\""+episode["name"]+"\" width=\""+img_w+"\" height=\""+img_h+"\">";
                ret_str+="</a>";
                ret_str+="<span>"+episode["name"]+" "+episode["movie_title"]+" </span>";
                ret_str+="</div>";
                
                
            });
        
        });
        ret_str+="</div>";   
        ret_str+="<div class=\"col-2\"></div>";
        ret_str+="</div>";
        
        $("#season_files").html(ret_str);
    }
    });
    
}

function load_shows(){
var url_list_dir="/utils/list_items?type=show";
   //console.log(url_list_dir);
   $.ajax({url: url_list_dir, success: function(result){
        let img_w=250;
        let img_h=250;
        movies_per_slide=Math.floor(window.innerWidth*0.8/img_w);
        slides=Math.ceil(result.length/movies_per_slide)
        //console.log(movies_per_slide)
        //console.log(slides)
        id=[];
        let ret_str="";
        result.forEach(function(category){
            ret_str+=category["category_name"]+"<br/>";
            
            category["shows"].forEach(function(show){
                ret_str+="<br/>";
                ret_str+=show["name"]+"<br/>";
                //let season_img=season["img_url"];
                    
                target_id=("demo"+show["name"]).replaceAll(" ","_");
                    
                slides=Math.ceil(show["seasons"].length/movies_per_slide)
            
                ids.push(target_id);
                
                ret_str+="<div id=\""+target_id+"\" class=\"carousel slide\" data-ride=\"carousel\" style=\"background-color: lightblue;\">";
                ret_str+="<ul class=\"carousel-indicators\">";
                ret_str+="<li data-target=\"#"+target_id+"\" data-slide-to=\"0\" class=\"active\"></li>";
            
                let i;
                for (i = 1; i < slides; i++) {
                    ret_str+="<li data-target=\"#"+target_id+"\" data-slide-to=\""+i+"\"></li>";}
                 
                ret_str+="</ul>";
                ret_str+="<div class=\"carousel-inner\">";
                    
                ret_str+="<div class=\"carousel-item active\" style=\"text-align: center\">";
                    
                for (i = 0; i < movies_per_slide; i++) {
                    //console.log(show["seasons"][i])
                    if(i>=show["seasons"].length)
                        break;
                   
                    ret_str+="<span onclick=\"load_description('"+show["seasons"][i]["unique_id"]+"','season');\" style=\"cursor: pointer;\" title=\"Info\" data-toggle=\"modal\" data-target=\"#descriptionModal\">";
                    ret_str+="<svg width=\"1em\" height=\"1em\" viewBox=\"0 0 16 16\" class=\"bi bi-info-square\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\">";
                    ret_str+="<path fill-rule=\"evenodd\" d=\"M14 1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z\"/>";
                    ret_str+="<path fill-rule=\"evenodd\" d=\"M14 1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z\"/>";
                    ret_str+="<path d=\"M8.93 6.588l-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588z\"/>";
                    ret_str+="<circle cx=\"8\" cy=\"4.5\" r=\"1\"/></svg>";
                    ret_str+="</span>";
                
                    ret_str+="<a data-toggle=\"tooltip\" title=\""+show["seasons"][i]["name"]+"\" href=\"/entry_point?type=season&uuid="+show["seasons"][i]["unique_id"]+"\">";
                    ret_str+="<img style=\"border-radius: 8%;cursor: pointer;\" src=\""+show["seasons"][i]["img_url"];
                    ret_str+="\" alt=\""+show["seasons"][i]["name"]+"\" width=\""+img_w+"\" height=\""+img_h+"\">";
                    ret_str+="</a>";
                
                    //ret_str+="</div>";
                
                    ret_str+="<span> </span>";}
                 
                ret_str+="</div>";
            
                var slide_i;
                for (slide_i = 1; slide_i < slides;slide_i++) {
                    
                    ret_str+="<div class=\"carousel-item\" style=\"text-align: center\">";
                        
                    for (i = 0; i < movies_per_slide; i++) {
                        current_index=slide_i*movies_per_slide+i;
                        //console.log(current_index)
                        //console.log(show["seasons"][current_index])
                        if(current_index>=show["seasons"].length)
                            break;
                        
                        //ret_str+="<div>";
                        ret_str+="<span> ";
                    
                        ret_str+="<span onclick=\"load_description('"+show["seasons"][current_index]["unique_id"]+"','season');\" style=\"cursor: pointer;\" title=\"Info\" data-toggle=\"modal\" data-target=\"#descriptionModal\">";
                        ret_str+="<svg width=\"1em\" height=\"1em\" viewBox=\"0 0 16 16\" class=\"bi bi-info-square\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\">";
                        ret_str+="<path fill-rule=\"evenodd\" d=\"M14 1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z\"/>";
                        ret_str+="<path fill-rule=\"evenodd\" d=\"M14 1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z\"/>";
                        ret_str+="<path d=\"M8.93 6.588l-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588z\"/>";
                        ret_str+="<circle cx=\"8\" cy=\"4.5\" r=\"1\"/></svg>";
                        ret_str+="</span>";
                    
                        ret_str+="<a data-toggle=\"tooltip\" title=\""+show["seasons"][current_index]["name"]+"\" href=\"/entry_point?type=season&uuid="+show["seasons"][current_index]["unique_id"]+"\">";
                        ret_str+="<img style=\"border-radius: 8%;cursor: pointer;\" src=\""+show["seasons"][current_index]["img_url"];
                        ret_str+="\" alt=\""+show["seasons"][current_index]["name"]+"\"  width=\""+img_w+"\" height=\""+img_h+"\">";
                        ret_str+="</a>";
                    
                        ret_str+="</span>";
                     
                        //ret_str+="</div>";
                     
                        ret_str+="<span>  </span>";}
                         
                    ret_str+="</div>";}
            
                ret_str+="</div>";
                    
                ret_str+="<a class=\"carousel-control-prev\" href=\"#"+target_id+"\" data-slide=\"prev\">";
                ret_str+="<span class=\"carousel-control-prev-icon\"></span></a>";
                ret_str+="<a class=\"carousel-control-next\" href=\"#"+target_id+"\" data-slide=\"next\">";
                ret_str+="<span class=\"carousel-control-next-icon\"></span></a>";
                ret_str+="</div>";
                    
                ret_str+="</div>";
            });    
                
            ret_str+="<br/>";
        });
    
    $("#shows_files").html(ret_str);
    
    }});        
}

function load_videos(){
   var url_list_dir="/utils/list_items?type=movie";
   //console.log(url_list_dir);
   $.ajax({url: url_list_dir, success: function(result){
        let img_w=250;
        let img_h=250;
        movies_per_slide=Math.floor(window.innerWidth*0.7/img_w);
        slides=Math.ceil(result.length/movies_per_slide)
        //console.log(movies_per_slide)
        //console.log(slides)
        id=[];
        let ret_str="";
        result.forEach(function(parent_dir){
            ret_str+=parent_dir["parent_folder_name"]+"<br/>";
            let movies=parent_dir["movies"]
            slides=Math.ceil(movies.length/movies_per_slide)
            target_id=("demo"+parent_dir["parent_folder_name"]).replaceAll(" ","_");
            ids.push(target_id);
            ret_str+="<div id=\""+target_id+"\" class=\"carousel slide\" data-ride=\"carousel\" style=\"background-color: lightblue;\">";
            ret_str+="<ul class=\"carousel-indicators\">";
            ret_str+="<li data-target=\"#"+target_id+"\" data-slide-to=\"0\" class=\"active\"></li>";
            
            let i;
            for (i = 1; i < slides; i++) {
                ret_str+="<li data-target=\"#"+target_id+"\" data-slide-to=\""+i+"\"></li>";}
                 
            ret_str+="</ul>";
            ret_str+="<div class=\"carousel-inner\">";
            ret_str+="<div class=\"carousel-item active\" style=\"text-align: center\">";
            for (i = 0; i < movies_per_slide; i++) {
                //console.log(movies[i])
                if(i>=movies.length)
                    break;
                
                
                //ret_str+="<div>";
                
                ret_str+="<span onclick=\"load_description('"+movies[i]["unique_id"]+"','movie');\" style=\"cursor: pointer;\" title=\"Info\" data-toggle=\"modal\" data-target=\"#descriptionModal\">";
                ret_str+="<svg width=\"1em\" height=\"1em\" viewBox=\"0 0 16 16\" class=\"bi bi-info-square\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\">";
                ret_str+="<path fill-rule=\"evenodd\" d=\"M14 1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z\"/>";
                ret_str+="<path fill-rule=\"evenodd\" d=\"M14 1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z\"/>";
                ret_str+="<path d=\"M8.93 6.588l-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588z\"/>";
                ret_str+="<circle cx=\"8\" cy=\"4.5\" r=\"1\"/></svg>";
                ret_str+="</span>";
                
                ret_str+="<a data-toggle=\"tooltip\" title=\""+movies[i]["name"]+"\" href=\"/video_player/?play="+movies[i]["unique_id"]+"&type=movie\">";
                ret_str+="<img style=\"border-radius: 8%;cursor: pointer;\" src=\""+movies[i]["img_url"];
                ret_str+="\" alt=\""+movies[i]["name"]+"\" width=\""+img_w+"\" height=\""+img_h+"\">";
                ret_str+="</a>";
                
                
                
                //ret_str+="</div>";
                
                ret_str+="<span> </span>";}
                 
            ret_str+="</div>";
            
            var slide_i;
            for (slide_i = 1; slide_i < slides;slide_i++) {
            ret_str+="<div class=\"carousel-item\" style=\"text-align: center\">";
                for (i = 0; i < movies_per_slide; i++) {
                    current_index=slide_i*movies_per_slide+i;
                    //console.log(current_index)
                    //console.log(movies[current_index])
                    if(current_index>=movies.length)
                        break;
                        
                    //ret_str+="<div>";
                    ret_str+="<span> ";
                    
                    ret_str+="<span onclick=\"load_description('"+movies[current_index]["unique_id"]+"','movie');\" style=\"cursor: pointer;\" title=\"Info\" data-toggle=\"modal\" data-target=\"#descriptionModal\">";
                    ret_str+="<svg width=\"1em\" height=\"1em\" viewBox=\"0 0 16 16\" class=\"bi bi-info-square\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\">";
                    ret_str+="<path fill-rule=\"evenodd\" d=\"M14 1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z\"/>";
                    ret_str+="<path fill-rule=\"evenodd\" d=\"M14 1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z\"/>";
                    ret_str+="<path d=\"M8.93 6.588l-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588z\"/>";
                    ret_str+="<circle cx=\"8\" cy=\"4.5\" r=\"1\"/></svg>";
                    ret_str+="</span>";
                    
                    ret_str+="<a data-toggle=\"tooltip\" title=\""+movies[current_index]["name"]+"\" href=\"/video_player/?play="+movies[current_index]["unique_id"]+"&type=movie\">";
                    ret_str+="<img style=\"border-radius: 8%;cursor: pointer;\" src=\""+movies[current_index]["img_url"];
                    ret_str+="\" alt=\""+movies[current_index]["name"]+"\" onclick=\"present_video('"+movies[current_index]["movie_url"]+"');\" width=\""+img_w+"\" height=\""+img_h+"\">";
                    ret_str+="</a>";
                    
                    ret_str+="</span>";
                     
                    //ret_str+="</div>";
                     
                    ret_str+="<span>  </span>";
                } 
            ret_str+="</div>";}
            
            ret_str+="</div>";
            ret_str+="<a class=\"carousel-control-prev\" href=\"#"+target_id+"\" data-slide=\"prev\">";
            ret_str+="<span class=\"carousel-control-prev-icon\"></span></a>";
            ret_str+="<a class=\"carousel-control-next\" href=\"#"+target_id+"\" data-slide=\"next\">";
            ret_str+="<span class=\"carousel-control-next-icon\"></span></a>";
            ret_str+="</div>";
            ret_str+="</div>";
            
            ret_str+="<br/>";
        }
    );
        
        $("#video_files").html(ret_str);
   }});
   /*$(document).ready(function(){
   console.log(ids)
    ids.forEach(function(id){
    $(id).carousel();});
    });*/

}

function video_scroll(el){
    console.log(el.scrollTop )
}

function present_video(relative_path){
    location.replace("/video_player?play="+relative_path);}

function rescanfiles(type){
    let url_list_dir="/utils/scan_video_db";
    let wait_str="<div style=\"color:orange;\">";
    wait_str+="<svg width=\"1em\" height=\"1em\" viewBox=\"0 0 16 16\" class=\"bi bi-clock-history\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\">";
    wait_str+="<path fill-rule=\"evenodd\" d=\"M8.515 1.019A7 7 0 0 0 8 1V0a8 8 0 0 1 .589.022l-.074.997zm2.004.45a7.003 7.003 0 0 0-.985-.299l.219-.976c.383.086.76.2 1.126.342l-.36.933zm1.37.71a7.01 7.01 0 0 0-.439-.27l.493-.87a8.025 8.025 0 0 1 .979.654l-.615.789a6.996 6.996 0 0 0-.418-.302zm1.834 1.79a6.99 6.99 0 0 0-.653-.796l.724-.69c.27.285.52.59.747.91l-.818.576zm.744 1.352a7.08 7.08 0 0 0-.214-.468l.893-.45a7.976 7.976 0 0 1 .45 1.088l-.95.313a7.023 7.023 0 0 0-.179-.483zm.53 2.507a6.991 6.991 0 0 0-.1-1.025l.985-.17c.067.386.106.778.116 1.17l-1 .025zm-.131 1.538c.033-.17.06-.339.081-.51l.993.123a7.957 7.957 0 0 1-.23 1.155l-.964-.267c.046-.165.086-.332.12-.501zm-.952 2.379c.184-.29.346-.594.486-.908l.914.405c-.16.36-.345.706-.555 1.038l-.845-.535zm-.964 1.205c.122-.122.239-.248.35-.378l.758.653a8.073 8.073 0 0 1-.401.432l-.707-.707z\"/>";
    wait_str+="<path fill-rule=\"evenodd\" d=\"M8 1a7 7 0 1 0 4.95 11.95l.707.707A8.001 8.001 0 1 1 8 0v1z\"/>";
    wait_str+="<path fill-rule=\"evenodd\" d=\"M7.5 3a.5.5 0 0 1 .5.5v5.21l3.248 1.856a.5.5 0 0 1-.496.868l-3.5-2A.5.5 0 0 1 7 9V3.5a.5.5 0 0 1 .5-.5z\"/>";
    wait_str+="</svg>Scanning ... </div>";
    
    let ready_str="<div  onclick=\"rescanfiles();\" style=\"color:green;\">";
    ready_str+="<svg width=\"1em\" height=\"1em\" viewBox=\"0 0 16 16\" class=\"bi bi-arrow-clockwise\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\">";
    ready_str+="<path fill-rule=\"evenodd\" d=\"M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z\"/>";
    ready_str+="<path d=\"M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z\"/>";
    ready_str+="</svg>Scan</div>";
    
    let error_str="<div  onclick=\"rescanfiles();\" style=\"color:red;\">";
    error_str+="<svg width=\"1em\" height=\"1em\" viewBox=\"0 0 16 16\" class=\"bi bi-arrow-clockwise\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\">";
    error_str+="<path fill-rule=\"evenodd\" d=\"M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z\"/>";
    error_str+="<path d=\"M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z\"/>";
    error_str+="</svg>Scan error</div>";
    
    let busy_str="<div style=\"color:orange;\">";
    busy_str+="<svg width=\"1em\" height=\"1em\" viewBox=\"0 0 16 16\" class=\"bi bi-clock-history\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\">";
    busy_str+="<path fill-rule=\"evenodd\" d=\"M8.515 1.019A7 7 0 0 0 8 1V0a8 8 0 0 1 .589.022l-.074.997zm2.004.45a7.003 7.003 0 0 0-.985-.299l.219-.976c.383.086.76.2 1.126.342l-.36.933zm1.37.71a7.01 7.01 0 0 0-.439-.27l.493-.87a8.025 8.025 0 0 1 .979.654l-.615.789a6.996 6.996 0 0 0-.418-.302zm1.834 1.79a6.99 6.99 0 0 0-.653-.796l.724-.69c.27.285.52.59.747.91l-.818.576zm.744 1.352a7.08 7.08 0 0 0-.214-.468l.893-.45a7.976 7.976 0 0 1 .45 1.088l-.95.313a7.023 7.023 0 0 0-.179-.483zm.53 2.507a6.991 6.991 0 0 0-.1-1.025l.985-.17c.067.386.106.778.116 1.17l-1 .025zm-.131 1.538c.033-.17.06-.339.081-.51l.993.123a7.957 7.957 0 0 1-.23 1.155l-.964-.267c.046-.165.086-.332.12-.501zm-.952 2.379c.184-.29.346-.594.486-.908l.914.405c-.16.36-.345.706-.555 1.038l-.845-.535zm-.964 1.205c.122-.122.239-.248.35-.378l.758.653a8.073 8.073 0 0 1-.401.432l-.707-.707z\"/>";
    busy_str+="<path fill-rule=\"evenodd\" d=\"M8 1a7 7 0 1 0 4.95 11.95l.707.707A8.001 8.001 0 1 1 8 0v1z\"/>";
    busy_str+="<path fill-rule=\"evenodd\" d=\"M7.5 3a.5.5 0 0 1 .5.5v5.21l3.248 1.856a.5.5 0 0 1-.496.868l-3.5-2A.5.5 0 0 1 7 9V3.5a.5.5 0 0 1 .5-.5z\"/>";
    busy_str+="</svg>Still Scanning ... </div>";
    
    $("#scan_status").html(wait_str);
    $.ajax({url: url_list_dir, success: function(result){
        $("#scan_status").html(ready_str);
        if(type!=undefined){
            if(type=="show"){
                load_shows();}
            else if(type=="movie"){
                load_videos();}
        }
    },
    error:function(result,status,error){
        if(result.status == 501){
            $("#scan_status").html(busy_str);
        }
        else{
            $("#scan_status").html(error_str);}
        
        if(type!=undefined){
            if(type=="show"){
                load_shows();}
            else if(type=="movie"){
                load_videos();}
        }
    }
    
    });
}

function load_description(uuid,type){
    var url_list_dir="/utils/description?uuid="+uuid+"&type="+type;
   //console.log(url_list_dir);
   $.ajax({url: url_list_dir, success: function(result){
   //console.log(result);
       if(result.length==1){
           movie_data=result[0];
           //console.log(movie_data);
           $("#description_title").html(movie_data["movie_title"]);
           $("#description_body").html(movie_data["descript_html"]);
       }
       
   }});
}

function addJumpOnVideoEnd(url){
let player = videojs('my-video');
player.on('volumechange', () => {
    //console.log('volume changed: '+player.volume()+' previous value: '+sessionStorage.getItem('playerAudioVolume'));
    sessionStorage.setItem('playerAudioVolume', player.volume());
})
player.on('ended', function() {
  setTimeout(function(){
    window.location.href = url;
}, 3000);
    //alert('videoended next:'+url);
  
});
}
