// Conditional export: Vite/browser gets apiBase.vite.js, Node/Jest gets apiBase.node.js
// Vite will resolve the .vite.js file, Node will resolve .node.js
// See package.json "exports" for proper mapping if needed
let API_BASE;
if (typeof process !== 'undefined' && process.versions && process.versions.node) {
	// Node or Jest
	API_BASE = require('./apiBase.node.js').default;
} else {
	// Browser/Vite
	API_BASE = require('./apiBase.vite.js').default;
}
export default API_BASE;
