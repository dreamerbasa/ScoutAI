// ScoutAI capture bookmarklet
// LinkedIn's CSP blocks fetch() to external domains, so instead of POSTing
// directly, this opens a small relay popup served by the ScoutAI backend
// (same-origin as /capture) and hands it the page data via postMessage.
// The relay page does the actual fetch() to /capture.

(function () {
  try {
    // Grab the page content we want to send.
    const text = document.body.innerText; // full page text, no truncation
    const url = window.location.href;
    const title = document.title; // may be empty — that's fine, /capture defaults it

    // Open the relay popup on the ScoutAI backend's own origin.
    // window.open() is not blocked by LinkedIn's fetch-blocking CSP.
    const popup = window.open(
      "https://scoutai-production-6ccf.up.railway.app/relay",
      "scoutai_capture",
      "width=420,height=320,top=100,left=" + (screen.width - 500)
    );

    // Give the popup a moment to load before messaging it.
    setTimeout(() => {
      popup.postMessage(
        { text, url, title },
        "https://scoutai-production-6ccf.up.railway.app"
      );
    }, 1000);
  } catch (err) {
    alert("❌ Could not open ScoutAI capture window");
  }
})();

// === BOOKMARKLET (paste this as bookmark URL) ===
// javascript:(function(){try{const text=document.body.innerText;const url=window.location.href;const title=document.title;const popup=window.open("https://scoutai-production-6ccf.up.railway.app/relay","scoutai_capture","width=420,height=320,top=100,left="+(screen.width-500));setTimeout(()=>{popup.postMessage({text,url,title},"https://scoutai-production-6ccf.up.railway.app");},1000);}catch(err){alert("❌ Could not open ScoutAI capture window");}})();
