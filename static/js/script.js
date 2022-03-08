$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $('.collapsible').collapsible();
    $('select').formSelect();
    $('.datepicker').datepicker({format: "dd/mm/yy"});
    $('.timepicker').timepicker({twelveHour: false});
    $('.modal').modal();
  });