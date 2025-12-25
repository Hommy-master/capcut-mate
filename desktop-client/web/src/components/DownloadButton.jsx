
function DownloadButton({ onClick, isLoading, setIsLoading, textValue }) {
  const handleClick = async () => {
    setIsLoading(true);
    try {
      await onClick();
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="module">
      <button
        className="btn btn-download"
        onClick={handleClick}
        disabled={isLoading || !textValue}
      >
        <i
          className={`fas ${isLoading ? "fa-spinner fa-spin" : "fa-download"}`}
        ></i>
        创建剪映草稿
      </button>
    </section>
  );
}

export default DownloadButton;
