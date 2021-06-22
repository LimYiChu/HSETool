
$(document).ready(function() {
    // Setup - add a text input to each footer cell
    ;
    $('#closeoutsheet thead tr:eq(1) th').each( function (i) {
        var title = $(this).text();
        $(this).html( '<input type="text" placeholder="Search" />' );
 
        $( 'input', this ).on( 'keyup change', function () {
            if ( table.column(i).search() !== this.value ) {
                table
                    .column(i)
                    .search( this.value )
                    .draw();
            }
        } );
    } );
    
    var table = $('#closeoutsheet').DataTable( {
        orderCellsTop: true,
        fixedHeader: true,
         "lengthMenu": [[-1, 10, 25, 50, 100], ["All", 10, 25, 50, 100]],
         "dom": '<"wrapper"f>',
        
    } );
} );

// $(document).ready(function() {
//     $('table.display').DataTable();

    
    
// } );

  $(document).ready(function() {
    // Setup - add a text input to each footer cell
    
    $('#table5 thead tr').clone(true).appendTo( '#table5 thead' );
    $('#table5 thead tr:eq(1) th').each( function (i) {
        var title = $(this).text();
        $(this).html( '<input type="text" placeholder="Search" />' );
  
        $( 'input', this ).on( 'keyup change', function () {
            if ( table.column(i).search() !== this.value ) {
                table
                    .column(i)
                    .search( this.value )
                    .draw();
            }
        } );
    } );
  
    var table = $('#table5').DataTable( {
        orderCellsTop: true,
        fixedHeader: true,
         "lengthMenu": [[-1, 10, 25, 50, 200], ["All", 10, 25, 50, 200]],
         //"dom": '<"top"ifl>rt<"bottom"ip><"clear">',
    } );
  } );



//   $(document).ready(function() {
//     // Setup - add a text input to each footer cell
//     for (var k =1;k<7;k++) 
  
//   { 
//     var tableid = '#table'
//     var finaltableid = tableid.concat(k)
     
  
//     $(finaltableid + ' thead tr').clone(true).appendTo(finaltableid + ' thead' );
//     $(finaltableid + ' thead tr:eq(1) th').each( function (i) {
//         var title = $(this).text();
//         $(this).html( '<input type="text" placeholder="Search" />' );
  
//         $( 'input', this ).on( 'keyup change', function () {
            
//             if ( table.column(i).search() !== this.value ) {
//                 alert(this.value)
//                 table
//                     .column(i)
//                     .search( this.value )
//                     .draw();
//             }
//         } );
//     } );
  
//     var table = $(finaltableid).DataTable( {
//         orderCellsTop: true,
//         fixedHeader: true,
//          "lengthMenu": [[-1, 10, 25, 50, 200], ["All", 10, 25, 50, 200]],
//          //"dom": '<"top"ifl>rt<"bottom"ip><"clear">',
//     } );}
//   } );

function openReport(evt, ReportName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(ReportName).style.display = "block";
    evt.currentTarget.className += " active";
    
  }
document.getElementById("defaultOpen").click(); //default open
