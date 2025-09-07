// Polyfill BroadcastChannel for MSW in Jest/node
if (typeof global.BroadcastChannel === 'undefined') {
  global.BroadcastChannel = class {
    constructor() {}
    postMessage() {}
    close() {}
    addEventListener() {}
    removeEventListener() {}
  };
}
// Polyfill TextEncoder/TextDecoder for Jest/node, before anything else
if (typeof global.TextEncoder === 'undefined') {
  const { TextEncoder, TextDecoder } = require('util');
  global.TextEncoder = TextEncoder;
  global.TextDecoder = TextDecoder;
}

// Polyfill TransformStream for MSW/node-fetch in Jest/node
if (typeof global.TransformStream === 'undefined') {
  global.TransformStream = class {
    constructor() {
      // Minimal stub for MSW/node-fetch
    }
  };
}
