export default {
  async fetch(request, env, ctx) {
    // Разрешаем CORS для всех
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
        },
      });
    }

    const url = new URL(request.url);
    const streamUrl = url.searchParams.get('url');
    
    if (!streamUrl) {
      // Дефолтный стрим, если не указан
      const defaultStream = 'http://stream.zeno.fm/0r0xa792kwzuv';
      return await proxyStream(defaultStream);
    }

    return await proxyStream(streamUrl);
  }
};

async function proxyStream(streamUrl) {
  try {
    const response = await fetch(streamUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'audio/*',
      },
    });

    // Создаем новый ответ с CORS заголовками
    const newResponse = new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': response.headers.get('Content-Type') || 'audio/mpeg',
      },
    });

    return newResponse;
  } catch (error) {
    return new Response(`Error: ${error.message}`, { status: 500 });
  }
}