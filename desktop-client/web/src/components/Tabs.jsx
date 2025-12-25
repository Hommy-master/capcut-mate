import React, { useState } from 'react';

function Tabs({ onTabChange, initialContent }) {
  const templates = {
    template1: {
      title: "案例一",
      content: "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=20251204214904ccb1af38"
    },
    template2: {
      title: "案例二",
      content: "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025120421372636a27729"
    }
  };

  const [activeTab, setActiveTab] = useState('');

  const handleTabClick = (templateId) => {
    setActiveTab(templateId);
    onTabChange(templates[templateId].content);
  };

  return (
    <section className="module tabs-module">
      <span><i className="fas fa-folder-open"></i> 案例草稿：</span>
      <div className="tabs">
        {Object.entries(templates).map(([key, template]) => (
          <button
            key={key}
            className={`tab-btn ${activeTab === key ? 'active' : ''}`}
            onClick={() => handleTabClick(key)}
            data-template={key}
          >
            {template.title}
          </button>
        ))}
      </div>
    </section>
  );
}

export default Tabs;
