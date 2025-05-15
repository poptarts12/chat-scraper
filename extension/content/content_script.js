/**
 * content/content_script.js
 * – Single‐file bubble logger for ChatGPT
 * – No ES modules, no bundling
 */

console.log('[CS] content_script.js injected — starting ordered logger');

// at top, compute ID from URL
function getConversationIdFromUrl() {
  return window.location.pathname
    .split('/c/')[1]
    ?.split('/')[0]
    || null;
}

let conversationId = getConversationIdFromUrl();
if (!conversationId) {
  console.error('[CS] no conversation ID in URL, aborting logger');
  throw new Error('No conversation ID');
}

// helper to notify SW & reset state
function startConversation(id) {
  console.log('[CS] new conversation detected:', id);
  // clear out anything we saw before
  seenIds.clear();
  queue.length = 0;
  processing = false;

  conversationId = id;
  // tell background to create/activate this conversation
  chrome.runtime.sendMessage({
    type: 'NEW_CHAT',
    data: { conversation_id: id, title: document.title }
  });
  // kick off logging again
  enqueueNew();
}

// watch for SPA URL changes
window.addEventListener('popstate', () => {
  const newId = getConversationIdFromUrl();
  if (newId && newId !== conversationId) {
    startConversation(newId);
  }
});
// monkey-patch pushState so we catch all in-page navigations
const _pushState = history.pushState;
history.pushState = function(...args) {
  _pushState.apply(this, args);
  window.dispatchEvent(new Event('popstate'));
};

const STOP_BTN_SEL =
  '#composer-submit-button[data-testid="stop-button"], button[aria-label="Stop streaming"]';

const seenIds    = new Set();
const queue      = [];
let   processing = false;

function getTurns() {
  return Array.from(
    document.body.querySelectorAll('article[data-testid^="conversation-turn-"]')
  );
}

function extractText(turn) {
  const copy = turn.cloneNode(true);
  copy.querySelectorAll('h5.sr-only').forEach(el => el.remove());
  const md = copy.querySelector('div.prose, div.markdown');
  if (md) return md.innerText.trim();
  copy.querySelectorAll('button, svg').forEach(el => el.remove());
  return copy.innerText.trim();
}

function getSender(turn) {
  const author = turn.querySelector('[data-message-author-role]');
  return author
    ? author.getAttribute('data-message-author-role')
    : 'assistant';
}

function waitForAssistantComplete(turn) {
  return new Promise(resolve => {
    const sel = STOP_BTN_SEL;
    if (!document.querySelector(sel)) {
      return resolve();
    }
    console.log('[CS][debug] Stop button detected — polling for its removal');
    const interval = setInterval(() => {
      if (!document.querySelector(sel)) {
        clearInterval(interval);
        clearTimeout(timeout);
        resolve();
      }
    }, 500);
    const timeout = setTimeout(() => {
      clearInterval(interval);
      resolve();
    }, 25000);
  });
}

function logTurn(turn, idx) {
  const text      = extractText(turn);
  const rawSender = getSender(turn);
  // 2) Map "assistant" → "chatbot", leave "user"
  const senderType = rawSender === 'assistant' ? 'chatbot' : 'user';
  const messageId  = turn.getAttribute('data-testid');

  console.log(`[CS] bubble #${idx} (${rawSender}):`, text);

  chrome.runtime.sendMessage({
    type: 'NEW_MESSAGE',
    data: {
      conversation_id: conversationId,
      message_id:      messageId,
      sender_type:     senderType,
      content:         text,
      order_index:     idx
    }
  });
}

function enqueueNew() {
  getTurns().forEach((turn, idx) => {
    const id = turn.getAttribute('data-testid');
    if (id && !seenIds.has(id)) {
      seenIds.add(id);
      queue.push({ turn, idx });
    }
  });
  processQueue();
}

async function processQueue() {
  if (processing) return;
  processing = true;
  while (queue.length) {
    const { turn, idx } = queue.shift();
    if (getSender(turn) === 'assistant') {
      const md = turn.querySelector('div.prose, div.markdown');
      if (md) {
        const obs = new MutationObserver(() => logTurn(turn, idx));
        obs.observe(md, { childList: true, subtree: true, characterData: true });
        await waitForAssistantComplete(turn);
        obs.disconnect();
      } else {
        await waitForAssistantComplete(turn);
      }
    }
    logTurn(turn, idx);
  }
  processing = false;
}

function observeNew() {
  new MutationObserver(enqueueNew).observe(document.body, {
    childList:    true,
    subtree:      true,
    characterData:true
  });
}

// bootstrap
enqueueNew();
observeNew();
startConversation(conversationId);

