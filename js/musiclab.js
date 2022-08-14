var reqURL = "https://api.rss2json.com/v1/api.json?rss_url=" + encodeURIComponent("https://www.youtube.com/feeds/videos.xml?channel_id=");

function loadVideo(iframe) {
  $.getJSON(reqURL + iframe.getAttribute('cid'),
    function(data) {
      var videoNumber = (iframe.getAttribute('vnum') ? Number(iframe.getAttribute('vnum')) : 0);
      console.log(videoNumber);
      var link = data.items[videoNumber].link;
      var title=data.items[videoNumber].title;
      var thumbImg = data.items[videoNumber].thumbnail;
      id = link.substr(link.indexOf("=") + 1);
      console.log(data)
      iframe.setAttribute("src", "https://youtube.com/embed/" + id + "?controls=0&autoplay=1");
      iframe.parentElement.querySelector("#video-title").innerText = title;

      iframe.parentElement.querySelector("#video-link").firstChild.setAttribute("src", thumbImg)
      iframe.parentElement.querySelector("#video-link").setAttribute("href", link)
    }
  );
}

var iframes = document.getElementsByClassName('latestVideoEmbed');
for (var i = 0, len = iframes.length; i < len; i++) {
  loadVideo(iframes[i]);
}
