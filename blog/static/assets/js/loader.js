$(document).ready(function(){
    
    $('.parallax').parallax();
    $('.sidenav').sidenav();
    $(".slider").slider({fullWidth:true});
    $('.parallax').parallax();
    
  });

  $(document).ready(function(){

    $('.chips').chips();
    $('.chips-placeholder').chips({
      placeholder: 'Enter a tag',
      secondaryPlaceholder: '+Tag',
      limit: 10,
      minLength: 1,
 });
   $('textarea#description, textarea#address').characterCounter();
   $('.modal').modal();
   $('.parallax').parallax();
   $('.sidenav').sidenav();
   $(".slider").slider({fullWidth:true});
   $('.parallax').parallax();
   $('.myreviews').carousel({
     numVisible: 7,
     shift: 55,
     padding: 55
   });

 });

function toggleModal(){
 var instance =M.Modal.getInstance($('#modal3'));
 instance.open();
}







/*Profile pic upload*/

$(document).ready(function() {

   
   var readURL = function(input) 
   {
       if (input.files && input.files[0]) 
       {
           var reader = new FileReader();

           reader.onload = function (e) 
           {
               $('.profile-pic').attr('src', e.target.result);
           }
   
           reader.readAsDataURL(input.files[0]);
       }
   }
   

   $(".file-upload").on('change', function()
   {
       readURL(this);
   });
   
   $(".upload-button").on('click', function() 
   {
      $(".file-upload").click();
   });

});



/*cover pic upload*/


$(document).ready(function() {

   
   var readURL = function(input) 
   {
       if (input.files && input.files[0]) 
       {
           var reader = new FileReader();

           reader.onload = function (e) 
           {
               $('.profile-pic').attr('src', e.target.result);
           }
   
           reader.readAsDataURL(input.files[0]);
       }
   }

   $(".file-upload").on('change', function()
   {
       readURL(this);
   });
   
   $(".upload-button").on('click', function() 
   {
      $(".file-upload").click();
   });


var readcpicURL = function(input) 
   {
       if (input.files && input.files[0]) 
       {
           var reader = new FileReader();

           reader.onload = function (e) 
           {
               $('.cover-pic').attr('src', e.target.result);
           }
   
           reader.readAsDataURL(input.files[0]);
       }
   }
   

   $(".file-cpic-upload").on('change', function()
   {
       readcpicURL(this);
   });
   
   $(".upload-cpic-button").on('click', function() 
   {
      $(".file-cpic-upload").click();
   });


});