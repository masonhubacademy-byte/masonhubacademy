module.exports = async function handler(req, res) {
  try {
    const URL = 'https://script.google.com/macros/s/AKfycbxPkDLzvapuTMPWEREMhqCXHdaRzsouYdAxj80O4HSvTHWq2gIqDqUdXwwV3EiXFfxKYg/exec?api=brain';
    const r = await fetch(URL, { redirect: 'follow' });
    if (!r.ok) {
      return res.status(502).json({ error: 'Cérebro indisponível.' });
    }
    const data = await r.json();
    res.setHeader('Cache-Control', 'no-store, max-age=0');
    return res.status(200).json(data);
  } catch (e) {
    console.error('[brain] erro:', e);
    return res.status(500).json({ error: 'Falha ao carregar a base.' });
  }
};
