import dns from "node:dns";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Resolve "localhost" to 127.0.0.1 first; otherwise Vite may bind IPv6 ::1 only
// and http://127.0.0.1:3000 is refused (CRA listened on IPv4).
dns.setDefaultResultOrder("ipv4first");

// Port 3000 matches the backend's default CORS_ORIGINS; outDir matches .gitignore.
export default defineConfig({
  plugins: [react()],
  server: { port: 3000, strictPort: true },
  preview: { port: 3000, strictPort: true },
  build: { outDir: "build" },
});
