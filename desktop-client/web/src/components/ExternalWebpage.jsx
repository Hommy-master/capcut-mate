import { useEffect, useRef, useState } from "react";
// import electronService from "../services/electronService";

const externalUrl = "https://jcaigc.cn/external-features";

function ExternalWebpage() {
  const [iframeHeight, setIframeHeight] = useState(0);
  // const [isAccessible, setIsAccessible] = useState(null);
  const [themeConfig, setThemeConfig] = useState(null);
  const iframeRef = useRef(null);

  // 将主题配置同步到全局 CSS 变量
  useEffect(() => {
    if (themeConfig && typeof themeConfig === "object") {
      Object.entries(themeConfig).forEach(([key, value]) => {
        document.documentElement.style.setProperty(key, value);
      });
    }
  }, [themeConfig]);

  // const checkAccessibility = async () => {
  //   try {
  //     // 使用Electron提供的API来检测URL是否可访问（绕过CORS限制）
  //     const result = await electronService.checkUrlAccess(externalUrl);
  //     setIsAccessible(result.accessible);
  //   } catch (error) {
  //     // 请求失败，表示不可访问
  //     setIsAccessible(false);
  //     console.error("无法访问外部网页:", error);
  //   }
  // };

  // useEffect(() => {
  //   checkAccessibility();
  // }, []);

  // 监听子页面发来的配置消息
  useEffect(() => {
    const handleMessage = (event) => {
      // 安全校验：只接受来自指定域名的消息
      if (event.origin !== new URL(externalUrl).origin) return;

      if (event.data?.type === "config" && event.data?.payload) {
        const { height, themeConfig: config } = event.data.payload;

        const parsedHeight = +height;
        if (parsedHeight && typeof parsedHeight === "number") {
          setIframeHeight(parsedHeight);
        }
        if (config && typeof config === "object") {
          setThemeConfig(config);
        }
      }
    };

    window.addEventListener("message", handleMessage);
    return () => window.removeEventListener("message", handleMessage);
  }, []);

  // iframe 加载完成后，通知子页面父页面已就绪
  const handleIframeLoad = () => {
    if (iframeRef.current?.contentWindow) {
      iframeRef.current.contentWindow.postMessage(
        { type: "parentReady" },
        new URL(externalUrl).origin,
      );
    }
  };

  return (
    <section className="module">
      <div className="external-webpage-container">
        <iframe
          ref={iframeRef}
          src={externalUrl}
          title="External Webpage"
          className="external-webpage"
          width="100%"
          height={iframeHeight + "px"}
          allowFullScreen
          sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
          onLoad={handleIframeLoad}
        />
      </div>
    </section>
  );
}

export default ExternalWebpage;
