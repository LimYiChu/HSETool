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

function fadein(event, that, tablepopup) {    
    var $x = $($(that).closest('div .divclick'));
    var $y = $($(that).closest('div .divclick').siblings('.popup'));  
    $x.css("animaton", "mymoveout .5s ease");
    $y.css("animation", "slide-in .5s ease");
    $y.css("display", "block");

    var data = event.currentTarget.firstElementChild.innerText  
    
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
            
            }  
          })  
}
  
function fadeout(that) {

    var $x = $($(that).closest('div .popup').siblings('.divclick'));
    var $y = $($(that).closest('div .popup'))
    $x.css("animaton", "mymovein 2.5s ease")
    $y.css("animation", "slide-out .5s ease");
    setTimeout(() => {
      $y.css("display", "none");
    }, 500);
}

$( document ).ready(function() {
  $( '.tablinks' ).click(function() {
    var $x = $('.divclick');
    var $y = $('.popup');
    if($y.css('display') !== 'none')
    { 
      $x.css("animaton", "mymovein 2.5s ease")
      $y.css("animation", "slide-out .5s ease");
      setTimeout(() => {
        $y.css("display", "none");
      }, 500);
    }
  });
});
