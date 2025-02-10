import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  webpack: (config, _) => ({
    ...config,
    watchOptions: {
      ...config.watchOptions,
      poll: 800,
      aggregateTimeout: 300,
    },
  }),
};

export default nextConfig;
