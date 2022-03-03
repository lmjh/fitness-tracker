$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $('.collapsible').collapsible();
    $('select').formSelect();
    today = new Date();
    $('.datepicker').datepicker({format: "dd mmmm yy"});
    $('.timepicker').timepicker({defaultTime: "now"});
  });