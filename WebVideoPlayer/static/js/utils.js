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
    let myVideo = videojs('my-video');
    myVideo.src([
        {type: "application/x-mpegURL", src: "/media/"+relative_path},
    ]); 
    myVideo.load();  
   myVideo.play();
      
}