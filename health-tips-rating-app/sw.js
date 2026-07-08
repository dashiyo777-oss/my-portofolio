/*
 * Kiku — Service Worker（オフライン対応）
 * 方針: HTML/JS/CSS/データは「ネット優先→失敗時キャッシュ」。
 *       更新の反映を最優先し、オフライン時のみキャッシュで動かす。
 *       画像・フォント等は「キャッシュ優先」。
 * 更新時は CACHE のバージョン番号を上げること（例: kiku-v2）。
 */
var CACHE = "kiku-v1";
var CORE = [
  "./",
  "./index.html",
  "./style.css",
  "./app.js",
  "./data.js",
  "./manifest.webmanifest",
  "./icon-192.png",
  "./icon-512.png"
];

self.addEventListener("install", function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) { return c.addAll(CORE); }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET") return;
  var url = new URL(req.url);

  // 同一オリジンのアプリ本体: ネット優先（成功したらキャッシュ更新）→ オフライン時はキャッシュ
  if (url.origin === location.origin) {
    e.respondWith(
      fetch(req).then(function (res) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
        return res;
      }).catch(function () {
        return caches.match(req).then(function (hit) {
          return hit || caches.match("./index.html");
        });
      })
    );
    return;
  }

  // 外部（Googleフォント等）: キャッシュ優先 → なければネット
  e.respondWith(
    caches.match(req).then(function (hit) {
      if (hit) return hit;
      return fetch(req).then(function (res) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
        return res;
      }).catch(function () { return hit; });
    })
  );
});
