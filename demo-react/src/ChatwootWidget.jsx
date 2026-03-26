import { useEffect } from "react";

/**
 * Laddar Chatwoots website-widget när VITE_CHATWOOT_BASE_URL och VITE_CHATWOOT_WEBSITE_TOKEN är satta.
 * Bas-URL måste vara nåbar från användarens webbläsare (t.ex. http://localhost:3001), inte Docker-interna värdnamn.
 */
export default function ChatwootWidget() {
  useEffect(() => {
    const rawBase = import.meta.env.VITE_CHATWOOT_BASE_URL;
    const websiteToken = import.meta.env.VITE_CHATWOOT_WEBSITE_TOKEN;
    if (!rawBase || !websiteToken) return;

    const baseUrl = String(rawBase).replace(/\/$/, "");
    if (document.querySelector("script[data-demo-chatwoot-sdk]")) return;

    const script = document.createElement("script");
    script.dataset.demoChatwootSdk = "true";
    script.src = `${baseUrl}/packs/js/sdk.js`;
    script.async = true;
    script.defer = true;
    script.onload = () => {
      window.chatwootSDK?.run({
        websiteToken,
        baseUrl,
      });
    };
    document.body.appendChild(script);
  }, []);

  return null;
}
