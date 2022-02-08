// $(document).ready(function() {
//     // Setup - add a text input to each footer cell
//     $('#example thead tr').clone(true).appendTo( '#example thead' );
//     $('#example thead tr:eq(1) th').each( function (i) {
//         var title = $(this).text();
//         $(this).html( '<input type="text" placeholder="Search" />' );
 
//         $( 'input', this ).on( 'keyup change', function () {
//             if ( table.column(i).search() !== this.value ) {
//                 table
//                     .column(i)
//                     .search( this.value )
//                     .draw();
//             }
//         } );
//     } );
    
//     var table = $('#example').DataTable( {
//         orderCellsTop: true,
//         fixedHeader: true,
//          "lengthMenu": [[-1, 10, 25, 50, 100], ["All", 10, 25, 50, 100]],
//          //"dom": '<"top"ifl>rt<"bottom"ip><"clear">',
        
//     } );
// } );

// $(document).ready(function() {
//     // Setup - add a text input to each footer cell
//     ;
//     $('#closeoutsheet thead tr:eq(1) th').each( function (i) {
//         var title = $(this).text();
//         $(this).html( '<input type="text" placeholder="Search" />' );
 
//         $( 'input', this ).on( 'keyup change', function () {
//             if ( table.column(i).search() !== this.value ) {
//                 table
//                     .column(i)
//                     .search( this.value )
//                     .draw();
//             }
//         } );
//     } );
    
//     var table = $('#closeoutsheet').DataTable( {
//         orderCellsTop: true,
//         fixedHeader: true,
//          "lengthMenu": [[-1, 10, 25, 50, 100], ["All", 10, 25, 50, 100]],
//          "dom": '<"wrapper"f>',
        
//     } );
// } );

// $(document).ready(function() {
//   // Setup - add a text input to each footer cell
 
//   $('#table1 thead tr').clone(true).appendTo( '#table1 thead' );
//   $('#table1 thead tr:eq(1) th').each( function (i) {
//       var title = $(this).text();
      
//       $(this).html( '<input type="text" placeholder="Search" />' );

//       $( 'input', this ).on( 'keyup change', function () {
//           if ( table.column(i).search() !== this.value ) {
//               table
//                   .column(i)
//                   .search( this.value )
//                   .draw();
//           }
//       } );
//   } );

//     var table = $('#table1').DataTable( {
//         orderCellsTop: true,
//         fixedHeader: true,
//         "lengthMenu": [[-1, 10, 25, 50, 100], ["All", 10, 25, 50, 100]],
//         //"dom": '<"top"ifl>rt<"bottom"ip><"clear">',
//   } );
// } );

// $(document).ready(function() {
//   // Setup - add a text input to each footer cell
//   $('#table2 thead tr').clone(true).appendTo( '#table2 thead' );
//   $('#table2 thead tr:eq(1) th').each( function (i) {
//       var title = $(this).text();
//       $(this).html( '<input type="text" placeholder="Search" />' );

//       $( 'input', this ).on( 'keyup change', function () {
//           if ( table.column(i).search() !== this.value ) {
//               table
//                   .column(i)
//                   .search( this.value )
//                   .draw();
//           }
//       } );
//   } );

//   var table = $('#table2').DataTable( {
//       orderCellsTop: true,
//       fixedHeader: true,
//        "lengthMenu": [[-1, 10, 25, 50, 200], ["All", 10, 25, 50, 200]],
//        //"dom": '<"top"ifl>rt<"bottom"ip><"clear">',
       
//        //20211209 Ishna-YHS date format sorting for column 6
//        "columnDefs": [{
//         "render": function(data) { 
//             return moment(data).format('DD-MMM-YYYY ');
//         },
//         "targets": 6
//        }]
//        //20211209 Ishna-YHS date format sorting for column 6
//    });
// });

// $(document).ready(function() {
//     // Setup - add a text input to each footer cell
//     $('#table3 thead tr').clone(true).appendTo( '#table3 thead' );
//     $('#table3 thead tr:eq(1) th').each( function (i) {
//         var title = $(this).text();
//         $(this).html( '<input type="text" placeholder="Search" />' );

//         $( 'input', this ).on( 'keyup change', function () {
//             if ( table.column(i).search() !== this.value ) {
//                 table
//                     .column(i)
//                     .search( this.value )
//                     .draw();
//             }
//         } );
//     } );

//     var table = $('#table3').DataTable( {
//         orderCellsTop: true,
//         fixedHeader: true,
//             "lengthMenu": [[-1, 10, 25, 50, 200], ["All", 10, 25, 50, 200]],
//             //"dom": '<"top"ifl>rt<"bottom"ip><"clear">',
//     } );
// } );

// $(document).ready(function() {
//     // Setup - add a text input to each footer cell
//     $('#table4 thead tr').clone(true).appendTo( '#table4 thead' );
//     $('#table4 thead tr:eq(1) th').each( function (i) {
//         var title = $(this).text();
//         $(this).html( '<input type="text" placeholder="Search" />' );
  
//         $( 'input', this ).on( 'keyup change', function () {
//             if ( table.column(i).search() !== this.value ) {
//                 table
//                     .column(i)
//                     .search( this.value )
//                     .draw();
//             }
//         } );
//     } );
  
//     var table = $('#table4').DataTable( {
//         orderCellsTop: true,
//         fixedHeader: true,
//          "lengthMenu": [[-1, 10, 25, 50, 200], ["All", 10, 25, 50, 200]],
//          //"dom": '<"top"ifl>rt<"bottom"ip><"clear">',
//     } );
// } );
  
// $(document).ready(function() {
//     // Setup - add a text input to each footer cell
    
//     $('#table5 thead tr').clone(true).appendTo( '#table5 thead' );
//     $('#table5 thead tr:eq(1) th').each( function (i) {
//         var title = $(this).text();
//         $(this).html( '<input type="text" placeholder="Search" />' );
  
//         $( 'input', this ).on( 'keyup change', function () {
//             if ( table.column(i).search() !== this.value ) {
//                 table
//                     .column(i)
//                     .search( this.value )
//                     .draw();
//             }
//         } );
//     } );
  
//     var table = $('#table5').DataTable( {
//         orderCellsTop: true,
//         fixedHeader: true,
//          "lengthMenu": [[-1, 10, 25, 50, 200], ["All", 10, 25, 50, 200]],
//          //"dom": '<"top"ifl>rt<"bottom"ip><"clear">',
//     } );
// } );

// $(document).ready(function() {
//     // Setup - add a text input to each footer cell
//     $('#table6 thead tr').clone(true).appendTo( '#table6 thead' );
//     $('#table6 thead tr:eq(1) th').each( function (i) {
//         var title = $(this).text();
//         $(this).html( '<input type="text" placeholder="Search" />' );
  
//         $( 'input', this ).on( 'keyup change', function () {
//             if ( table.column(i).search() !== this.value ) {
//                 table
//                     .column(i)
//                     .search( this.value )
//                     .draw();
//             }
//         } );
//     } );
  
//     var table = $('#table6').DataTable( {
//         orderCellsTop: true,
//         fixedHeader: true,
//          "lengthMenu": [[-1, 10, 25, 50, 200], ["All", 10, 25, 50, 200]],
//          //"dom": '<"top"ifl>rt<"bottom"ip><"clear">',
//     } );
// } );
  
// $(document).ready(function() {
//     // Setup - add a text input to each footer cell
//     $('#table7 thead tr').clone(true).appendTo( '#table7 thead' );
//     $('#table7 thead tr:eq(1) th').each( function (i) {
//         var title = $(this).text();
//         $(this).html( '<input type="text" placeholder="Search" />' );
  
//         $( 'input', this ).on( 'keyup change', function () {
//             if ( table.column(i).search() !== this.value ) {
//                 table
//                     .column(i)
//                     .search( this.value )
//                     .draw();
//             }
//         } );
//     } );
  
//     var table = $('#table7').DataTable( {
//         orderCellsTop: true,
//         fixedHeader: true,
//          "lengthMenu": [[-1, 10, 25, 50, 200], ["All", 10, 25, 50, 200]],
//          //"dom": '<"top"ifl>rt<"bottom"ip><"clear">',
//     } );
// } );

// $(document).ready(function () {
//     $('table.display').each(function () {
//         var datatableid = '#' + $(this).attr('id');
//         $(datatableid + ' thead tr').clone(true).appendTo(datatableid + ' thead');
//         $(datatableid + ' thead tr:eq(1) th').each(function (i) {
//             var title = $(this).text();
//             $(this).html('<input type="text" placeholder="Search" />');
//         });
//         var table = $(datatableid).DataTable({
//             initComplete: function () {
//                 // Apply the search
//                 this.api().columns().every(function () {
//                     var that = this;
//                     $('input', this.header()).on('keyup change clear',
//                         function () {
//                             if (that.search() !== this.value) {
//                                 that
//                                     .search(this.value)
//                                     .draw();
//                             }
//                         });
//                 });
//             },
//         orderCellsTop: true,
//         fixedHeader: true,
//          "lengthMenu": [[-1, 10, 25, 50, 200], ["All", 10, 25, 50, 200]],
//         });
//     });
// });