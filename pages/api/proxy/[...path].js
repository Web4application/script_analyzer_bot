// pages/api/proxy/[...path].js

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const AUTH_TOKEN = process.env.API_AUTH_TOKEN;

export default async function handler(req, res) {
  const authHeader = req.headers.authorization || "";
  if (!authHeader.startsWith("Bearer ") || authHeader.slice(7) !== AUTH_TOKEN) {
    return res.status(401).json({ error: "Unauthorized" });
  }

  const { path } = req.query;
  const targetBase = "https://api.openai.com";

  try {
    const cleanQuery = new URLSearchParams(req.query);
    cleanQuery.delete("path");

    const urlPath = Array.isArray(path) ? path.join("/") : path;
    const targetUrl = `${targetBase}/${urlPath}${cleanQuery.toString() ? "?" + cleanQuery.toString() : ""}`;

    const headers = {
      ...req.headers,
      host: new URL(targetBase).host,
      authorization: `Bearer ${OPENAI_API_KEY}`,
    };
    delete headers.cookie;

    const fetchOptions = {
      method: req.method,
      headers,
      body: ["GET", "HEAD"].includes(req.method) ? undefined : JSON.stringify(req.body),
    };

    if (fetchOptions.body) {
      fetchOptions.headers["Content-Type"] = "application/json";
    }

    const response = await fetch(targetUrl, fetchOptions);

    res.status(response.status);
    response.headers.forEach((value, key) => res.setHeader(key, value));

    const data = await response.arrayBuffer();
    res.send(Buffer.from(data));
  } catch (error) {
    console.error("Proxy error:", error);
    res.status(500).json({ error: "Proxy error" });
  }
}
