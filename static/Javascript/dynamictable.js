function launchtable(that, event, tablepopup,urlcolumn) {
  fadein(that);
  ajaxcall(event, tablepopup,urlcolumn);
}

function fadein(that) {
  var $x = $($(that).closest('div .divclick'));
  var $y = $($(that).closest('div .divclick').siblings('.popup'));
  $x.css("animaton", "mymoveout .5s ease");
  $y.css("animation", "slide-in .5s ease");
  $y.css("display", "block");
}

var title;

function ajaxcall(event, tablepopup, urlcolumn) {
  var data;
  title = event.currentTarget.firstElementChild.innerText

// To get the item from hidden dynamicdiscipline column 
  try 
  {                                                             
    rowtarget = $($(event.currentTarget).children(".hiddenx"));
    data = rowtarget[0].innerText
  } 
  catch (error) 
  {
    data = event.currentTarget.firstElementChild.innerText;
  }

  $('.caption').html(title);

  $.ajax({
      url: "/dynamictable/" + tablepopup,
      type: 'GET',
      data: {
        "dynamictable": tablepopup,  
        "data": data,
      },
      rootid: tablepopup,

      success: function(response) {
          dynamictable(response, this.rootid, urlcolumn);
          dynamicchart(response, this.rootid);
          dynamictabledisc(response, this.rootid);
      }
  })
}

function dynamictable(response,rootid,urlcolumn=true) {

    var dflist = response.dflist
    var headerlist = response.headerlist
   


    var dynamicheaders = [];
    for (var i = 0; i < headerlist.length; i++) 
    {
        dynamicheaders.push({
            "sTitle": headerlist[i],
        });
    };
    
    $('table.dynamictable').each(function() 
    {
        var datatableid = '#' + $(this).attr('id');
        
        if ($.fn.dataTable.isDataTable(datatableid)) 
        {
            $(datatableid).DataTable().destroy();
            $(datatableid).empty();
        }

        var table = $(datatableid).DataTable(
        {
            data: dflist,

            "aoColumns": dynamicheaders,
            "columnDefs": 
            [{
                "targets": [0],
                "mRender": function(data, row, column) {
                    if (urlcolumn == true)
                    {
                        return '<a href="/pmtrepviewall' + '/' + column[5] + '/view' + '">' + data + '</a>';
                    }
                    else if (urlcolumn == false)
                    {
                        return data;
                    }
                }
            }, ],
            "bDestroy": true,
            orderCellsTop: true,
            pageLength: 50,
            "lengthMenu": 
            [
                [10, 25, 50, 200,-1],
                [10, 25, 50, 200, "All"]
            ],
            "createdRow": function(row, data, dataIndex, column) 
            {
                if (data[6] == 'Red') 
                {
                    return $(column[4]).addClass('table-danger')
                } 
                else if (data[6] == 'Yellow') 
                {
                    return $(column[4]).addClass('table-warning')
                } 
                else if (data[6] == 'Green') 
                {
                    return $(column[4]).addClass('table-success');
                }
            },
        });

        $(datatableid + ' thead tr').clone(false).appendTo(datatableid + ' thead'); //clone headers
        $(datatableid + ' thead tr:eq(1) th').each(function(i) {
            $(this).html('<input type="text" placeholder="Search" class="column_search" />');
            $(this).removeClass("sorting sorting_asc sorting_desc")
        });

        $(datatableid + ' thead').on('keyup', ".column_search", function() {
            table
                .column($(this).parent().index())
                .search(this.value)
                .draw();
        });
    });

    $('#buttonplaceindisumm').html(" <a class='article-title' href='/dynamicindisummexcel/" + title + 
    "' ><button type='button' class='btn btn-outline-primary btn-md;' style='width:150pt'>Download Excel</button></a>")

    $('#buttonplacedetails').html(" <a class='article-title' href='/dynamicstudiesexcel/" + title + 
    "' ><button type='button' class='btn btn-outline-primary btn-md;' style='width:150pt'>Download Excel</button></a>") 
    
    $('#buttonplacedissumm').html(" <a class='article-title' href='/dynamicstudiesdiscexcel/" + title + 
    "' ><button type='button' class='btn btn-outline-primary btn-md;' style='width:150pt'>Download Excel</button></a>")
    
    $('#buttonplacediscipline').html(" <a class='article-title' href='/dynamicdisciplineexcel/" + title + 
    "' ><button type='button' class='btn btn-outline-primary btn-md;' style='width:150pt'>Download Excel</button></a>") 

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

//fade out automatically when changing tabs
$(document).ready(function() {
  $('.tablinks').each(function() {
      $(this).on("click", function() {
          var $x = $('.divclick');
          var $y = $('.popup');

          if ($y.css('.popup') !== 'none') 
          {
            $x.css("animaton", "mymovein 2.5s ease")
              $y.css("animation", "slide-out .5s ease");
              setTimeout(() => {
                  $y.css("display", "none");
              }, 500);
          }

      });
  });
});


function dynamicchart(response,rootid) {
  
    google.charts.load("current", {
        packages: ["corechart"]
    });

    var dfstuckatlst = response.dfstuckatlst;
    values = response.multilst;
    
    var getdivs = $( '.' + rootid ).children()
    // for (let i = 0; i < getdivs.length; i++) {
    //     alert(getdivs.eq(i).attr('id'))
    // }
    // alert (getdivs)
    google.charts.setOnLoadCallback(function () { drawChart(values,rootid,getdivs); });
}
  

function drawChart(values,rootid,getdivs) {
  
    for (let i = 0; i < values.length; i++)
    {
    
    drawPieChart (values[i],i,rootid,getdivs[i])
    }
}


function drawPieChart (value,index,rootid,singlediv) {

    chartTitle = value[0][0]
    firstindex = chartTitle.lastIndexOf("///")+3
    lastindex = chartTitle.lastIndexOf(":::")
    var newtitle = chartTitle.substring(firstindex,lastindex );

    var data = google.visualization.arrayToDataTable(
        value
    );
    var options = {
        title:newtitle,
        titleTextStyle: 
        {
            color: 'black',
            fontSize: 16,
            bold: true,  
            italic: false,
        },
        width: 350,
        height: 270,
        backgroundColor: '#f3f2f2',
        pieHole: 0.4,
        pieSliceText: 'value',

        tooltip: 
        {
            text: 'value'
        },

        pieSliceTextStyle: 
        {
            bold: true,
            fontSize: 18,
            color: 'black'
        },

        chartArea: 
        {
            right: 20,
            bottom: 0,
            width: '100%',
            height: '80%'
        },

        legend: 
        {
            position: 'labeled',
            textStyle: {
                color: 'black',
                fontSize: 12.5
            }
        }
    };

    var chart = new google.visualization.PieChart(singlediv);
    chart.draw(data, options);chart.draw(data, options);
}

function openTab(evt, tabname) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("dyntabcontent");
    for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("dynamictabs");
    for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabname).style.display = "block";
    evt.currentTarget.className += " active";
    }
    $(document).ready(function() {
    document.getElementById("defaultOpen").click();  
})


function dynamictabledisc(response,rootid) {
   
    var discheaderlst = response.discheaderlst
    var disclst = response.disclst
    
    var dynamicheaders = [];
    for (var i = 0; i < discheaderlst.length; i++) 
    {
        dynamicheaders.push({
            "sTitle": discheaderlst[i],
        });
    };
    
    var tables = $('table.dynamictabledisc');
    for(var i=0; i<tables.length; i++)
    {
        var table = tables.eq(i);
        var tableid = rootid + 'table' + i
        table.attr('id',tableid);
    }
        
    $('table.dynamictabledisc').each(function() 
    {
      
        var datatableid = '#' + $(this).attr('id');
        
        if ($.fn.dataTable.isDataTable(datatableid)) 
        {
            $(datatableid).DataTable().destroy();
            $(datatableid).empty();
        }
    
        var table = $(datatableid).DataTable({
            data: disclst,
    
            "aoColumns": dynamicheaders,
            
            "bDestroy": true,
            orderCellsTop: true,
            pageLength: 25,
            "lengthMenu": 
            [
                [10, 25, 50, 200, -1],
                [10, 25, 50, 200, "All"]
            ],
            "createdRow": function(row, data, dataIndex, column) 
            {
                if (data[6] == 'Red') 
                {
                    return $(column[4]).addClass('table-danger')
                } 
                else if (data[6] == 'Yellow') 
                {
                    return $(column[4]).addClass('table-warning')
                } 
                else if (data[6] == 'Green') 
                {
                    return $(column[4]).addClass('table-success');
                }
            },
        });
      
        $(datatableid + ' thead tr').clone(false).appendTo(datatableid + ' thead'); //clone headers
        $(datatableid + ' thead tr:eq(1) th').each(function(i) {
            $(this).html('<input type="text" placeholder="Search" class="column_search" />');
            $(this).removeClass("sorting sorting_asc sorting_desc")
        });
    
        $(datatableid + ' thead').on('keyup', ".column_search", function() {
            table
                .column($(this).parent().index())
                .search(this.value)
                .draw();
        });
    });
}