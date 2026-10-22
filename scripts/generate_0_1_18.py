from pathlib import Path

p = Path('八卦搜索.user.js')
text = p.read_text(encoding='utf-8')

text = text.replace('@version      0.1.17', '@version      0.1.18')
text = text.replace('// 0.1.17 test build generated from 0.1.16.', '// 0.1.18 test build generated from 0.1.17.')
text = text.replace('直接拖拽执行内圈功能', '直接拖拽，执行搜索盘内圈功能')

marker = '/* 0.1.18 UI refinements */'
if marker not in text:
    patch = r'''/* 0.1.18 UI refinements */
(function(){
  const css = `
    [class*="custom-site"] p,[class*="custom-website"] p,.custom-site-hint,.custom-website-hint{white-space:pre-line!important}
    .engine-item,.site-item,.p-site-item{display:flex!important;align-items:center!important;gap:8px!important}
    .engine-item img,.site-item img,.p-site-item img{margin-top:0!important;flex:0 0 auto!important}
    .engine-library .engine-item,.engine-library .site-item{margin-left:-14px!important;padding-left:0!important}
    .engine-library input[type="checkbox"],.engine-library .engine-actions,.engine-library .site-actions{margin-left:-14px!important}
    [class*="text-menu"],[class*="selection-menu"],[class*="search-menu"]{display:flex!important;align-items:center!important;background:#fff!important;border:1px solid #d9e2ec!important;border-radius:18px!important;padding:6px 10px!important;box-shadow:0 6px 18px rgba(15,23,42,.12)!important}
    [class*="text-menu"] [class*="item"],[class*="selection-menu"] [class*="item"],[class*="search-menu"] [class*="item"]{width:30px!important;height:30px!important;border:1px solid #d9e2ec!important;border-radius:8px!important;display:flex!important;align-items:center!important;justify-content:center!important;transition:transform .15s ease!important}
    [class*="text-menu"] [class*="item"]:hover,[class*="selection-menu"] [class*="item"]:hover,[class*="search-menu"] [class*="item"]:hover{transform:scale(1.18)!important}
    .p-modal{position:fixed!important;z-index:999999!important}
    .p-modal .panel-cats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:10px 0}
    .p-modal .panel-cats button{padding:10px;border-radius:10px;border:1px solid #d9e2ec;background:#fff;cursor:pointer}
    .p-modal.draggable{cursor:move}
    .bagua-panel-size{display:flex;align-items:center;gap:8px;margin-top:10px}
    .bagua-panel-size input[type=range]{width:160px}
  `;
  const style = document.createElement('style');
  style.textContent = css;
  document.documentElement.appendChild(style);

  const tencentIcon = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64"><rect width="64" height="64" rx="12" fill="#4285f4"/><text x="32" y="42" font-size="34" text-anchor="middle" fill="#fff">译</text></svg>');

  const fixIcons = () => {
    document.querySelectorAll('img').forEach(img => {
      const label = [img.alt, img.title, img.getAttribute('aria-label')].join(' ');
      if (label.includes('腾讯翻译')) img.src = tencentIcon;
    });
  };

  const fixCustomText = () => {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
    let node;
    while ((node = walker.nextNode())) {
      if (node.nodeValue.includes('输入填写网址，自动识别搜索规则。如果自动识别不成功，可以自行添加。')) {
        node.nodeValue = '输入填写网址，自动识别搜索规则。\n如果自动识别不成功，可以自行添加。';
      }
    }
  };

  const makeDraggable = panel => {
    if (panel.dataset.baguaDraggable) return;
    panel.dataset.baguaDraggable = '1';
    let dragging = false, startX = 0, startY = 0, originX = 0, originY = 0;
    panel.addEventListener('pointerdown', event => {
      if (event.target.closest('input,textarea,select,button,a')) return;
      dragging = true;
      panel.classList.add('draggable');
      const rect = panel.getBoundingClientRect();
      startX = event.clientX; startY = event.clientY;
      originX = rect.left; originY = rect.top;
      panel.setPointerCapture(event.pointerId);
    });
    panel.addEventListener('pointermove', event => {
      if (!dragging) return;
      const left = Math.max(0, Math.min(window.innerWidth - panel.offsetWidth, originX + event.clientX - startX));
      const top = Math.max(0, Math.min(window.innerHeight - panel.offsetHeight, originY + event.clientY - startY));
      panel.style.left = left + 'px';
      panel.style.top = top + 'px';
      panel.style.right = 'auto';
      panel.style.bottom = 'auto';
    });
    panel.addEventListener('pointerup', () => {
      dragging = false;
      panel.classList.remove('draggable');
    });
  };

  const addPanelSizeSetting = panel => {
    if (!panel.textContent.includes('设置') || panel.querySelector('.bagua-panel-size')) return;
    const wrap = document.createElement('label');
    wrap.className = 'bagua-panel-size';
    wrap.innerHTML = '<span>功能面板大小</span><input type="range" min="70" max="160" step="5">';
    const input = wrap.querySelector('input');
    const current = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--bagua-panel-scale')) || 1;
    input.value = Math.round(current * 100);
    input.addEventListener('input', () => {
      document.documentElement.style.setProperty('--bagua-panel-scale', (input.value / 100).toFixed(3));
    });
    panel.appendChild(wrap);
  };

  const addPanelCategories = panel => {
    if (!panel.textContent.includes('功能面板') || panel.querySelector('.panel-cats')) return;
    const host = panel.querySelector('.p-site-list') || panel.querySelector('.p-grid') || panel.querySelector('.p-quick')?.parentElement;
    if (!host) return;
    const cats = document.createElement('div');
    cats.className = 'panel-cats';
    [['search','搜索引擎'],['video','视频搜索'],['music','音乐搜索'],['image','识图搜索'],['translate','翻译网站'],['general','综合搜索']].forEach(([kind,label]) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = label;
      button.addEventListener('click', () => {
        const tab = [...panel.querySelectorAll('button')].find(item => item.textContent.trim() === label);
        if (tab) tab.click();
      });
      cats.appendChild(button);
    });
    host.insertBefore(cats, host.children[3] || null);
  };

  const patchPanels = () => {
    document.querySelectorAll('.p-modal').forEach(panel => {
      makeDraggable(panel);
      addPanelSizeSetting(panel);
      addPanelCategories(panel);
    });
  };

  const queue = () => {
    fixIcons();
    fixCustomText();
    patchPanels();
  };

  const start = () => {
    queue();
    new MutationObserver(() => setTimeout(queue, 50)).observe(document.documentElement, { childList: true, subtree: true });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start, { once: true });
  } else {
    start();
  }
})();'''
    text += '\n\n' + patch + '\n'

p.write_text(text, encoding='utf-8')
