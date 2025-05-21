import type { NextApiRequest, NextApiResponse } from "next";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  // Only allow POST or GET for example — lock it down
  if (!["POST", "GET"].includes(req.method ?? "")) {
    res.setHeader("Allow", ["POST", "GET"]);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }

  // Extract the path after /api/proxy/
  const path = req.query.path;
  if (!path || Array.isArray(path)) {
    return res.status(400).json({ error: "Invalid path" });
  }

  try {
    const apiUrl = `https://api.openai.com/${path}`;

    // Forward the request to OpenAI API
    const openaiResponse = await fetch(apiUrl, {
      method: req.method,
      headers: {
        "Content-Type": req.headers["content-type"] ?? "application/json",
        Authorization: `Bearer ${process.env.OPENAI_API_KEY}`, // Use env var
      },
      body: req.method === "POST" ? JSON.stringify(req.body) : undefined,
    });

    // Stream response back to client
    const data = await openaiResponse.json();
    res.status(openaiResponse.status).json(data);
  } catch (error) {
    console.error("Proxy error:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
}
