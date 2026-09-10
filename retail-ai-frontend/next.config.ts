import type { NextConfig } from "next";

// next.config.ts is loaded as an ES module by Next.js — `module.exports =`
// is CommonJS syntax and can behave inconsistently here (works in some
// setups, silently ignored in others). `export default` is the form Next's
// own TypeScript template uses and is guaranteed to be picked up correctly.
const nextConfig: NextConfig = {
  allowedDevOrigins: ["10.81.129.27", "http://10.81.129.27:3000"],
};

export default nextConfig;