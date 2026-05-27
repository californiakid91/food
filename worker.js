export default {
  async fetch(request) {
    const url = new URL(request.url);
    const ticker = url.searchParams.get('t');
    if (!ticker) {
      return new Response(JSON.stringify({ error: 'Missing ?t=TICKER' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
      });
    }

    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET',
          'Access-Control-Allow-Headers': 'Content-Type',
        }
      });
    }

    try {
      const yahooUrl = `https://query2.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(ticker)}?interval=1d&range=1d`;
      const resp = await fetch(yahooUrl, {
        headers: { 'User-Agent': 'Mozilla/5.0' }
      });
      const data = await resp.json();
      const price = data?.chart?.result?.[0]?.meta?.regularMarketPrice;
      const currency = data?.chart?.result?.[0]?.meta?.currency;
      return new Response(JSON.stringify({ price, currency, ticker }), {
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
      });
    } catch (e) {
      return new Response(JSON.stringify({ error: e.message }), {
        status: 500,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
      });
    }
  }
};
