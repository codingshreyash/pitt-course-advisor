
import { NextResponse } from 'next/server';

const MCP_SERVER_BASE_URL = process.env.MCP_SERVER_BASE_URL || 'http://localhost:8000';

export async function GET(request) {
  const { pathname, searchParams } = new URL(request.url);
  const path = pathname.replace('/api/mcp', '');
  const targetUrl = `${MCP_SERVER_BASE_URL}${path}?${searchParams.toString()}`;

  try {
    const response = await fetch(targetUrl);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error proxying request to MCP server:', error);
    return NextResponse.json({ error: 'Failed to connect to MCP server' }, { status: 500 });
  }
}

export async function POST(request) {
  const { pathname } = new URL(request.url);
  const path = pathname.replace('/api/mcp', '');
  const targetUrl = `${MCP_SERVER_BASE_URL}${path}`;

  try {
    const body = await request.json();
    const response = await fetch(targetUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error proxying request to MCP server:', error);
    return NextResponse.json({ error: 'Failed to connect to MCP server' }, { status: 500 });
  }
}

// You can add other HTTP methods (PUT, DELETE, etc.) as needed
