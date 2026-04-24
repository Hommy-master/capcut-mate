import { useEffect, useState } from "react";
import electronService from "../services/electronService";

const externalUrl = "https://jcaigc.cn/external-features";

function ExternalWebpage() {
  const [iframeHeight, setIframeHeight] = useState("340px");
  const [isAccessible, setIsAccessible] = useState(null);
  
  const checkAccessibility = async () => {
    try {
      // 使用Electron提供的API来检测URL是否可访问（绕过CORS限制）
      const result = await electronService.checkUrlAccess(externalUrl);
      setIsAccessible(result.accessible);
    } catch (error) {
      // 请求失败，表示不可访问
      setIsAccessible(false);
      console.error("无法访问外部网页:", error);
    }
  };

  useEffect(() => {
    checkAccessibility();
    // const handleResize = () => {
    //   // 计算合适的高度，确保网页内容完整显示
    //   const newHeight = Math.max(300, window.innerHeight - 300) + "px";
    //   setIframeHeight(newHeight);
    // };

    // // 初始设置
    // handleResize();

    // // 添加窗口大小变化监听
    // window.addEventListener("resize", handleResize);

    // return () => {
    //   window.removeEventListener("resize", handleResize);
    // };
  }, []);

  return (
    <section className="module">
      <div className="external-webpage-container">
        {isAccessible ? (
          <iframe
            src={externalUrl}
            title="External Webpage"
            className="external-webpage"
            width="100%"
            height={iframeHeight}
            frameBorder="0"
            allowFullScreen
            sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
          />
        ) : null}
      </div>
    </section>
  );
}

export default ExternalWebpage;
