/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable standalone output for Render deployment
  output: 'standalone',
  
  // React strict mode for better development experience
  reactStrictMode: true,
  
  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
  
  // Image optimization configuration
  images: {
    unoptimized: true, // Required for Render deployment
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
    ],
  },
  
  // Webpack configuration
  webpack: (config, { isServer }) => {
    // Fix for some node modules
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        net: false,
        tls: false,
      };
    }
    return config;
  },
  
  // Experimental features
  experimental: {
    serverComponentsExternalPackages: ['@prisma/client'],
  },
  
  // Headers for security
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
        ],
      },
    ];
  },
  
  // Redirects (if needed)
  async redirects() {
    return [];
  },
  
  // Rewrites (if needed for API proxying)
  async rewrites() {
    return [];
  },
}

module.exports = nextConfig
