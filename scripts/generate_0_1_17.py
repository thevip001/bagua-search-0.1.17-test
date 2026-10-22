from pathlib import Path

src = Path('source/八卦搜索.user.js')
out = Path('八卦搜索.user.js')
text = src.read_text(encoding='utf-8')

text = text.replace('@version      0.1.16', '@version      0.1.17')
marker = '// 0.1.17 test build generated from 0.1.16.'
if marker not in text:
    text = marker + '\n' + text

# DEFAULT: add wheel colors and panel scale
old_default = 'wheelScale:90,wheelGap:false,'
new_default = 'wheelScale:90,wheelColors:{outerLight:"#ffffff",outerDark:"#454545",innerLight:"#ffffff",innerDark:"#454545",center:"#ffffff",outerText:"#25313d",innerText:"#25313d"},panelScale:100,'
assert old_default in text
text = text.replace(old_default, new_default, 1)

# COMMON_KEYS: persist new settings
old_common = "const COMMON_KEYS=['box','boxKey','boxSize','boxPosition','super','superKey','normal','foreground','wheelScale','wheelGap','language','recordMode','quickPanel'];"
new_common = "const COMMON_KEYS=['box','boxKey','boxSize','boxPosition','super','superKey','normal','foreground','wheelScale','wheelColors','panelScale','wheelGap','language','recordMode','quickPanel'];"
assert old_common in text
text = text.replace(old_common, new_common, 1)

# drawWheel: fixed rings, colors, larger labels
pairs = [
    ("for(const[ring,r1,r2,labelR]of (cfg.wheelGap?[['Outer',114,178,147],['Inner',34,103,73]]:[['Outer',109,178,147],['Inner',34,109,73]]))", "for(const[ring,r1,r2,labelR]of [['Outer',109,178,147],['Inner',34,109,73]])"),
    ("ring=wheelRingAtRadius(r,cfg.wheelGap)", "ring=wheelRingAtRadius(r,false)"),
    ("const gapLabel=el('label',undefined,top),gapToggle=el('input',undefined,gapLabel);gapToggle.type='checkbox';gapToggle.checked=!!cfg.wheelGap;gapLabel.append('内外圈间隔');gapToggle.onchange=()=>{cfg.wheelGap=gapToggle.checked;persist();draw();};", ""),
    ("svg('circle',{cx:190,cy:190,r:178,fill:'#e9edf2'},drawing);", "const wc=cfg.wheelColors||{};svg('circle',{cx:190,cy:190,r:178,fill:wc.outerLight||'#ffffff'},drawing);"),
    ("const center=svg('circle',{cx:190,cy:190,r:25,fill:'#fff',stroke:'#b6c5d3',class:'center'},cg);", "const center=svg('circle',{cx:190,cy:190,r:34,fill:wc.center||'#ffffff',stroke:'#b6c5d3','stroke-width':2,class:'center'},cg);"),
    ("path=svg('path',{d:sectorPath(r1,r2,i),fill:dark?'#454545':'#fff',class:'sector'},g);const color=dark?'#fff':'#25313d';", "path=svg('path',{d:sectorPath(r1,r2,i),fill:dark?(ring==='Inner'?(wc.innerDark||'#454545'):(wc.outerDark||'#454545')):(ring==='Inner'?(wc.innerLight||'#ffffff'):(wc.outerLight||'#ffffff')),class:'sector'},g);const color=dark?'#fff':(ring==='Inner'?(wc.innerText||'#25313d'):(wc.outerText||'#25313d'));"),
    ("const text=(x,y,value,size=14)=>{", "const text=(x,y,value,size=17)=>{"),
    ("chars.forEach((ch,j)=>text(190+(i===1?147:-147),190-(chars.length-1)*17/2+5+j*17,ch));", "chars.forEach((ch,j)=>text(190+(i===1?147:-147),190-(chars.length-1)*20/2+6+j*20,ch));"),
    ("const cw=/[\\x00-\\xff]/.test(ch)?8:14;", "const cw=/[\\x00-\\xff]/.test(ch)?10:17;"),
    ("const symbol=id!=='ocr'&&a.symbol;if(symbol)text(point[0],point[1]-(ring==='Outer'?10:13),symbol,19);", "const symbol=id!=='ocr'&&a.symbol;if(symbol)text(point[0],point[1]-(ring==='Outer'?12:15),symbol,22);"),
    ("const first=symbol?(lines.length>1?7:13):(lines.length>1?-2:5);lines.forEach((value,j)=>text(point[0],point[1]+first+j*17,value));", "const first=symbol?(lines.length>1?8:15):(lines.length>1?-2:6);lines.forEach((value,j)=>text(point[0],point[1]+first+j*20,value));")
]
for old, new in pairs:
    assert old in text, 'missing snippet: ' + old[:60]
    text = text.replace(old, new, 1)

# CSS2: panel scale and new panel/search styles
css_marker = '/* 0.1.16 layout and whole-button hover */'
css2 = '''
:root{--bagua-panel-scale:1;}
.p-modal{zoom:var(--bagua-panel-scale);}
.p-site-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px;}
.p-site-item{display:flex;align-items:center;gap:8px;padding:8px;border-radius:10px;background:#fff;border:1px solid #d9e2ec;cursor:pointer;}
.p-site-item:hover{border-color:#9db4c8;}
.p-site-icon{width:18px;height:18px;}
.p-site-name{font-size:13px;color:#25313d;}
.p-quick{display:flex;gap:8px;margin-top:10px;}
.panel-image{padding:6px 10px;border-radius:8px;border:1px solid #d9e2ec;background:#fff;cursor:pointer;}
.panel-input{width:100%;padding:10px;border-radius:10px;border:1px solid #d9e2ec;margin-bottom:10px;}
.input-search-tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px;}
.input-search-tabs button{padding:6px 10px;border-radius:999px;border:1px solid #d9e2ec;background:#fff;cursor:pointer;}
.input-search-tabs button.active{background:#25313d;color:#fff;border-color:#25313d;}
.p-search-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:8px;}
.p-search-item{display:flex;align-items:center;gap:8px;padding:8px;border-radius:10px;background:#fff;border:1px solid #d9e2ec;cursor:pointer;}
'''
assert css_marker in text
text = text.replace(css_marker, css2 + '\n' + css_marker, 1)

# Apply panel scale on startup
old_startup = 'cfg=profileConfig(profileState);\nlet saveIndicator=null;'
new_startup = "cfg=profileConfig(profileState);\ndocument.documentElement.style.setProperty('--bagua-panel-scale',((cfg.panelScale||100)/100).toFixed(3));\nlet saveIndicator=null;"
assert old_startup in text
text = text.replace(old_startup, new_startup, 1)

def replace_function(src, name, new):
    start = src.index('function ' + name + '(')
    open_brace = src.index('{', start)
    depth = 0
    for i in range(open_brace, len(src)):
        if src[i] == '{':
            depth += 1
        elif src[i] == '}':
            depth -= 1
            if depth == 0:
                return src[:start] + new + src[i+1:]
    raise ValueError('unbalanced function: ' + name)

open_panel_new = '''function openPanel(){
  const pOpen=panel('功能面板','textmodal p-modal');
  const ph=phone(pOpen);
  ph.tabs.innerHTML='';
  ph.grid.innerHTML='';
  ph.hint.textContent='点按图标直接打开；按住可固定到悬浮球。';
  Object.entries(CATEGORY).forEach(([kind,label])=>{
    const tab=el('button',label,ph.tabs);
    tab.type='button';
    if(kind==='search')tab.classList.add('active');
    tab.onclick=()=>{[...ph.tabs.children].forEach(x=>x.classList.remove('active'));tab.classList.add('active');grid(ph.grid,kind);};
  });
  const grid=(host,kind)=>{
    host.innerHTML='';
    const siteList=el('div',undefined,host);
    siteList.className='p-site-list';
    cfg.engines.filter(x=>x.kind===kind&&x.enabled!==false).forEach(engine=>{
      const item=el('button',undefined,siteList);
      item.type='button';
      item.className='p-site-item';
      const icon=attachIcon(item,engine);
      icon.classList.add('p-site-icon');
      el('span',engine.name,item).className='p-site-name';
      item.onclick=()=>runEngine(engine);
    });
    const quick=el('div',undefined,host);
    quick.className='p-quick';
    [['翻译','translate'],['识图','image'],['网盘','pan']].forEach(([label,k])=>{const b=button(label,()=>action(k));b.className='panel-image';quick.append(b);});
  };
  grid(ph.grid,'search');
  return pOpen;
}'''

input_search_new = '''function inputSearch(engine=null){
  const pOpen=panel('搜索','textmodal p-modal');
  const ph=phone(pOpen);
  ph.hint.textContent='输入关键词后选择站点；按 Esc 关闭。';
  const input=el('input',undefined,ph.grid);
  input.className='panel-input';
  input.placeholder='输入关键词…';
  input.value=(typeof selectedText==='function'?selectedText():'')||'';
  const tabs=el('div',undefined,ph.grid);
  tabs.className='input-search-tabs';
  const list=el('div',undefined,ph.grid);
  list.className='p-search-list';
  const open=(engine,q)=>{const url=engine.url.includes('%s')?engine.url.replace('%s',encodeURIComponent(q)):engine.url;window.open(url,'_blank');};
  const render=k=>{
    list.innerHTML='';
    cfg.engines.filter(x=>x.enabled!==false&&x.kind===k).forEach(engine=>{
      const item=el('button',undefined,list);
      item.type='button';
      item.className='p-search-item';
      const icon=attachIcon(item,engine);
      icon.classList.add('p-site-icon');
      el('span',engine.name,item).className='p-site-name';
      item.onclick=()=>{const q=input.value.trim();if(q)open(engine,q);};
    });
  };
  Object.entries(CATEGORY).forEach(([k,label],i)=>{
    const tab=el('button',label,tabs);
    tab.type='button';
    tab.dataset.kind=k;
    if(i===0)tab.classList.add('active');
    tab.onclick=()=>{[...tabs.children].forEach(x=>x.classList.remove('active'));tab.classList.add('active');render(k);};
  });
  render('search');
  const commit=()=>{const q=input.value.trim();if(!q)return;const active=[...tabs.children].find(x=>x.classList.contains('active'));const kind=active?.dataset.kind||'search';const en=cfg.engines.find(x=>x.enabled!==false&&x.kind===kind);if(en)open(en,q);};
  input.onkeydown=e=>{if(e.key==='Enter')commit();if(e.key==='Escape')pOpen.remove();};
  setTimeout(()=>input.focus(),50);
  return pOpen;
}'''

if 'function openPanel(' in text:
    text = replace_function(text, 'openPanel', open_panel_new)
else:
    text = open_panel_new + '\n' + text

if 'function inputSearch(' in text:
    text = replace_function(text, 'inputSearch', input_search_new)
else:
    text = input_search_new + '\n' + text

out.write_text(text, encoding='utf-8')
