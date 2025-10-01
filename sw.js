self.addEventListener('install', () => {
  console.log('Service Worker installed');
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Bypass compression route to avoid interference
  if (url.pathname === '/compress') return;

  // You can customize caching behavior here later
});