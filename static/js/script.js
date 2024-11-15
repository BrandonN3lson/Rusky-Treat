$(document).ready(function () {
    // get current url path
    const currentPath = window.location.pathname;
    const links = document.querySelectorAll('nav a');
    
    links.forEach(link => {
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