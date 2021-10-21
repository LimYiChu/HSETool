function phasesurl (phase)

{
    if (phase == '') {

        document.location.href = "../reppmt"

    }else{
        document.location.href = phase // adds the phase part to the end of the reppmt- it is then caught by views
        
}
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