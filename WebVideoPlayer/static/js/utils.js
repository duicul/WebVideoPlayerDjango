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
        console.log(result);
        var ret_str="<div class=\"list-group\">";
        var space_ind=0;
        console.log(Object.keys(result));
        result.forEach(function(item_par){
            ret_str+="<div class=\"list-group-item\" onclick=\"present_video('"+item_par[1].replace("\\","/")+"');\" >"+item_par[0];
            ret_str+="</div>";
        }
        
        );
        ret_str+="</div>";
        $("#video_files").html(ret_str);
   }
   });
    
    
}

function present_video(relative_path){
    location.replace("/video_player?play=/media/"+relative_path);
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