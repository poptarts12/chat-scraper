// extension/content/content_script.js

/**
 * content_script.js
 *
 * Injected into chat.openai.com pages.
 * Scrapes every message bubble and relays it to background.js.
 */

console.log('[CS] content_script.js injected — scraper enabled');

let seenBubbles = 0;

// Helper to send messages to the Service Worker
function send(type, data) {
  chrome.runtime.sendMessage({ type, data }, resp => {
    console.log(`[CS] ${type} resp`, resp);
  });
}

// Observe for new message bubbles
function initScraper() {
  const container = document.querySelector('main');
  if (!container) {
    // Retry until the <main> is available
    return setTimeout(initScraper, 500);
  }

  const mo = new MutationObserver(() => {
    const bubbles = Array.from(container.querySelectorAll('.group'));
    if (bubbles.length <= seenBubbles) return;

    for (let i = seenBubbles; i < bubbles.length; i++) {
      const bubble = bubbles[i];
      const text = bubble.innerText.trim();
      if (!text) continue;

      const sender = bubble.classList.contains('user') ? 'user' : 'assistant';
      console.log(`[CS] Detected bubble #${i}`, { sender, text });

      // First bubble → start a new conversation (SW will pull user_id/token)
      if (i === 0) {
        send('NEW_CHAT', {
          title: text.substring(0, 100)
        });
      }

      // Every bubble → append as a message
      send('NEW_MESSAGE', {
        sender_type: sender,
        content: text,
        order_index: i
      });
    }

    seenBubbles = bubbles.length;
  });

  mo.observe(container, { childList: true, subtree: true });
}

// Kick things off
initScraper();
