/* Based on the following code:
 * -------------------------------------------------------------------------------
 * Author: 
 * 	Andreas Gysin
 * 	@andreasgysin
 * 	
 * Project page:
 * 	http://ertdfgcvb.com/sequencer
 * 	http://github.com/ertdfgcvb/Sequencer	
 * 	
 * -------------------------------------------------------------------------------
 * Copyright (c) 2011-2012 Andreas Gysin
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published 
 * by the Free Software Foundation, either version 3 of the License, 
 * or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty 
 * 
 * of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
 * See the GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.
 * If not, see <http://www.gnu.org/licenses/>.
 * */

var Sequencer = (function() {
    var current = -1;
    var imgList = [];
    var playInterval;
    var playDir = 1;

    // configuration defaults
    var config = {
        scaleMode: "cover",
        mouseDirection: "x",
        playMode: "mouse"
    };


    function init(subPlaylist) {
        //subPlaylist.forEach(function(image) {
        //  console.log('images/' + image);
        //});
        var playlist = [];
        playlist = subPlaylist;
        configureBody();
        for (var i = 0, len = playlist.length; i < len; i++) {
            var img = new Image();
            console.log(playlist[i])
            img.src = playlist[i];
            //http://stackoverflow.com/questions/18936853/read-images-in-loop-wait-for-their-load
            img.onload = (function(i) {
                return function() {
                    if (i == 0) {
                        canvas.width = this.width;
                        canvas.height = this.height;
                    }
                    imgList[i] = this;
                }
            })(i);
        }


        current = 0;
        setPlayMode(config.playMode);
        play();
    }

    function setPlayMode(mode) {
        stop();
        config.playMode = mode;
    }

    function play() {
        stop();
        if (config.playMode == "mouse") {
            document.addEventListener('mousemove', onMouseMove, false);
            document.ontouchmove = function(e) {
                onMouseMove(e.touches[0]);
                return false;
            }
        }
    }

    function stop() {
        document.removeEventListener('mousemove', onMouseMove);
        if (playInterval) {
            clearInterval(playInterval);
            playInterval == null;
        }
    }

    function nextImage(mode) {
        if (!mode) mode = config.playMode;
        showImage(++current % imgList.length); //loop
    }


    function onMouseMove(e) {
        var t = imgList.length;
        var m, w;
        if (config.mouseDirection == "x") {
            w = window.innerWidth;
            m = e.pageX;
        } else if (config.mouseDirection == "-x") {
            w = window.innerWidth;
            m = w - e.pageX - 1;
        } else if (config.mouseDirection == "y") {
            w = window.innerHeight;
            m = e.pageY;
        } else if (config.mouseDirection == "-y") {
            w = window.innerHeight;
            m = w - e.pageY - 1;
        }

        var id = Math.min(t, Math.max(0, Math.floor(m / w * t)));
        if (id != current) {
            showImage(id);
            current = id;
        }
    }

    function configureBody() {
        canvas = document.createElement('canvas');
        canvas.style.position = "fixed";
        context = canvas.getContext('2d');
        document.body.appendChild(canvas);
        document.body.style.height = "100%";
    }

    function onWindowResize() {
        var ca = window.innerWidth / window.innerHeight;
        var ia = canvas.width / canvas.height;
        var iw, ih;

        if (config.scaleMode == "cover") {
            if (ca > ia) {
                iw = window.innerWidth;
                ih = iw / ia;

            } else {
                ih = window.innerHeight;
                iw = ih * ia;
            }
        } else if (config.scaleMode == "contain") {
            if (ca < ia) {
                iw = window.innerWidth;
                ih = iw / ia;
            } else {
                ih = window.innerHeight;
                iw = ih * ia;
            }
        } else if (config.scaleMode == "auto") {
            iw = canvas.width;
            ih = canvas.height;
        }

        var ox = window.innerWidth / 2 - iw / 2;
        var oy = window.innerHeight / 2 - ih / 2;

        canvas.style.width = Math.round(iw) + "px";
        canvas.style.height = Math.round(ih) + "px";
        canvas.style.left = Math.round(ox) + "px";
        canvas.style.top = Math.round(oy) + "px";
    }


    function showImage(id) {
        if (id >= 0 && id < imgList.length) {
            context.drawImage(imgList[id], 0, 0);
        }
    }

    return {
        init: init,
        nextImage: nextImage,
        setPlayMode: setPlayMode,
        play: play,
        stop: stop
    };
})();
