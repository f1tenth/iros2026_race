---
short_title: Results
layout: page
section: stream
---
<center>
<h2 id="virtual-results"> LIVE STREAM </h2>

<script src="https://player.twitch.tv/js/embed/v1.js"></script>

<div id="1"></div>
<script type="text/javascript">
    var options = {
        width: 854,
        height: 480,
        channel: "roboracer_ai",
        // video: "<video ID>",
        // collection: "<collection ID>",
        parent: <!-- TWITCH_PARENTS -->["iros2026-race.roboracer.ai", "localhost"]<!-- /TWITCH_PARENTS -->
    };
    var player = new Twitch.Player("1", options);
    player.setVolume(0.5);
</script>

<!-- STREAM_PLACEHOLDER --><p style="color: #888; font-style: italic;">Live stream will appear here during the event.</p><!-- /STREAM_PLACEHOLDER -->

<h2 id="virtual-results"> RESULTS </h2>

<!-- RESULTS_PLACEHOLDER --><p style="color: #888; font-style: italic;">Results will be posted after the competition.</p><!-- /RESULTS_PLACEHOLDER -->

<!-- TIME_TRIAL_SECTION --><!-- /TIME_TRIAL_SECTION -->

<!-- BRACKET_SECTION --><!-- /BRACKET_SECTION -->

</center>
