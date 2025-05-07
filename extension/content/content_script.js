// extension/content/content_script.js

/**
 * content_script.js
 * 
 * Injected into chat.openai.com pages.
 * Scrapes every message bubble and relays it to background.js,
 * ensuring the first message only sends after the conversation is created.
 */

console.log('[CS] content_script.js injected — scraper enabled');

let seenBubbles = 0;

// Helper to send messages to the SW, with optional callback
function send(type, data, callback) {
  chrome.runtime.sendMessage({ type, data }, resp => {
    console.log(`[CS] ${type} resp`, resp);
    if (callback) callback(resp);
  });
}

function initScraper() {
  const container = document.querySelector('main');
  if (!container) {
    return setTimeout(initScraper, 500);
  }

  const mo = new MutationObserver(() => {
    const bubbles = Array.from(container.querySelectorAll('.group'));
    if (bubbles.length <= seenBubbles) return;

    for (let i = seenBubbles; i < bubbles.length; i++) {
      const bubble = bubbles[i];
      const text   = bubble.innerText.trim();
      if (!text) continue;

      const sender = bubble.classList.contains('user') ? 'user' : 'assistant';
      console.log(`[CS] Detected bubble #${i}`, { sender, text });

      if (i === 0) {
        // FIRST bubble: create the conversation, then send the message
        send('NEW_CHAT', { title: text.substring(0, 100) }, resp => {
          if (resp.status === 'ok') {
            // now that we have a conversation, send the first message
            send('NEW_MESSAGE', {
              sender_type: sender,
              content: text,
              order_index: i
            });
          } else {
            console.error('[CS] NEW_CHAT failed, skipping first NEW_MESSAGE', resp);
          }
        });
      } else {
        // Subsequent bubbles fire immediately
        send('NEW_MESSAGE', {
          sender_type: sender,
          content: text,
          order_index: i
        });
      }
    }

    seenBubbles = bubbles.length;
  });

  mo.observe(container, { childList: true, subtree: true });
}

// Kick things off
initScraper();
