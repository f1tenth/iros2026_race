/* Event gallery: looping video previews and a small lightbox with a
   full-quality download button. No dependencies. */
(function () {
	'use strict';

	var items = Array.prototype.slice.call(document.querySelectorAll('.rr-gallery-open'));
	if (!items.length) return;

	/* ---- Video previews: play only while on screen, never for reduced motion ---- */
	var previews = Array.prototype.slice.call(document.querySelectorAll('.rr-gallery-item video'));
	var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

	function playQuietly(video) {
		var attempt = video.play();
		if (attempt && attempt.catch) attempt.catch(function () { /* autoplay blocked: poster stays */ });
	}

	if (reduceMotion) {
		previews.forEach(function (v) { v.removeAttribute('autoplay'); v.pause(); });
	} else if ('IntersectionObserver' in window) {
		var observer = new IntersectionObserver(function (entries) {
			entries.forEach(function (entry) {
				if (entry.isIntersecting) playQuietly(entry.target); else entry.target.pause();
			});
		}, { threshold: 0.25 });
		previews.forEach(function (v) { observer.observe(v); });
	}

	/* ---- Lightbox ---- */
	var lb = document.createElement('div');
	lb.className = 'rr-lb';
	lb.hidden = true;
	lb.setAttribute('role', 'dialog');
	lb.setAttribute('aria-modal', 'true');
	lb.setAttribute('aria-label', 'Photo and video viewer');
	lb.innerHTML =
		'<div class="rr-lb-bar">' +
			'<span class="rr-lb-count"></span>' +
			'<span class="rr-lb-name"></span>' +
			'<a class="rr-lb-download icon solid fa-download" download>Download</a>' +
			'<button type="button" class="rr-lb-btn rr-lb-close" aria-label="Close">&times;</button>' +
		'</div>' +
		'<div class="rr-lb-stage">' +
			'<button type="button" class="rr-lb-btn rr-lb-nav rr-lb-prev" aria-label="Previous">&#8249;</button>' +
			'<div class="rr-lb-media"></div>' +
			'<button type="button" class="rr-lb-btn rr-lb-nav rr-lb-next" aria-label="Next">&#8250;</button>' +
		'</div>';
	document.body.appendChild(lb);

	var media = lb.querySelector('.rr-lb-media');
	var count = lb.querySelector('.rr-lb-count');
	var name = lb.querySelector('.rr-lb-name');
	var download = lb.querySelector('.rr-lb-download');
	var closeBtn = lb.querySelector('.rr-lb-close');
	var stage = lb.querySelector('.rr-lb-stage');
	var current = -1;
	var lastFocus = null;

	function show(index) {
		current = (index + items.length) % items.length;
		var link = items[current];
		var data = link.dataset;

		media.innerHTML = '';
		var el;
		if (data.type === 'video') {
			el = document.createElement('video');
			el.controls = true;
			el.autoplay = true;
			el.playsInline = true;
			el.preload = 'metadata';
			if (data.poster) el.poster = data.poster;
			el.src = data.full;
		} else {
			el = document.createElement('img');
			el.alt = data.alt || '';
			el.src = data.full;
		}
		media.appendChild(el);

		count.textContent = (current + 1) + ' / ' + items.length;
		name.textContent = data.name || '';
		download.href = data.download;
		download.setAttribute('download', data.name || '');
		download.textContent = 'Download' + (data.size ? ' (' + data.size + ')' : '');
		download.title = 'Download the original file, full quality';

		/* Warm the next photo so arrow navigation feels instant. */
		var next = items[(current + 1) % items.length];
		if (next && next.dataset.type !== 'video') { new Image().src = next.dataset.full; }
	}

	function open(index) {
		lastFocus = document.activeElement;
		previews.forEach(function (v) { v.pause(); });
		lb.hidden = false;
		document.body.classList.add('rr-lb-open');
		show(index);
		closeBtn.focus();
	}

	function close() {
		if (lb.hidden) return;
		media.innerHTML = '';   /* also stops a playing video */
		lb.hidden = true;
		document.body.classList.remove('rr-lb-open');
		if (!reduceMotion) {
			previews.forEach(function (v) {
				var r = v.getBoundingClientRect();
				if (r.bottom > 0 && r.top < window.innerHeight) playQuietly(v);
			});
		}
		if (lastFocus && lastFocus.focus) lastFocus.focus();
	}

	items.forEach(function (link, index) {
		link.addEventListener('click', function (event) {
			/* Let ctrl/cmd/middle-click open the file in a new tab as usual. */
			if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button) return;
			event.preventDefault();
			open(index);
		});
	});

	closeBtn.addEventListener('click', close);
	lb.querySelector('.rr-lb-prev').addEventListener('click', function () { show(current - 1); });
	lb.querySelector('.rr-lb-next').addEventListener('click', function () { show(current + 1); });

	/* Click on the dark backdrop (not the media or a control) closes. */
	stage.addEventListener('click', function (event) {
		if (event.target === stage || event.target === media) close();
	});

	document.addEventListener('keydown', function (event) {
		if (lb.hidden) return;
		if (event.key === 'Escape') { close(); }
		else if (event.key === 'ArrowLeft') { show(current - 1); }
		else if (event.key === 'ArrowRight') { show(current + 1); }
		else if (event.key === 'Tab') {
			/* Keep keyboard focus inside the dialog. */
			var focusable = lb.querySelectorAll('a[href], button, video[controls]');
			var first = focusable[0], last = focusable[focusable.length - 1];
			if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
			else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
		}
	});

	/* Swipe left / right on touch screens. */
	var touchX = null;
	stage.addEventListener('touchstart', function (event) {
		touchX = event.touches.length === 1 ? event.touches[0].clientX : null;
	}, { passive: true });
	stage.addEventListener('touchend', function (event) {
		if (touchX === null) return;
		var dx = event.changedTouches[0].clientX - touchX;
		touchX = null;
		if (event.target.tagName === 'VIDEO') return;   /* leave the scrubber alone */
		if (Math.abs(dx) > 50) show(current + (dx < 0 ? 1 : -1));
	}, { passive: true });
})();
