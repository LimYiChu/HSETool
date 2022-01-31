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

var newarray = new Array() ;

newarray.push(nestedheader);

for (let i = 0; i < dfstudieslist.length; i++) {
  newarray.push(dfstudieslist[i])
};

var $table = $("#studydetailstable");
$table.html(""); //needed to clear previous data from table upon second click

//creating header
var columnCount = newarray[0].length;
var $thead = $('<thead>').addClass("thead-dark").appendTo($table);
var $row = $($thead[0].insertRow(-1));
for (var i = 0; i < columnCount; i++) {
    var $headerCell = $("<th />");
    $headerCell.html(newarray[0][i]);
    $row.append($headerCell);
}

//creating body
var $tbody = $('<tbody>').appendTo($table);
for (var i = 1; i < newarray.length; i++) {
  $row = $($tbody[0].insertRow(-1));
  for (var j = 0; j < columnCount; j++) {
      var $cell = $("<td />");
      $cell.html(newarray[i][j]);
      $row.append($cell);
  }
}

//add dynamic table to existing div
var $dvTable = $("#studydetails");
$dvTable.append($table);


// Setup - add a text input to each header cell
$('#studydetailstable thead tr').clone(true).appendTo( '#studydetailstable thead' );
$('#studydetailstable thead tr:eq(1) th').each( function (i) {
    var title = $(this).text();
    $(this).html( '<input type="text" placeholder="Search" />' );

    $( 'input', this ).on( 'keyup change', function () {
        // alert(this.value)
        
      if ( table.column(i).search() !== this.value ) {
            table
                .column(i)
                .search( this.value )
                .draw();
                
        }
    } );
} );

var table = $('#studydetailstable').DataTable( {
    'destroy': true,
    orderCellsTop: true,
    fixedHeader: true,
     "lengthMenu": [[-1, 10, 25, 50, 100], ["All", 10, 25, 50, 100]],
     //"dom": '<"top"ifl>rt<"bottom"ip><"clear">',
    
} );

        
     
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