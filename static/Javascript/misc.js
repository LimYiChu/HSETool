// $(document).ready(function()

// {
//   $(".btn").click(function()
//   {
//     $.ajax({

//       url: "../loadajax3",
//       type : 'get',
//       data : {
//         button_text: $(this).text()
//       },
//       success: function (response){
//         $(".btn").text(response.context) 
//         // alert(response.context)  
//       }


//     })
//     })

// })

function phasesurl (id,phase)

{
    
    if (phase == '') {

        document.location.href = "../reppmt"

    }else{
        document.location.href = phase // adds the phase part to the end of the reppmt- it is then caught by views
        
}}

function closeoutphasesurl (id,phase)

{
    
    if (phase == '') {

        document.location.href = "../closeoutsheet"

    }else{
        document.location.href = phase // adds the phase part to the end of the reppmt- it is then caught by views
        
}}

function maketabactive (id){
    ///make the tab (button active)
    if (id===""){

        id="allphases"
    }
    var gettab = document.getElementById(id)
    gettab.className += " active"

}

function makecloseouttabactive (id){
    ///make the tab (button active)
    if (id===""){

        id="allcloseoutphases"
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
