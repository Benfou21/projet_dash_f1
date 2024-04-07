document.addEventListener('scroll', function() {
    var scrollPosition = window.scrollY || document.documentElement.scrollTop;
    window.dash_clientside = window.dash_clientside || {};
    window.dash_clientside.scrollPosition = scrollPosition;
});

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        update_scroll_position: function(timestamp, data) {
            return window.dash_clientside.scrollPosition || data;
        }
    }
});

window.addEventListener('scroll', () => {
    console.log(window.scrollY);
});