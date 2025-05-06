// extension/background/background.js

/**
 * Service Worker for ChatGPT Saver
 * Listens for NEW_CHAT and NEW_MESSAGE messages from content scripts
 * and forwards them to your FastAPI backend via apiClient.js,
 * pulling auth info from chrome.storage.local.
 */

import { postData, putData } from './apiClient.js';

console.log('[SW] background.js loaded');

let currentConversationId = null;
const BACKEND_BASE = 'http://localhost:8000';

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'NEW_CHAT') {
    // Create a new conversation, using stored token + user_id
    chrome.storage.local.get(['token', 'user_id'], ({ token, user_id }) => {
      if (!token || !user_id) {
        console.error('[SW] Missing token or user_id');
        sendResponse({ status: 'error', message: 'Not authenticated' });
        return;
      }
      postData(
        `${BACKEND_BASE}/conversations`,
        { user_id, title: message.data.title },
        token
      )
        .then(response => {
          currentConversationId = response.conversation_id;
          console.log('[SW] created conversation', currentConversationId);
          sendResponse({ status: 'ok', conversationId: currentConversationId });
        })
        .catch(err => {
          console.error('[SW] Error creating conversation:', err);
          sendResponse({ status: 'error', message: err.message });
        });
    });
    return true;  // keep channel open for async sendResponse
  }

  if (message.type === 'NEW_MESSAGE') {
    // Append a message to the current conversation
    if (!currentConversationId) {
      sendResponse({ status: 'error', message: 'No active conversation ID' });
      return;
    }
    chrome.storage.local.get('token', ({ token }) => {
      if (!token) {
        console.error('[SW] Missing token');
        sendResponse({ status: 'error', message: 'Not authenticated' });
        return;
      }
      putData(
        `${BACKEND_BASE}/conversations/${currentConversationId}/messages`,
        {
          sender_type: message.data.sender_type,
          content: message.data.content,
          order_index: message.data.order_index
        },
        token
      )
        .then(() => {
          console.log('[SW] message added to', currentConversationId);
          sendResponse({ status: 'ok' });
        })
        .catch(err => {
          console.error('[SW] Error adding message:', err);
          sendResponse({ status: 'error', message: err.message });
        });
    });
    return true;
  }

  // Unknown message type
  sendResponse({ status: 'error', message: 'Unknown message type' });
});
