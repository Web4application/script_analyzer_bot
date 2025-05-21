const CorsHeaders = [
  { key: "Access-Control-Allow-Origin", value: "*" }, // Ideally restrict to your frontend domain
  { key: "Access-Control-Allow-Headers", value: "Authorization, Content-Type" },
  { key: "Access-Control-Allow-Methods", value: "GET,POST,OPTIONS" },
  { key: "Access-Control-Max-Age", value: "86400" },
];

const nextConfig = {
  // Add headers only if not exporting (e.g., in dev or server mode)
  async headers() {
    return [
      {
        source: "/api/:path*",
        headers: CorsHeaders,
      },
    ];
  },

  async rewrites() {
    return [
      {
        source: "/api/proxy/:path*",
        destination: "/api/proxy/:path*",
      },
      {
        source: "/google-fonts/:path*",
        destination: "https://fonts.googleapis.com/:path*",
      },
      {
        source: "/sharegpt",
        destination: "https://sharegpt.com/api/conversations",
      },
    ];
  },
};

export default nextConfig;
