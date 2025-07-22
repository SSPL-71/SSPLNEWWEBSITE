self.addEventListener('install', () => {
  console.log('Service Worker installed');
});

self.addEventListener('fetch', event => {
  // You can customize caching behavior here later
});