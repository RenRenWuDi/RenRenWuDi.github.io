/**
 * 微信公众号引流卡片 - 自动注入文章底部
 * 公众号: 区块链编程
 * 更新: 2026-07-10 修复加载时机
 */
(function () {
  function inject() {
    var container = document.querySelector('#article-container, .post-content, article.container, .article-content');
    if (!container) return;
    if (document.querySelector('.wechat-promo-card')) return;

    var card = document.createElement('div');
    card.className = 'wechat-promo-card';
    card.innerHTML =
      '<div class="promo-title">📱 关注公众号「区块链编程」</div>' +
      '<div class="promo-desc">更多区块链技术干货、Web3开发实战、量化交易策略<br>第一时间推送，关注「区块链编程」公众号</div>' +
      '<img class="promo-qr" src="/img/wechat-qr.png" alt="区块链编程公众号二维码" onerror="this.style.display=\'none\'">' +
      '<a class="promo-cta" href="/about/">扫码关注</a>';

    container.appendChild(card);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject);
  } else {
    inject();
  }
})();
