// ScoutAI capture bookmarklet
// Captures the current page's text, URL, and title, and POSTs it to the
// ScoutAI /capture endpoint so it gets saved to Notion.

(async function () {
  try {
    // Grab the page content we want to send.
    const text = document.body.innerText; // full page text, no truncation
    const url = window.location.href;
    const title = document.title; // may be empty — that's fine, /capture defaults it

    // POST to the ScoutAI capture endpoint.
    // This is a cross-origin request (e.g. linkedin.com -> railway.app),
    // but the server already has CORS enabled for all origins.
    const res = await fetch(
      "https://scoutai-production-6ccf.up.railway.app/capture",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, url, title }),
      }
    );

    const data = await res.json();

    if (data.success === true) {
      alert("✅ Saved: " + data.message);
    } else {
      alert("❌ Failed: " + data.error);
    }
  } catch (err) {
    // Covers network errors, server down, etc. Never let this break the host page.
    alert("❌ Could not reach ScoutAI server");
  }
})();

// === BOOKMARKLET (paste this as bookmark URL) ===
// javascript:(async function(){try{const text=document.body.innerText;const url=window.location.href;const title=document.title;const res=await fetch("https://scoutai-production-6ccf.up.railway.app/capture",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text,url,title})});const data=await res.json();if(data.success===true){alert("✅ Saved: "+data.message);}else{alert("❌ Failed: "+data.error);}}catch(err){alert("❌ Could not reach ScoutAI server");}})();
