import { vi } from 'vitest';

Object.defineProperty(window, 'matchMedia', { writable: true, value: vi.fn(query => ({
  matches: false, media: query, addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {}, dispatchEvent() {},
})) });
globalThis.ResizeObserver = class { observe() {} unobserve() {} disconnect() {} };
Element.prototype.scrollIntoView = vi.fn();
window.scrollTo = vi.fn();
let previewId = 0;
URL.createObjectURL = vi.fn(() => `blob:fixture-image-${++previewId}`);
URL.revokeObjectURL = vi.fn();
