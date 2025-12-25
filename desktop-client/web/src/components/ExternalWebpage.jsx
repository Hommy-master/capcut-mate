import { useEffect, useState } from "react";
import electronService from "../services/electronService";

const externalUrl = "https://jcaigc.cn/external-features";

function ExternalWebpage() {
  const [iframeHeight, setIframeHeight] = useState("240px");
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
        ) : (
          // 不可访问时显示的默认静态广告
          <div className="default-advertisement">
            <div className="ad-content">
              <h2>欢迎使用剪映草稿下载工具</h2>
              <p>我们的工具可以帮助您轻松下载剪映草稿，提高工作效率。</p>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}

export default ExternalWebpage;
