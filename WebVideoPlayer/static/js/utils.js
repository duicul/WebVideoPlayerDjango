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
function load_videos(){
   var url_list_dir="/utils/list_video_files";
   console.log(url_list_dir);
   $.ajax({url: url_list_dir, success: function(result){
        let img_w=250;
        let img_h=250;
        movies_per_slide=Math.floor(window.innerWidth*0.9/img_w);
        slides=Math.ceil(result.length/movies_per_slide)
        console.log(movies_per_slide)
        console.log(slides)
        let ret_str="<div id=\"demo\" class=\"carousel slide\" data-ride=\"carousel\" style=\"background-color: lightblue;\">";
        ret_str+="<ul class=\"carousel-indicators\">";
        ret_str+="<li data-target=\"#demo\" data-slide-to=\"0\" class=\"active\"></li>";
        var i;
        for (i = 1; i < slides; i++) {
            ret_str+="<li data-target=\"#demo\" data-slide-to=\""+i+"\"></li>";
        } 
        ret_str+="</ul>";
        ret_str+="<div class=\"carousel-inner\">";
            ret_str+="<div class=\"carousel-item active\" style=\"text-align: center\">";
            for (i = 0; i < movies_per_slide; i++) {
                ret_str+="<a href=\"/video_player/?play="+result[i]["movie_url"]+"\">";
                ret_str+="<img style=\"border-radius: 8%;cursor: pointer;\" src=\""+result[i]["img_url"];
                ret_str+="\" alt=\""+result[i]["name"]+"\" width=\""+img_w+"\" height=\""+img_h+"\">";
                ret_str+="</a>";
                ret_str+="<span> </span>";
            } 
            ret_str+="</div>";
            var slide_i;
            for (slide_i = 1; slide_i < slides;slide_i++) {
            ret_str+="<div class=\"carousel-item\" style=\"text-align: center\">";
                for (i = 0; i < movies_per_slide; i++) {
                    current_index=slide_i*movies_per_slide+i;
                    if(current_index>=result.length)
                        break;
                    ret_str+="<a href=\"/video_player/?play="+result[current_index]["movie_url"]+"\">";
                    ret_str+="<img style=\"border-radius: 8%;cursor: pointer;\" src=\""+result[current_index]["img_url"];
                    ret_str+="\" alt=\""+result[current_index]["name"]+"\" onclick=\"present_video('"+result[current_index]["movie_url"]+"');\" width=\""+img_w+"\" height=\""+img_h+"\">";
                    ret_str+="</a>";
                    ret_str+="<span>  </span>";
                } 
            ret_str+="</div>";
            
            }
        ret_str+="</div>";
        ret_str+="<a class=\"carousel-control-prev\" href=\"#demo\" data-slide=\"prev\">";
        ret_str+="<span class=\"carousel-control-prev-icon\"></span></a>";
        ret_str+="<a class=\"carousel-control-next\" href=\"#demo\" data-slide=\"next\">";
        ret_str+="<span class=\"carousel-control-next-icon\"></span></a>";
        ret_str+="</div>";
        console.log(result);
       /* var ret_str="<div class=\"list-group\">";
        var space_ind=0;
        console.log(Object.keys(result));
        result.forEach(function(item_par){
        console.log(item_par["name"])
            ret_str+="<div class=\"list-group-item\" onclick=\"present_video('"+item_par["movie_url"]+"');\" >";
            ret_str+="<img src=\"";
            ret_str+=item_par["img_url"];
            ret_str+="\" alt=\""+item_par["name"]+"\" width=\"100\" height=\"100\">";
            ret_str+="</div>";
        }
        
        );
        ret_str+="</div>";*/
        $("#video_files").html(ret_str);
   }//put multiple videos in one carousel item
   });
    /*
    <div id="demo" class="carousel slide" data-ride="carousel">
  <ul class="carousel-indicators">
    <li data-target="#demo" data-slide-to="0" class="active"></li>
    <li data-target="#demo" data-slide-to="1"></li>
    <li data-target="#demo" data-slide-to="2"></li>
  </ul>
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="la.jpg" alt="Los Angeles" width="1100" height="500">
      <div class="carousel-caption">
        <h3>Los Angeles</h3>
        <p>We had such a great time in LA!</p>
      </div>   
    </div>
    <div class="carousel-item">
      <img src="chicago.jpg" alt="Chicago" width="1100" height="500">
      <div class="carousel-caption">
        <h3>Chicago</h3>
        <p>Thank you, Chicago!</p>
      </div>   
    </div>
    <div class="carousel-item">
      <img src="ny.jpg" alt="New York" width="1100" height="500">
      <div class="carousel-caption">
        <h3>New York</h3>
        <p>We love the Big Apple!</p>
      </div>   
    </div>
  </div>
  <a class="carousel-control-prev" href="#demo" data-slide="prev">
    <span class="carousel-control-prev-icon"></span>
  </a>
  <a class="carousel-control-next" href="#demo" data-slide="next">
    <span class="carousel-control-next-icon"></span>
  </a>
</div>
    */
    
}



function present_video(relative_path){
    location.replace("/video_player?play="+relative_path);
    /*let str_src="<video";
    str_src+="id=\"my-video\"";
    str_src+="class=\"video-js\"";
    str_src+="controls=\"true\"";
    str_src+="preload=\"auto\"";
    str_src+="width=\"640\"";
    str_src+="height=\"264\"";
    str_src+="data-setup=\"{}\" >";
    str_src+="<source src=\""+"/media/"+relative_path+"\"/>";
    str_src+="<p class=\"vjs-no-js\">";
    str_src+= " To view this video please enable JavaScript, and consider upgrading to a ";
    str_src+= " web browser that";
    str_src+=" <a href=\"https://videojs.com/html5-video-support/\" target=\"_blank\"";
    str_src+=" >supports HTML5 video</a>";
    str_src+="</p></video>";
    $("#video_window").html(str_src);*/
  /*    let myVideo = videojs('my-video');
    myVideo.src([
        {type: "application/x-mpegURL", src: "/media/"+relative_path},
    ]); 
    myVideo.dimensions(720,480);
    myVideo.reset()
   myVideo.load();  
   myVideo.play();
   myVideo.triggerReady();
   myVideo.show();
   console.log(myVideo.duration())*/
      
}