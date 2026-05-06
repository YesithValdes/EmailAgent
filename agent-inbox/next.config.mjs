/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/langgraph/:path*',
        destination: 'http://127.0.0.1:2024/:path*', // Proxy hacia el servidor local de LangGraph
      },
    ];
  },
};

export default nextConfig;
