import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Alinhado ao `saas_app`: permite evoluir código legado sem travar CI/build.
  // Remova quando ESLint/TS estiverem limpos no projeto.
  eslint: { ignoreDuringBuilds: true },
  typescript: { ignoreBuildErrors: true },

  async rewrites() {
    return [
      { source: "/api/viacep/:path*", destination: "https://viacep.com.br/:path*" },
      { source: "/api/receitaws/:path*", destination: "https://receitaws.com.br/:path*" },
    ];
  },
};

export default nextConfig;
