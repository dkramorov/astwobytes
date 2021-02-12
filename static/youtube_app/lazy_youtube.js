(function(){
  function hasClass(el, cls) {
    if (el.className.match('(?:^|\\s)'+cls+'(?!\\S)')) { return true; }
  }
  function addClass(el, cls) {
    if (!el.className.match('(?:^|\\s)'+cls+'(?!\\S)')) { el.className += ' '+cls; }
  }
  function delClass(el, cls) {
    el.className = el.className.replace(new RegExp('(?:^|\\s)'+cls+'(?!\\S)'),'');
  }

  function stripYouTubeEmbed() {
    var embed = document.querySelectorAll('iframe[src^="https://www.youtube.com/embed/"]'), length = embed.length, i, url, id;
    for (i = 0; i < length; ++i) {
      url = embed[i].getAttribute('src');
      id = url.substr(url.lastIndexOf('/') + 1); // get video id from youtube embed url
      embed[i].outerHTML = '<div class="youtube-wrap"><div class="youtube" data-embed="'+id+'"><div class="youtube-play"><\/div><\/div><\/div>';
    }
  }
  stripYouTubeEmbed();

  function LazyLoadYouTubeEmbed() {
    var yt = document.querySelectorAll('.yt-load:not(.yt-loaded)'),
        length = yt.length,
        i;
    for (i = 0; i < length; ++i) {
    var src = 'https://img.youtube.com/vi/'+ yt[i].dataset.embed +'/sddefault.jpg',
    img = new Image();
    img.src = src;
    img.addEventListener('load', function() {
      yt[i].appendChild(img);
    }(i));
    yt[i].addEventListener('click', function() {
      var iframe = document.createElement('iframe');
      iframe.setAttribute('frameborder', '0');
      iframe.setAttribute('allowfullscreen', '');
      iframe.setAttribute('src', 'https://www.youtube.com/embed/'+this.dataset.embed+'?rel=0&showinfo=0&autoplay=1');
      this.innerHTML = '';
      this.appendChild(iframe);
    });
    addClass(yt[i], 'yt-loaded');
    }
  }

  function elementFromTop(elemTrigger, elemTarget, classToAdd, distanceFromTop, unit) {
    var winY = window.innerHeight || document.documentElement.clientHeight,
        elTriggerLength = elemTrigger.length,
        elTargetLength, distTop, distPercent,
        distPixels, distUnit, elTarget, i, j;
    for (i = 0; i < elTriggerLength; ++i) {
      elTarget = document.querySelectorAll('.'+elemTarget);
      elTargetLength = elTarget.length;
      distTop = elemTrigger[i].getBoundingClientRect().top;
      distPercent = Math.round((distTop / winY) * 100);
      distPixels = Math.round(distTop);
      distUnit = unit == 'percent' ? distPercent : distPixels;
      if (distUnit <= distanceFromTop) {
        if (!hasClass(elemTrigger[i], elemTarget)) {
          for (j = 0; j < elTargetLength; ++j) {
            if (!hasClass(elTarget[j], classToAdd)) { addClass(elTarget[j], classToAdd); }
          }
        } else {
          if (!hasClass(elemTrigger[i], classToAdd)) { addClass(elemTrigger[i], classToAdd); }
        }
      } else {
        delClass(elemTrigger[i], classToAdd);
        if (!hasClass(elemTrigger[i], elemTarget)) {
          for (j = 0; j < elTargetLength; ++j) { delClass(elTarget[j], classToAdd); }
        }
      }
    }
  }
  window.addEventListener('scroll', function() {
    elementFromTop(document.querySelectorAll('.youtube'), 'youtube', 'yt-load', 150, 'percent'); // half a screen below the fold
    LazyLoadYouTubeEmbed();
  }, false);

  window.addEventListener('resize', function() {
    elementFromTop(document.querySelectorAll('.youtube'), 'youtube', 'yt-load', 150, 'percent'); // half a screen below the fold
    LazyLoadYouTubeEmbed();
  }, false);

  window.addEventListener('load', function() {
    elementFromTop(document.querySelectorAll('.youtube'), 'youtube', 'yt-load', 150, 'percent'); // half a screen below the fold
    LazyLoadYouTubeEmbed();
  }, false);
})();