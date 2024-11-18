$(document).ready(function () {
    // get current url path
    const currentPath = window.location.pathname;
    const links = document.querySelectorAll('nav a');
    
    links.forEach(link => {
        // adds active class to a tag in nav items, highlights current page.
        if ($(link).attr('href') === currentPath) {
            $(link).addClass('active');
        } else {
            $(link).removeClass('active')
        }
    })


    $(links).click(function () {
        $(links).removeClass('active');
        $(this).addClass('active');
    })
})