// extension/content/domHelpers.js

/**
 * domHelpers.js
 *
 * A collection of helper functions for querying and manipulating
 * the ChatGPT page DOM.
 */

/**
 * Returns the first Element matching the selector, or null.
 * @param {string} selector - CSS selector to query.
 * @returns {Element|null}
 */
export function getElement(selector) {
    return document.querySelector(selector);
  }
  
  /**
   * Returns all Elements matching the selector.
   * @param {string} selector - CSS selector to query.
   * @returns {NodeListOf<Element>}
   */
  export function getElements(selector) {
    return document.querySelectorAll(selector);
  }
  
  /**
   * Checks whether the given element (or any ancestor up to <html>) has the given class.
   * @param {Element} element
   * @param {string} className
   * @returns {boolean}
   */
  export function elementHasClass(element, className) {
    let el = element;
    while (el && el !== document.documentElement) {
      if (el.classList && el.classList.contains(className)) {
        return true;
      }
      el = el.parentElement;
    }
    return false;
  }
  
  /**
   * Returns the trimmed textContent of an element (or empty string).
   * @param {Element} element
   * @returns {string}
   */
  export function getTextContent(element) {
    return element && element.textContent ? element.textContent.trim() : "";
  }
  
  /**
   * A simple throttle: ensures `fn` is only called at most once per `wait` ms.
   * @param {Function} fn   The function to throttle.
   * @param {number} wait   Minimum time between calls, in milliseconds.
   * @returns {Function}
   */
  export function throttle(fn, wait) {
    let last = 0;
    return function(...args) {
      const now = Date.now();
      if (now - last >= wait) {
        last = now;
        fn.apply(this, args);
      }
    };
  }
  
  /**
   * Finds all new message bubble elements, based on a given selector,
   * and returns them as an Array.
   * @param {string} selector - CSS selector for the message bubbles.
   * @returns {Element[]}
   */
  export function findNewMessageElements(selector) {
    return Array.from(document.querySelectorAll(selector));
  }
  