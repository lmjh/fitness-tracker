$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $('.collapsible').collapsible();
    $('select').formSelect();
    $('.datepicker').datepicker({format: "dd mmmm yy"});
    $('.timepicker').timepicker({defaultTime: "now"});
    $('.modal').modal();
  });