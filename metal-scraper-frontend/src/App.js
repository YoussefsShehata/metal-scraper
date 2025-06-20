import React, { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState("");

  const handleSearch = () => {
    if (!query.trim()) return;

    setLoading(true);
    setError("");
    setProgress(0);
    setResults([]);

    const eventSource = new EventSource(
      `http://127.0.0.1:8000/scrape-stream?search=${encodeURIComponent(query)}`
    );

    eventSource.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        if (payload.progress) setProgress(payload.progress);

        if (payload.message === "done" && payload.data) {
          setResults(payload.data);
          setLoading(false);
          eventSource.close();
        }

        if (payload.message === "error") {
          setError("❌ " + payload.error);
          setLoading(false);
          eventSource.close();
        }
      } catch (err) {
        console.error("Failed to parse SSE message:", err);
      }
    };

    eventSource.onerror = () => {
      setError("❌ Connection error. Please try again.");
      setLoading(false);
      eventSource.close();
    };
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>📦 Metal Price Scraper</h1>
        <p>Search for stainless steel products on Made-in-China</p>
      </header>

      <div className="search-container">
        <input
          type="text"
          placeholder="e.g. stainless steel TP316L seamless pipe"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      {loading && (
        <div className="progress-bar-container">
          <div className="progress-bar" style={{ width: `${progress}%` }}>
            {progress}%
          </div>
        </div>
      )}

      {error && <p className="error">{error}</p>}

      {results.length > 0 && (
        <div className="results-table">
          <table>
            <thead>
              <tr>
                <th>Product Title</th>
                <th>Supplier</th>
                <th>Price</th>
                <th>MOQ</th>
                <th>Link</th>
              </tr>
            </thead>
            <tbody>
              {results.map((item, index) => (
                <tr key={index}>
                  <td>{item.title}</td>
                  <td>{item.supplier}</td>
                  <td>{item.raw_price}</td>
                  <td>{item.moq}</td>
                  <td>
                    <a href={item.link} target="_blank" rel="noopener noreferrer">
                      🔗 View
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
