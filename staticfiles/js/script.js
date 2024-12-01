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

    // //change colors of order status
    // $('.order-status').each(function() {
    //     let status = $(this).find('strong').text().trim();
    //     console.log("Status: ", status)
    //     switch(status) {
    //         case "Pending":
    //             $(this).addClass('pending');
    //             break;
    //         case "Processing":
    //             $(this).addClass('processing');
    //             break;
    //         case "Delivered":
    //             $(this).addClass('delivered');
    //             break;
    //         case "Cancelled":
    //             $(this).addClass('cancelled');
    //             break;
    //         default:
    //             break;
    //     }
    // });
    

    // initiate toast
    var toastElList = [].slice.call(document.querySelectorAll('.toast'))
        var toastList = toastElList.map(function (toastEl) {
            return new bootstrap.Toast(toastEl, option)
            })
})