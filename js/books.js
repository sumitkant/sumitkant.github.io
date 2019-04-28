
(function() {

    var overlay = document.getElementById( 'book-overlay' ),
        overlayClose = overlay.querySelector( 'button' ),
        header = document.getElementById( 'book-header' )
        switchBtnn = header.querySelector( 'button.slider-switch' ),
        toggleBtnn = function() {
            if( slideshow.isFullscreen ) {
                classie.add( switchBtnn, 'view-maxi' );
            }
            else {
                classie.remove( switchBtnn, 'view-maxi' );
            }
        },
        toggleCtrls = function() {
            if( !slideshow.isContent ) {
                classie.add( header, 'hide' );
            }
        },
        toggleCompleteCtrls = function() {
            if( !slideshow.isContent ) {
                classie.remove( header, 'hide' );
            }
        },
        slideshow = new DragSlideshow( document.getElementById( 'slideshow' ), { 
            // toggle between fullscreen and minimized slideshow
            onToggle : toggleBtnn,
            // toggle the main image and the content view
            onToggleContent : toggleCtrls,
            // toggle the main image and the content view (triggered after the animation ends)
            onToggleContentComplete : toggleCompleteCtrls
        }),
        toggleSlideshow = function() {
            slideshow.toggle();
            toggleBtnn();
        },
        closeOverlay = function() {
            classie.add( overlay, 'hide' );
        };

    // toggle between fullscreen and small slideshow
    switchBtnn.addEventListener( 'click', toggleSlideshow );
    // close overlay
    overlayClose.addEventListener( 'click', closeOverlay );

}());
