import electronService from "@/services/electronService";
import { PROJECT_LINKS } from "@/utils/const";

import "./index.less";

function FooterLink({ href, children }) {
  const handleClick = (event) => {
    event.preventDefault();
    electronService.openExternalUrl(href);
  };

  return (
    <a
      className="app-footer-link"
      href={href}
      title={href}
      onClick={handleClick}
    >
      {children}
    </a>
  );
}

function Footer({ appVersion }) {
  return (
    <footer className="app-footer">
      <div className="app-footer-inner">
        <FooterLink href={PROJECT_LINKS.discussions}>论坛求助</FooterLink>
        <span className="app-footer-sep">|</span>
        <FooterLink href={PROJECT_LINKS.docs}>使用手册</FooterLink>
        <span className="app-footer-sep">|</span>
        <FooterLink href={PROJECT_LINKS.github}>GitHub</FooterLink>
        <span className="app-footer-sep">|</span>
        <FooterLink href={PROJECT_LINKS.gitee}>Gitee</FooterLink>
        <span className="app-footer-sep">|</span>
        <span className="app-footer-version">
          当前版本：{appVersion ? `v${appVersion}` : "v-"}
        </span>
      </div>
    </footer>
  );
}

export default Footer;
