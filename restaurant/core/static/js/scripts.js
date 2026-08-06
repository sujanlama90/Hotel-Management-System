
   // Add this to your JavaScript
$(document).ready(function() {
    // Fix navbar toggle on mobile
    $('.navbar-toggler').on('click', function() {
        $(this).toggleClass('collapsed');
    });
    
    // Close mobile menu when clicking a link
    $('.navbar-nav .nav-link').on('click', function() {
        $('.navbar-collapse').collapse('hide');
    });
    
    // Smooth scroll offset for navbar
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();
        
        var target = this.hash;
        var $target = $(target);
        
        // Offset for fixed navbar
        var offset = 80;
        
        $('html, body').stop().animate({
            'scrollTop': $target.offset().top - offset
        }, 900, 'swing');
    });
});


