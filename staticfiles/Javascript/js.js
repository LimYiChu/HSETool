$(document).ready(function() {
    // Setup - add a text input to each footer cell
    $('#example thead tr').clone(true).appendTo( '#example thead' );
    $('#example thead tr:eq(1) th').each( function (i) {
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
 
    var table = $('#example').DataTable( {
        orderCellsTop: true,
        fixedHeader: true,
         "lengthMenu": [[-1, 10, 25, 50, 100], ["All", 10, 25, 50, 100]]
    } );
} );

$(document).ready(function() {
  // Setup - add a text input to each footer cell
  $('#table1 thead tr').clone(true).appendTo( '#table1 thead' );
  $('#table1 thead tr:eq(1) th').each( function (i) {
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

  var table = $('#table1').DataTable( {
      orderCellsTop: true,
      fixedHeader: true,
       "lengthMenu": [[-1, 10, 25, 50, 100], ["All", 10, 25, 50, 100]]
  } );
} );

$(document).ready(function() {
  // Setup - add a text input to each footer cell
  $('#table2 thead tr').clone(true).appendTo( '#table2 thead' );
  $('#table2 thead tr:eq(1) th').each( function (i) {
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

  var table = $('#table2').DataTable( {
      orderCellsTop: true,
      fixedHeader: true,
       "lengthMenu": [[-1, 10, 25, 50, 200], ["All", 10, 25, 50, 200]]
  } );
} );

$(document).ready(function() {
    // Setup - add a text input to each footer cell
    $('#table3 thead tr').clone(true).appendTo( '#table3 thead' );
    $('#table3 thead tr:eq(1) th').each( function (i) {
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
  
    var table = $('#table3').DataTable( {
        orderCellsTop: true,
        fixedHeader: true,
         "lengthMenu": [[-1, 10, 25, 50, 200], ["All", 10, 25, 50, 200]]
    } );
  } );
  
  $(document).ready(function() {
    // Setup - add a text input to each footer cell
    $('#table4 thead tr').clone(true).appendTo( '#table4 thead' );
    $('#table4 thead tr:eq(1) th').each( function (i) {
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
  
    var table = $('#table4').DataTable( {
        orderCellsTop: true,
        fixedHeader: true,
         "lengthMenu": [[-1, 10, 25, 50, 200], ["All", 10, 25, 50, 200]]
    } );
  } );
  
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
         "lengthMenu": [[-1, 10, 25, 50, 200], ["All", 10, 25, 50, 200]]
    } );
  } );
  

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
