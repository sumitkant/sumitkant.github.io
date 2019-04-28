/**
 * demo1.js
 * http://www.codrops.com
 *
 * Licensed under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 * 
 * Copyright 2019, Codrops
 * http://www.codrops.com
 */
{
    class Revealer {
        constructor(el, options) {
            this.options = {
                angle: 0
            };
            Object.assign(this.options, options);

            this.DOM = {};
            this.DOM.el = el;
            this.DOM.inner = this.DOM.el.firstElementChild;

            // this.DOM.inner.style.width = `calc(100vw * ${Math.abs(Math.cos(this.options.angle * Math.PI/180))} + 100vh * ${Math.abs(Math.sin(this.options.angle * Math.PI/180))})`;
            // this.DOM.inner.style.height = `calc(100vw * ${Math.abs(Math.sin(this.options.angle * Math.PI/180))} + 100vh * ${Math.abs(Math.cos(this.options.angle * Math.PI/180))})`;
            // this.DOM.el.style.transform = `rotate3d(0,0,1,${this.options.angle}deg)`;

            // this.DOM.reverse = this.DOM.inner.querySelector('.content__reverse');
            if (this.DOM.reverse) {
                TweenMax.set(this.DOM.reverse, {
                    rotation: -1 * this.options.angle
                });
            }
        }
    }

    // Content elements
    const content = {
        first: document.querySelector('.content--first'),
        // second: document.querySelector('.content--second')
    };

    // First page's content.
    const firstPageContent = {
        // img: content.first.querySelector('.intro__img'),
        title: content.first.querySelector('.intro__title'),
        // enter: content.first.querySelector('.intro__enter')
    };

    // Splitting letters for the firstPageContent.title element (just adding a bit more feeling to it)
    charming(firstPageContent.title);
    firstPageContent.titleLetters = [...firstPageContent.title.querySelectorAll('span')];
    firstPageContent.titleLetters.sort(() => Math.round(Math.random()) - 0.5);
    // some random letters
    let letters = firstPageContent.titleLetters.filter(_ => Math.random() < .5);
    // remaining
    let otherletters = firstPageContent.titleLetters.filter(el => letters.indexOf(el) < 0);

    // Second page's content.
    // const secondPageContent = {
    //     reel: content.second.querySelector('.reel'),
    //     backCtrl: content.second.querySelector('.content__back')
    // };

    // Revealer element
    const revealer = new Revealer(content.first, {
        angle: 35
    });

    // Animate things: show revealer animation, animate first page elements out (optional) and animate second page elements in (optional)
    // const showNextPage = () => {
    //     // Pointer events related class
    //     content.first.classList.add('content--hidden');

    //     const ease = Expo.easeInOut;
    //     const duration = 1.2;
    //     this.pageToggleTimeline = new TimelineMax()
    //     // Animate first page elements (optional)
    //     .to(firstPageContent.img, duration, {
    //         ease: ease,
    //         y: -150,
    //         scaleY: 1.1,
    //         opacity: 0
    //     }, 0)
    //     .staggerTo(otherletters, duration*0.8, {
    //         ease: ease,
    //         y: '-100%',
    //         scaleX: 0.8,
    //         scaleY: 1.5,
    //         opacity: 0
    //     }, 0.04, 0)
    //     .to(firstPageContent.enter, duration*0.5, {
    //         ease: ease,
    //         opacity: 0
    //     }, 0)

    //     // "Unreveal effect" (inner moves to one direction and reverse moves to the opposite one)
    //     .to(revealer.DOM.inner, duration, {
    //         ease: ease,
    //         y: '-100%'
    //     }, 0)
    //     .to(revealer.DOM.reverse, duration, {
    //         ease: ease,
    //         y: '100%'
    //     }, 0)

    //     // Animate second page elements (optional)
    //     .to(secondPageContent.reel, duration, {
    //         ease: ease,
    //         startAt: {y: 100},
    //         y: 0
    //     }, 0);
    // };
    // firstPageContent.enter.addEventListener('click', showNextPage);

    // Animate back
    // const showIntro = () => {
    //     // Pointer events related class
    //     content.first.classList.remove('content--hidden');
    //     this.pageToggleTimeline.reverse();
    // };
    // secondPageContent.backCtrl.addEventListener('click', showIntro);

    // Hover animation on the intro "title" element
    let enterHoverAnimationRunning = false;
    const onEnterHoverFn = () => {
        if (enterHoverAnimationRunning) {
            return false;
        }
        enterHoverAnimationRunning = true;

        letters = firstPageContent.titleLetters.filter(_ => Math.random() < .5);
        otherletters = firstPageContent.titleLetters.filter(el => letters.indexOf(el) < 0);

        new TimelineMax({
                onComplete: () => enterHoverAnimationRunning = false
            })
            .staggerTo(letters, 0.2, {
                ease: Quad.easeIn,
                y: '-100%',
                opacity: 0
            }, 0.04, 0)
            .staggerTo(letters, 0.6, {
                ease: Quint.easeOut,
                startAt: {
                    y: '35%'
                },
                y: '0%',
                opacity: 1
            }, 0.04, 0.2);
    };
    firstPageContent.title.addEventListener('mouseenter', onEnterHoverFn);


    // Typewriter Effect

    var TxtType = function (el, toRotate, period) {
        this.toRotate = toRotate;
        this.el = el;
        this.loopNum = 0;
        this.period = parseInt(period, 10) || 1000;
        this.txt = '';
        this.tick();
        this.isDeleting = false;
    };

    TxtType.prototype.tick = function () {
        var i = this.loopNum % this.toRotate.length;
        var fullTxt = this.toRotate[i];

        if (this.isDeleting) {
            this.txt = fullTxt.substring(0, this.txt.length - 1);
        } else {
            this.txt = fullTxt.substring(0, this.txt.length + 1);
        }

        this.el.innerHTML = '<span class="wrap">' + this.txt + '</span>';

        var that = this;
        var delta = 200 - Math.random() * 100;

        if (this.isDeleting) {
            delta /= 2;
        }

        if (!this.isDeleting && this.txt === fullTxt) {
            delta = this.period;
            this.isDeleting = true;
        } else if (this.isDeleting && this.txt === '') {
            this.isDeleting = false;
            this.loopNum++;
            delta = 500;
        }

        setTimeout(function () {
            that.tick();
        }, delta);
    };

    window.onload = function () {
        var elements = document.getElementsByClassName('typewrite');
        for (var i = 0; i < elements.length; i++) {
            var toRotate = elements[i].getAttribute('data-type');
            var period = elements[i].getAttribute('data-period');
            if (toRotate) {
                new TxtType(elements[i], JSON.parse(toRotate), period);
            }
        }
        // INJECT CSS
        var css = document.createElement("style");
        css.type = "text/css";
        css.innerHTML = ".typewrite > .wrap { border-right: 0.08em solid #fff}";
        document.body.appendChild(css);
    };

}
