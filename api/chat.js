module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store, max-age=0');

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Use POST.' });
  }

  try {
    let body = req.body;
    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch (e) { body = {}; }
    }
    body = body || {};

    const msg = String(body.msg || '').slice(0, 2000);
    const session = String(body.session || '').slice(0, 120);

    if (!msg) {
      return res.status(400).json({ error: 'Mensagem vazia.' });
    }

    const base = 'https://script.google.com/macros/s/AKfycbxPkDLzvapuTMPWEREMhqCXHdaRzsouYdAxj80O4HSvTHWq2gIqDqUdXwwV3EiXFfxKYg/exec';
    const url = base + '?api=chat&msg=' + encodeURIComponent(msg) + '&session=' + encodeURIComponent(session);

    const r = await fetch(url, { redirect: 'follow' });
    if (!r.ok) {
      return res.status(502).json({ error: 'Cérebro indisponível.' });
    }

    const data = await r.json();
    return res.status(200).json(data);
  } catch (e) {
    console.error('[chat] erro:', e);
    return res.status(500).json({ error: 'Falha na comunicação com o Guardião.' });
  }
};
