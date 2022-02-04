$(document).ready(function()

{
  $(".btn").click(function()
  {
    $.ajax({

      url: "../loadajax3",
      type : 'get',
      data : {
        button_text: $(this).text()
      },
      success: function (response){
        $(".btn").text(response.context) 
        // alert(response.context)  
      }


    })
    })

})




function fadein(event, tableclick, tablepopup) { 
  var x = document.getElementById(tableclick); 
  var y = document.getElementById(tablepopup); 
  var data = event.currentTarget.firstElementChild.innerText 
  // alert(data) 
  x.style.animation = 'mymoveout .5s ease'; 
  y.style.animation = 'slide-in .5s ease'; 
  y.style.display = "block"; 
          $.ajax({  
            url: "/studiesjs",  
            type : 'GET',  
            data : {  
            "data": data  
            },  
            success: function (response){  
            // $(".btn").text(response.buttontext)   
            // alert("xyz")  
            var dfstudieslist = response.dfstudieslist  
            var nestedheader = response.nestedheader  
            var dfstudiesdict = response.dfstudiesdict 
            alert(dfstudieslist)
            $(document).ready(function() {
              $('table.raretable').each(function () {
                var datatableid = '#' + $(this).attr('id');
                $(datatableid + ' thead tr').clone(true).appendTo(datatableid + ' thead');
                $(datatableid + ' thead tr:eq(1) th').each(function (i) {
                    var title = $(this).text();
                    $(this).html('<input type="text" placeholder="Search" />');
                });
              
              $(datatableid).DataTable( { 
                
                  data: dfstudieslist,                    
                  "bDestroy":true, 
                  columns: [ 
                      { title: "Study Action No" ,"name" : "Study" }, 
                      { title: "Study Name" }, 
                      { title: "Action With" }, 
                      { title: "test","name":"test", "visible": true },     
                  ], 
                  initComplete: function () {
                    // Apply the search
                    this.api().columns().every(function () {
                        var that = this;
                        $('input', this.header()).on('keyup change clear',
                            function () {
                                if (that.search() !== this.value) {
                                    that
                                        .search(this.value)
                                        .draw();
                                }
                            });
                    });
                },
                  "columnDefs": [ 
                    { "targets" : [3], 
                       "mRender": function ( data,row) { 
                         return '<a href="/pmtrepviewall'+ '/' + data +'/view'+'">'+ data + '</a>'; 
                       }}, 
                  ] 
              }); 
            }); 
          });
          } 
          }) 
} 

 

function fadeout(tableclick,tablepopup) {
  var x = document.getElementById(tableclick);
  var y = document.getElementById(tablepopup);
  x.style.animation = 'mymovein 2.5s ease';
  y.style.animtion = 'slide-out .5s ease';
  setTimeout(() => {
    y.style.display = 'none';
  }, 500);
}

function phasesurl (id,phase)

{
    
    if (phase == '') {

        document.location.href = "../reppmt"

    }else{
        document.location.href = phase // adds the phase part to the end of the reppmt- it is then caught by views
        
}
   
}

function maketabactive (id){
    ///make the tab (button active)
    if (id===""){

        id="allphases"
    }
    var gettab = document.getElementById(id)
    gettab.className += " active"

}

function openReport(evt, ReportName) {
    var i, tabcontent, tablinks;
    
    tabcontent = document.getElementsByClassName("tabcontent");
    //Gets tabs and sets diaply to none
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(ReportName).style.display = "block";

    evt.currentTarget.className += " active";
    //evt.currentTarget.style.visibility = 'hidden';
  }
document.getElementById("defaultOpen").click(); //default open