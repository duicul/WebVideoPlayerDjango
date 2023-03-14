function loadBook(){
  console.log("random");
  var book = ePub("/media/Toshiba_drive/Heaven's%20River%20by%20Dennis%20E.%20Taylor.epub", { 'restore': true, 'sidebarReflow': true });
  //book.open("/media/Toshiba_drive/Heaven's%20River%20by%20Dennis%20E.%20Taylor.epub")
  var pl = book.pagelist
  console.log(pl)
  console.log("opened "+book.opened)
  var rendition = book.renderTo("ebookarea", { flow: 'paginated',width: 600, height: 400});
  var displayed = rendition.display();
  displayed.then(function() {
    console.log('rendition.currentLocation():', rendition.currentLocation());
    });
  console.log(displayed);
    book.on('book:pageChanged', function(location){
    console.log('Current page: ' + location.anchorPage);
    });
  
  var pl = book.pagelist
  var tablecontentHTML = "";
  console.log(pl)
  console.log("opened "+book.opened)
  rendition.display(8)
  book.ready.then((b) => {
      console.log("Navigation "+book.navigation);
      book.navigation.forEach(function(item){console.log("item "+JSON.stringify(item));
                                            tablecontentHTML+="<p class=\"p-p6\"><a href=\""+item["href"]+"\" class=\"calibre\">"+item["label"]+"</a></p>";
                                            });
      
  }).then((b)=>{$("#tablecontent").html(tablecontentHTML);});
  book.ready.then((b) => {
            return book.locations.generate();
        }).then(locations => {
            console.log("Total Pages?: ", locations.length);
        });
    /*book.ready.then(function(pageList) {
        console.log('Total pages: ' + book.pagination.totalPages);
    });*/
    displayed.then(function() {
    console.log('rendition.currentLocation():', rendition.currentLocation());
});
    document.getElementById("Nextbutton").addEventListener("click", function(){rendition.next()}); 
    document.getElementById("Prevbutton").addEventListener("click", function(){rendition.prev()});
  }