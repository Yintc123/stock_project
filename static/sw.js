// install
self.addEventListener('install', (event) => {
    // console.log('installing…');
});

// activate
self.addEventListener('activate', (event) => {
    // console.log('now ready to handle fetches!');
});

// fetch
// self.addEventListener('fetch', (event) => {
//     console.log('now fetch!');
// });

self.addEventListener('push', function(event){
    console.log('收到推播訊息', event.data.json());
    let contentObj = {title: '新訊息', body: '預設訊息，會被伺服器訊息覆蓋'};
    if(event.data){
        contentObj = event.data.json();
    }
    let options = {
        body: contentObj.body,
        // tag: 'first-notification' //僅通知一次
    };
    event.waitUntil(self.registration.showNotification(contentObj.title, options));
});