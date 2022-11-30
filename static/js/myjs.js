// $(function () {
//   var triggerTabList = [].slice.call(document.querySelectorAll('#myTab a'))
// triggerTabList.forEach(function (triggerEl) {
//   var tabTrigger = new bootstrap.Tab(triggerEl);
//
//   triggerEl.addEventListener('click', function (event) {
//     event.preventDefault();
//     tabTrigger.show();
//   });
// });
//
// });

$(document).ready(function(){
    load_data();
    function load_data(query)
    {
     $.ajax({
      url:"/ajaxlivesearch",
      method:"POST",
      data:{query:query},
      success:function(data)
      {
        $('#result').html(data);
        $("#result").append(data.htmlresponse);
      }
     });
    }
    $('#search_text').keyup(function(){
      var search = $(this).val();
      if(search != ''){
      load_data(search);
     }else{
      load_data();
     }
    });
  });
