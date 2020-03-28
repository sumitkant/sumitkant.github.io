// $(document).ready(function () {
//
//     $(".filter-button").click(function () {
//         var value = $(this).attr('data-filter');
//
//         if (value == "all") {
//             //$('.filter').removeClass('hidden');
//             $('.filter').show('1000');
//         } else {
//             //            $('.filter[filter-item="'+value+'"]').removeClass('hidden');
//             //            $(".filter").not('.filter[filter-item="'+value+'"]').addClass('hidden');
//             $(".filter").not('.' + value).hide('3000');
//             $('.filter').filter('.' + value).show('3000');
//
//         }
//     });
//
//     if ($(".filter-button").removeClass("active")) {
//         $(this).removeClass("active");
//     }
//     $(this).addClass("active");
//
// });

 $(document).ready(function () {
 
     // Button on click
     $('.btn').click(function () {
 
         // remove all button class
         $('.btn').each(function () {
             $(this).removeClass('active')
         });
 
         // add active class to active button
         $(this).addClass('active')
 
         // adding and removing classes based on buttons
         var getClass = $(this).attr('data');
 
         $('.entry-thumb').each(function () {
             parentEl = $(this).parent()
 
             if (getClass == 'all')
                 parentEl.removeClass('hide')
             else {
                 if ($(this).hasClass(getClass)) {
                     parentEl.removeClass('hide')
                     console.log(parentEl)
                 } else
                     parentEl.addClass('hide')
             }
 
         }); 
 
     }); //$('.btn').click(function () {
      
 });
