from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from GoogleNews import GoogleNews

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>GoogleNews Web UI</title>
  <style>body{font-family:sans-serif;padding:20px;max-width:800px;margin:auto;}</style>
</head>
<body>
  <h1>GoogleNews Accessible Search</h1>
  <form id="search-form">
    <label for="q">Search Term <span aria-hidden="true">*</span></label>
    <input id="q" name="q" type="text" aria-label="Search term" required />
    <button type="submit" aria-label="Search news">Search</button>
  </form>
  <div id="results" aria-live="polite" style="margin-top:20px;"></div>
  <script>
    document.getElementById('search-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const resultsDiv = document.getElementById('results');
      resultsDiv.innerHTML = '<p aria-busy="true">Loading...</p>';
      try {
        const q = document.getElementById('q').value;
        const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
        const data = await res.json();
        if (data.length === 0) { resultsDiv.innerHTML = '<p>No results found.</p>'; return; }
        resultsDiv.innerHTML = '';
        data.forEach(item => {
          const div = document.createElement('div');
          div.style.cssText = 'margin-bottom:15px; border-bottom: 1px solid #eee; padding-bottom:10px;';
          const a = document.createElement('a');
          a.href = item.link || '#';
          a.target = '_blank';
          a.rel = 'noopener noreferrer';
          const h3 = document.createElement('h3');
          h3.textContent = item.title || 'Untitled';
          a.appendChild(h3);
          const p = document.createElement('p');
          p.textContent = item.date || '';
          div.appendChild(a);
          div.appendChild(p);
          resultsDiv.appendChild(div);
        });
      } catch (err) { resultsDiv.innerHTML = '<p>Error loading results.</p>'; }
    });
  </script>
</body>
</html>"""

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        elif self.path.startswith('/api/search?q='):
            q = urllib.parse.unquote(self.path.split('=')[1])
            try:
                gn = GoogleNews(lang='en', period='7d')
                gn.search(q)
                res = gn.results()
            except Exception:
                res = []
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(res, default=str).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8000), RequestHandler)
    print("Serving on http://127.0.0.1:8000")
    server.serve_forever()
