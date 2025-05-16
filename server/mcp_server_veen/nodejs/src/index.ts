export * from './server';

import { registerServices, registerTools } from './registry';

(function() {
  registerServices();
  registerTools();
})();
