import { useEffect, useState } from "react";
import "./App.css";

const API = "http://localhost:8000";

const navItems = [
  { id: "overview", icon: "▦", label: "Overview" },
  { id: "chat", icon: "✳", label: "AI Assistant" },
  { id: "orders", icon: "▤", label: "Orders" },
  { id: "tickets", icon: "◫", label: "Support tickets" },
];

async function apiRequest(path, token, options = {}) {
  const response = await fetch(`${API}${path}`, {
    ...options,
    headers: {
      ...(options.body ? { "Content-Type": "application/json" } : {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(
      data.detail || data.message || `Request failed (${response.status})`
    );
  }

  return data;
}

function App() {
  const [token, setToken] = useState(
    () => localStorage.getItem("supportops_token") || ""
  );
  const [email, setEmail] = useState("agent@test.com");
  const [password, setPassword] = useState("password123");
  const [page, setPage] = useState("overview");
  const [orders, setOrders] = useState([]);
  const [tickets, setTickets] = useState([]);
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const [loginError, setLoginError] = useState("");

  async function login(event) {
    event.preventDefault();
    setLoading(true);
    setLoginError("");

    try {
      const data = await apiRequest("/auth/login", "", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });

      const newToken = data.access_token;

      if (!newToken) {
        throw new Error("Login response did not contain an access token.");
      }

      localStorage.setItem("supportops_token", newToken);
      setToken(newToken);
    } catch (err) {
      setLoginError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function logout() {
    localStorage.removeItem("supportops_token");
    setToken("");
    setMessages([]);
    setOrders([]);
    setTickets([]);
    setPage("overview");
    setError("");
  }

  async function loadData() {
    if (!token) return;

    setError("");

    try {
      const [orderData, ticketData] = await Promise.all([
        apiRequest("/orders/", token),
        apiRequest("/tickets/", token),
      ]);

      setOrders(Array.isArray(orderData) ? orderData : []);
      setTickets(Array.isArray(ticketData) ? ticketData : []);
    } catch (err) {
      setError(err.message);
      if (err.message.toLowerCase().includes("token")) logout();
    }
  }

  useEffect(() => {
    if (token) loadData();
  }, [token]);

  async function sendMessage(event) {
    event.preventDefault();

    const text = question.trim();
    if (!text || sending) return;

    setMessages((previous) => [...previous, { role: "user", content: text }]);
    setQuestion("");
    setSending(true);
    setError("");

    try {
      const data = await apiRequest("/agent/chat", token, {
        method: "POST",
        body: JSON.stringify({ question: text }),
      });

      setMessages((previous) => [
        ...previous,
        { role: "assistant", content: data.answer },
      ]);
    } catch (err) {
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: `I couldn't process that request: ${err.message}`,
          failed: true,
        },
      ]);
    } finally {
      setSending(false);
    }
  }

  if (!token) {
    return (
      <main className="login-screen">
        <section className="login-card">
          <div className="brand-mark">S</div>
          <p className="eyebrow">SUPPORT OPERATIONS PLATFORM</p>
          <h1>Welcome back.</h1>
          <p className="muted">
            Sign in to manage support operations with your AI assistant.
          </p>

          <form className="login-form" onSubmit={login}>
            <label htmlFor="email">Email address</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            {loginError && <div className="error-box">{loginError}</div>}

            <button className="primary-button full-width" disabled={loading}>
              {loading ? "Signing in..." : "Sign in →"}
            </button>
          </form>

          <p className="login-note">
            Development environment · FastAPI + PostgreSQL
          </p>
        </section>
      </main>
    );
  }

  const activeItem = navItems.find((item) => item.id === page);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">S</div>
          <div>
            <strong>SupportOps</strong>
            <span>AI WORKSPACE</span>
          </div>
        </div>

        <div className="nav-heading">WORKSPACE</div>
        <nav className="navigation">
          {navItems.map((item) => (
            <button
              key={item.id}
              className={`nav-item ${page === item.id ? "active" : ""}`}
              onClick={() => setPage(item.id)}
            >
              <span className="nav-icon">{item.icon}</span>
              {item.label}
              {item.id === "chat" && <span className="nav-badge">AI</span>}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="status-card">
            <span className="status-dot" />
            <div>
              <strong>Local environment</strong>
              <p>Connected to API</p>
            </div>
          </div>
          <button className="profile-button" onClick={logout}>
            <div className="avatar">
              {email.charAt(0).toUpperCase()}
            </div>
            <div className="profile-text">
              <strong>{email}</strong>
              <span>Support agent</span>
            </div>
            <span className="logout-icon">↗</span>
          </button>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div className="breadcrumbs">
            <span>Workspace</span>
            <span className="crumb-divider">/</span>
            <strong>{activeItem?.label}</strong>
          </div>
          <div className="topbar-right">
            <span className="live-indicator">
              <span className="status-dot" /> API workspace
            </span>
            <button className="refresh-button" onClick={loadData}>
              ↻ <span>Refresh</span>
            </button>
          </div>
        </header>

        <section className="page-content">
          {error && (
            <div className="error-banner">
              <span>{error}</span>
              <button onClick={() => setError("")}>×</button>
            </div>
          )}

          {page === "overview" && (
            <>
              <div className="page-heading">
                <div>
                  <p className="eyebrow">YOUR WORKSPACE</p>
                  <h1>Overview</h1>
                  <p className="muted">
                    Your support operations, all in one place.
                  </p>
                </div>
                <button
                  className="primary-button"
                  onClick={() => setPage("chat")}
                >
                  ✳ Ask AI assistant
                </button>
              </div>

              <div className="stats-grid">
                <StatCard
                  label="Total orders"
                  value={orders.length}
                  icon="▤"
                  detail="From your database"
                />
                <StatCard
                  label="Support tickets"
                  value={tickets.length}
                  icon="◫"
                  detail="Across all customers"
                />
                <StatCard
                  label="Open tickets"
                  value={
                    tickets.filter(
                      (t) =>
                        !["resolved", "closed"].includes(
                          String(t.status).toLowerCase()
                        )
                    ).length
                  }
                  icon="◷"
                  detail="Needs attention"
                />
              </div>

              <section className="welcome-panel">
                <div className="welcome-copy">
                  <span className="ai-pill">✳ AI-POWERED SUPPORT</span>
                  <h2>How can we help today?</h2>
                  <p>
                    Look up order statuses, check support tickets, or find
                    answers in your support knowledge base.
                  </p>
                  <button
                    className="light-button"
                    onClick={() => setPage("chat")}
                  >
                    Start a conversation <span>→</span>
                  </button>
                </div>
                <div className="orb" aria-hidden="true">
                  <div className="orb-inner">✳</div>
                </div>
              </section>

              <div className="section-heading">
                <div>
                  <h2>Recent orders</h2>
                  <p className="muted">Latest records from your API</p>
                </div>
                <button
                  className="text-button"
                  onClick={() => setPage("orders")}
                >
                  View all →
                </button>
              </div>

              <DataTable
                type="orders"
                rows={orders.slice(0, 5)}
                empty="No orders found. Create an order through the API first."
              />
            </>
          )}

          {page === "chat" && (
            <div className="chat-layout">
              <div className="page-heading">
                <div>
                  <p className="eyebrow">INTELLIGENT SUPPORT</p>
                  <h1>AI Assistant</h1>
                  <p className="muted">
                    Ask questions about orders, tickets, and support policies.
                  </p>
                </div>
                <span className="online-pill">
                  <span className="status-dot" /> Local AI
                </span>
              </div>

              <section className="chat-card">
                <div className="chat-card-header">
                  <div className="assistant-avatar">✳</div>
                  <div>
                    <strong>SupportOps Assistant</strong>
                    <p>Powered by your local Ollama model</p>
                  </div>
                  <span className="secure-label">● Connected</span>
                </div>

                <div className="chat-messages">
                  {messages.length === 0 && (
                    <div className="chat-welcome">
                      <div className="chat-welcome-icon">✳</div>
                      <h2>How can I help?</h2>
                      <p>
                        I can look up order and ticket information or search
                        your support policies.
                      </p>
                      <div className="suggestion-list">
                        {[
                          "What is the status of order 1?",
                          "What is the status of ticket 1?",
                          "My package arrived damaged. What should I do?",
                        ].map((suggestion) => (
                          <button
                            key={suggestion}
                            onClick={() => setQuestion(suggestion)}
                          >
                            {suggestion} <span>↗</span>
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {messages.map((message, index) => (
                    <div
                      key={index}
                      className={`message-row ${message.role}`}
                    >
                      {message.role === "assistant" && (
                        <div className="message-avatar">✳</div>
                      )}
                      <div
                        className={`message-bubble ${
                          message.failed ? "message-error" : ""
                        }`}
                      >
                        {message.content}
                      </div>
                    </div>
                  ))}

                  {sending && (
                    <div className="message-row assistant">
                      <div className="message-avatar">✳</div>
                      <div className="message-bubble typing">
                        <span />
                        <span />
                        <span />
                        Thinking...
                      </div>
                    </div>
                  )}
                </div>

                <form className="chat-input-area" onSubmit={sendMessage}>
                  <input
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask about an order, ticket, or policy..."
                    aria-label="Your question"
                    maxLength={2000}
                  />
                  <button
                    className="send-button"
                    disabled={!question.trim() || sending}
                    aria-label="Send message"
                  >
                    ↑
                  </button>
                </form>
                <p className="chat-disclaimer">
                  AI-generated responses can be inaccurate. Verify important
                  information against your records.
                </p>
              </section>
            </div>
          )}

          {page === "orders" && (
            <>
              <div className="page-heading">
                <div>
                  <p className="eyebrow">OPERATIONS</p>
                  <h1>Orders</h1>
                  <p className="muted">
                    Orders retrieved from your PostgreSQL database.
                  </p>
                </div>
                <button className="secondary-button" onClick={loadData}>
                  ↻ Refresh orders
                </button>
              </div>
              <DataTable
                type="orders"
                rows={orders}
                empty="No orders found. Create one through Swagger at /docs."
              />
            </>
          )}

          {page === "tickets" && (
            <>
              <div className="page-heading">
                <div>
                  <p className="eyebrow">CUSTOMER CARE</p>
                  <h1>Support tickets</h1>
                  <p className="muted">
                    Review ticket statuses and customer issues.
                  </p>
                </div>
                <button className="secondary-button" onClick={loadData}>
                  ↻ Refresh tickets
                </button>
              </div>
              <DataTable
                type="tickets"
                rows={tickets}
                empty="No tickets found. Create one through Swagger at /docs."
              />
            </>
          )}
        </section>
      </main>
    </div>
  );
}

function StatCard({ label, value, icon, detail }) {
  return (
    <article className="stat-card">
      <div className="stat-top">
        <span>{label}</span>
        <span className="stat-icon">{icon}</span>
      </div>
      <div className="stat-value">{value}</div>
      <p>{detail}</p>
    </article>
  );
}

function DataTable({ type, rows, empty }) {
  const isOrders = type === "orders";

  const columns = isOrders
    ? [
        ["Order", (row) => `#${row.id}`],
        ["Product", (row) => row.product_name || "—"],
        ["Customer ID", (row) => row.customer_id ?? "—"],
        ["Quantity", (row) => row.quantity ?? "—"],
        ["Status", (row) => row.status || "Unknown"],
      ]
    : [
        ["Ticket", (row) => `#${row.id}`],
        ["Subject", (row) => row.subject || "—"],
        ["Customer ID", (row) => row.customer_id ?? "—"],
        ["Order ID", (row) => row.order_id ?? "—"],
        ["Status", (row) => row.status || "Unknown"],
      ];

  return (
    <div className="table-card">
      {rows.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">{isOrders ? "▤" : "◫"}</div>
          <strong>Nothing to show yet</strong>
          <p>{empty}</p>
        </div>
      ) : (
        <div className="table-scroll">
          <table>
            <thead>
              <tr>
                {columns.map(([label]) => (
                  <th key={label}>{label}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.id}>
                  {columns.map(([label, getValue]) => {
                    const value = getValue(row);
                    const isStatus = label === "Status";
                    return (
                      <td key={label}>
                        {isStatus ? (
                          <span
                            className={`status-badge ${String(value)
                              .toLowerCase()
                              .replace(/[^a-z0-9]+/g, "-")}`}
                          >
                            <span className="badge-dot" />
                            {value}
                          </span>
                        ) : (
                          value
                        )}
                      </td>
                    );
                  })}
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