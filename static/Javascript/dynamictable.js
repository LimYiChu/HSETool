function launchtable(that, event, tablepopup) {
  fadein(that);
  ajaxcall(event, tablepopup);
}

function fadein(that) {
  var $x = $($(that).closest('div .divclick'));
  var $y = $($(that).closest('div .divclick').siblings('.popup'));
  $x.css("animaton", "mymoveout .5s ease");
  $y.css("animation", "slide-in .5s ease");
  $y.css("display", "block");
}

function ajaxcall(event, tablepopup) {
  var data = event.currentTarget.firstElementChild.innerText
  var title = event.currentTarget.firstElementChild.innerText
  $('.caption').html(title);

  $.ajax({
      url: "/" + tablepopup,
      type: 'GET',
      data: {
          "data": data
      },
      rootid: tablepopup,

      success: function(response) {
          dynamictable(response, this.rootid);
          dynamicchart(response, this.rootid);
      }
  })
}

function dynamictable(response,rootid) {

  var dflist = response.dflist
  var headerlist = response.headerlist
  var dynamicheaders = [];
  for (var i = 0; i < headerlist.length; i++) 
  {
      dynamicheaders.push({
          "sTitle": headerlist[i],
      });
  };

    var tables = $('table.dynamictable');
    for(var i=0; i<tables.length; i++){
        var table = tables.eq(i);
        var tableid = rootid + 'table' + i
        table.attr('id',tableid);
    }
  
  $('table.dynamictable').each(function() {

    var datatableid = '#' + $(this).attr('id');
    
      if ($.fn.dataTable.isDataTable(datatableid)) 
      {
          $(datatableid).DataTable().destroy();
          $(datatableid).empty();
      }

      var table = $(datatableid).DataTable({
          data: dflist,

          "aoColumns": dynamicheaders,
          "columnDefs": 
          [{
              "targets": [0],
              "mRender": function(data, row, column) {
                  return '<a href="/pmtrepviewall' + '/' + column[5] + '/view' + '">' + data + '</a>';
              }
          }, ],
          "bDestroy": true,
          orderCellsTop: true,
          "lengthMenu": 
          [
              [-1, 10, 25, 50, 200],
              ["All", 10, 25, 50, 200]
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

          if ($y.css('display') !== 'none') 
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
    
    var data = google.visualization.arrayToDataTable(
        value
    );
    var options = {
        width: 370,
        height: 220,
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
            bottom: 50,
            width: '100%',
            height: '80%'
        },

        legend: 
        {
            position: 'labeled',
            textStyle: {
                color: 'black',
                fontSize: 15
            }
        }
    };

    // var chartid = rootid + 'chart'
    // $('div.dynamicchart').attr('id',chartid)

    // var charts = $('div.dynamicchart');
    // for(var i=0; i<charts.length; i++){
    //     var chart = charts.eq(i);
    //     var chartid = rootid + 'chart' + index
    //     $("<div/>").attr('id',chartid).appendTo(chart);
    // }

    // var $div = $('.dynamicchart')
    // id = chartid + index
    // $("<div/>").attr('id',chartid).appendTo($div);

    // var $div2 = $('.dynamicchart2')
    // index2 = parseInt(index) + 2
    // id2 = 'chart'+ index2
    // $("<div/>").attr('id',id2).appendTo($div2);
   
    // var finalpie = chartid.concat(index);
    // var chart = new google.visualization.PieChart(document.getElementById(finalpie));
    // chart.draw(data, options);
    var chart = new google.visualization.PieChart(singlediv);
    chart.draw(data, options);chart.draw(data, options);
    // var chart2 = new google.visualization.PieChart(document.getElementById(id2));
    // chart2.draw(data, options);
}