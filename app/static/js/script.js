let mode = 'chat', pdfFile = null;

function setMode(m, el) {
    mode = m;
    document.querySelectorAll('.ni').forEach(i => i.classList.remove('on'));
    el.classList.add('on');
    if (m === 'pdf') document.getElementById('pdfOv').classList.add('open');
}

function grow(el) { el.style.height = 'auto'; el.style.height = el.scrollHeight + 'px'; }
function handleKey(e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } }
function closeOv(id) { document.getElementById(id).classList.remove('open'); }

async function send() {
    const el = document.getElementById('inp'), txt = el.value.trim();
    if (!txt) return;
    document.getElementById('wl')?.remove();
    addMsg('u', txt);
    el.value = '';
    
    const r = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: txt, mode })
    });
    const d = await r.json();
    const w = addMsg('a', d.reply);
    
    // SMART ACTION LOGIC
    const acts = document.createElement('div'); acts.className = 'acts';
    if (d.code_blocks && d.code_blocks.length > 0) {
        const zb = document.createElement('button'); zb.className='ab'; zb.innerHTML='📦 ZIP';
        zb.onclick=()=>dlZip(d.code_blocks); acts.appendChild(zb);
    }
    const pb = document.createElement('button'); pb.className='ab'; pb.innerHTML='📥 PDF';
    pb.onclick=()=>dlPDF(d.reply); acts.appendChild(pb);
    w.querySelector('.bub').appendChild(acts);
}

function addMsg(role, text) {
    const chat = document.getElementById('chat');
    const w = document.createElement('div');
    w.className = `msg ${role}`;
    w.innerHTML = `<div class="bub">${text}</div>`;
    chat.appendChild(w);
    w.scrollIntoView();
    return w;
}

async function dlPDF(content) {
    const r = await fetch('/download-plan', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({content})});
    const b = await r.blob(); const u = URL.createObjectURL(b);
    const a = document.createElement('a'); a.href=u; a.download='mark4k.pdf'; a.click();
}

async function dlZip(blocks) {
    const r = await fetch('/download-zip', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({code_blocks:blocks})});
    const b = await r.blob(); const u = URL.createObjectURL(b);
    const a = document.createElement('a'); a.href=u; a.download='code.zip'; a.click();
}

function onPDF(i) { pdfFile = i.files[0]; }
async function submitPDF() {
    if(!pdfFile) return;
    const fd = new FormData(); fd.append('file', pdfFile);
    closeOv('pdfOv');
    const r = await fetch('/analyze-pdf', {method:'POST', body:fd});
    const d = await r.json();
    addMsg('a', d.reply);
}
