function initiateGoogleChart(){
  google.charts.load('current', {'packages':['corechart']}); //edward 20210728 new chart
  //google.charts.load('current', {'packages':['line']});
  google.charts.setOnLoadCallback(starter);

}
function starter(){
    
        drawChart({{rundowncontent|safe}} );
           }

function drawChart(values) {

  var chartdata = [];
  var data = new google.visualization.DataTable();
  data.addColumn('date', 'Date');
  data.addColumn('number', 'Planned');
  data.addColumn('number', 'Actual');

  var arrplot =[]
  for(var i = 0; i < values.length; i++){
  //for(var j = 0; j < values[i].length; j++){
      
        first = (values[0][0]);
        seconddate=(values[1][0]);
        datess= (values[i][0]);
        actual = (values[i][1]);
        planned =(values[i][2]);
        
        stringdatas = '[new Date(\'' + datess + '\'),'+ actual + ','+ planned + ']';
        
        arrplot.push(stringdatas)
      
  //}
}
//stringdata = '[new Date(\'' + first + '\'),200,210]';
  var datarows = [];
  for (var k =0;k<arrplot.length;k++)

{

    data.addRow(eval(arrplot[k]));

}
;

  var options = {
    interpolateNulls: true,//edward 20210728 new chart 
    chart: {
      title: 'Run-Down Curve',
      subtitle: 'Action Items',
    
  },
    colors: ['blue', 'red'],
    //hAxis:{ format: 'MMM d,y'}, //edward 20210728 new chart
    hAxis:{ format: 'd MMMM',}, //edward 20210728 new chart
    pointSize: 5,
    vAxis: {title: "Number of Actions",titleTextStyle: {
      fontName: 'Helvetica',
      
        fontSize: 20,
        bold:true,
        }},//edward 20210728 new chart
    //curveType: 'function', //edward 20210728 new chart
    //legend: {position: 'left', textStyle: { fontSize: 16}}, //edward 20210728 new chart
    legend: {position: 'top', textStyle: {color: 'red', fontSize: 16}},//edward 20210728 new chart
    width: 1200,//edward 20210728 new chart changed the width to keep it in
    height: 500
};

    //var chart = new google.charts.Line(document.getElementById('linecharted')); //edward 20210728 new chart
    var chart = new google.visualization.LineChart(document.getElementById('linecharted'));//edward 20210728 new chart
    chart.draw(data,options);//edward 20210728

//chart.draw(data, google.charts.Line.convertOptions(options));
//edward 20210730 commit
}
     
        //google.charts.load('current', {'packages':['line']});
        //google.charts.setOnLoadCallback(starter); //cant call drawchart with paarmeters, need the parameters to make the code effcient
        function initiateGooPieChart(){
         
            //testjson()
            google.charts.load('current', {'packages':['corechart']});
            google.charts.setOnLoadCallback(starterPie);
            //google.charts.setOnLoadCallback(starterjsonPie()) 
            
          }
  
          
          function starterPie ()
          {
            {% for chart in forpie%}
            {%if chart %}
              
                      drawPieChart({{chart|safe}} ,  {{ forloop.counter }},'{{chart.0}}');
              {%endif%}
            {%endfor%}
                
          }
  
          function drawPieChart(values,index,chartTitle) 
          {
            
            
            firstindex = chartTitle.lastIndexOf("///")+3
            
            lastindex = chartTitle.lastIndexOf(":::")
            var newtitle = chartTitle.substring(firstindex,lastindex );
            
            
  
            var data = google.visualization.arrayToDataTable(values);
  
            
    
            var options = {
              title: newtitle,
              is3D : true,
              
              pieSliceText : 'value',
              pieSliceTextStyle: {
                bold: true,
                fontSize: 25,
                color: 'black'
            },
              titleTextStyle: {
                color: 'Black',    // any HTML string color ('red', '#cc00cc')
                fontName: 'Helvetica', // i.e. 'Times New Roman'
                fontSize: 25, // 12, 18 whatever you want (don't specify px)
                bold: true,    // true or false
                italic: false   // true of false
                            },
                height: 500,
                width: 900,
                
                chartArea:{left:20,top:100,width:'100%',height:'100%'},
                legend : {position: 'labeled', textStyle: {color: 'black', fontSize: 20}} //have to add this in otherwise charts seem small...like your dick
            };
            
           
            //var strpie = "piechart";
            //var finalpie = strpie.concat(index);
          
          var strpie = "piechart";
          var finalpie = strpie.concat(index);
        
          var chart = new google.visualization.PieChart(document.getElementById(finalpie));
          chart.draw(data, options);
  
            //var chart = new google.visualization.PieChart(document.getElementById('piechart'));
            //chart.draw(data, options);
            }
    