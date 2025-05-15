// extension/background/background.js
import { postData } from './apiClient.js';

console.log('[SW] background.js loaded');
const BACKEND_BASE = 'http://localhost:8000';

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'NEW_MESSAGE') {
    const {
      conversation_id,
      message_id,
      sender_type,
      content,
      order_index
    } = message.data;

    chrome.storage.local.get('token', ({ token }) => {
      if (!token) {
        console.error('[SW] Missing token');
        sendResponse({ status: 'error', message: 'Not authenticated' });
        return;
      }

      postData(
        `${BACKEND_BASE}/messages`,
        {
          conversation_id,
          message_id,
          sender_type,
          content,
          order_index
        },
        token
      )
        .then(() => {
          console.log(
            '[SW] stored message',
            message_id,
            'in conversation',
            conversation_id
          );
          sendResponse({ status: 'ok' });
        })
        .catch(err => {
          // ignore duplicates (409), log others
          if (err.status === 409) {
            console.warn('[SW] duplicate ignored', message_id);
            sendResponse({ status: 'ok' });
          } else {
            console.error('[SW] Error storing message:', err);
            sendResponse({ status: 'error', message: err.message });
          }
        });
    });

    return true; // keep channel open for async sendResponse
  }

  sendResponse({ status: 'error', message: 'Unknown message type' });
});
