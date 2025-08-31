
import React, { useState } from 'react';
import Layout from '../../components/Layout';
import Head from 'next/head';

export default function MCPChatPage() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleQuerySubmit = async () => {
    if (!query.trim()) return;

    const userMessage = { sender: 'user', text: query };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setQuery('');
    setLoading(true);

    try {
      // For simplicity, we'll hardcode a search for courses for now.
      // In a real scenario, you'd parse the query and call the appropriate MCP endpoint.
      const response = await fetch(`/api/mcp/search/courses?query=${encodeURIComponent(query)}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

      const mcpMessage = { sender: 'mcp', text: JSON.stringify(data, null, 2) };
      setMessages((prevMessages) => [...prevMessages, mcpMessage]);
    } catch (error) {
      console.error('Error fetching from MCP server:', error);
      setMessages((prevMessages) => [...prevMessages, { sender: 'mcp', text: `Error: ${error.message}` }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <Head>
        <title>MCP Chat</title>
      </Head>
      <div className="flex flex-col h-full">
        <h1 className="text-2xl font-bold mb-4">MCP Course Advisor Chat</h1>
        <div className="flex-1 overflow-y-auto border p-4 rounded mb-4 bg-gray-50">
          {messages.map((msg, index) => (
            <div key={index} className={`mb-2 ${msg.sender === 'user' ? 'text-right' : 'text-left'}`}>
              <span className={`inline-block p-2 rounded ${msg.sender === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'}`}>
                {msg.text}
              </span>
            </div>
          ))}
          {loading && (
            <div className="text-center text-gray-500">
              Loading...
            </div>
          )}
        </div>
        <div className="flex">
          <input
            type="text"
            className="flex-1 border rounded-l p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                handleQuerySubmit();
              }
            }}
            placeholder="Ask about courses (e.g., 'machine learning')"
          />
          <button
            className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-r focus:outline-none focus:ring-2 focus:ring-blue-500"
            onClick={handleQuerySubmit}
            disabled={loading}
          >
            Send
          </button>
        </div>
      </div>
    </Layout>
  );
}
