$(document).ready(function() {
    // Setup - add a text input to each footer cell
    $('table.fixedtable').each(function () {
    var datatableid = '#' + $(this).attr('id');
    $(datatableid + ' thead tr').clone(true).appendTo(datatableid + ' thead'); //clone headers
    $(datatableid + ' thead tr:eq(1) th').each(function (i) {

    var title = $(this).text();
    $(this).html( '<input type="text" placeholder="Search" class="column_search" />' );
    } );
    // DataTable
    var table = $(datatableid).DataTable({
      orderCellsTop: true,
      "lengthMenu": [[-1, 10, 25, 50, 200], ["All", 10, 25, 50, 200]],
    });
// Apply the search
    $( datatableid +' thead'  ).on( 'keyup', ".column_search",function () {
        table
            .column( $(this).parent().index() )
            .search( this.value )
            .draw();

            
    } );
    
} );
})

function fadein(event, tableclick, tablepopup) {  
    var x = document.getElementById(tableclick);  
    var y = document.getElementById(tablepopup);  
    var data = event.currentTarget.firstElementChild.innerText  
    
    x.style.animation = 'mymoveout .5s ease';  
    y.style.animation = 'slide-in .5s ease';  
    y.style.display = "block";  
            $.ajax({   
              url: "/" + tablepopup,   
              type : 'GET',   
              data : {   
              "data": data   
              },   
              success: function (response){   
                 
              var dflist = response.dflist   
              var nestedheader = response.nestedheader    
              var dynamicheaders = []; 
              for (var i=0; i < nestedheader.length; i++ ) { 
                dynamicheaders.push({ 
                          "sTitle": nestedheader[i], 
                 }); 
              }; 
          
            $(document).ready(function() { 
              $('table.nestedtable').each(function () {
                var datatableid = '#' + $(this).attr('id');
                
                if ( $.fn.dataTable.isDataTable(datatableid) ) {
                  $(datatableid).DataTable().destroy();
                  $(datatableid).empty();
                }
                
                $('.caption').html(data);
                
                var table = $(datatableid).DataTable( {  
                    data: dflist,      
                                   
                  "aoColumns": dynamicheaders, 
                  "columnDefs": [  
                    { "targets" : [0],  
                        "mRender": function ( data,row,column) {  
                          return '<a href="/pmtrepviewall'+ '/' + column[5]+'/view'+'">'+ data + '</a>';  
                        }},  
                  ],
                  "bDestroy":true, 
                  orderCellsTop: true,
                  "lengthMenu": [[-1, 10, 25, 50, 200], ["All", 10, 25, 50, 200]],
                });  
                
                $(datatableid + ' thead tr').clone(false).appendTo(datatableid + ' thead'); //clone headers
                $(datatableid + ' thead tr:eq(1) th').each(function (i) {
                $(this).html( '<input type="text" placeholder="Search" class="column_search" />' );
                $(this).removeClass( "sorting sorting_asc sorting_desc" )
                } ); 
                
                $( datatableid +' thead'  ).on( 'keyup', ".column_search",function () {
                  table
                      .column( $(this).parent().index() )
                      .search( this.value )
                      .draw(); 
                } );
                
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
