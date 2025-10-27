import pytest
from fastapi.testclient import TestClient
from main import app
from src.service.create_draft import create_draft_service
from src.schemas.create_draft import CreateDraftRequest

client = TestClient(app)


def test_create_draft_service(mocker):
    """测试创建草稿的服务函数"""
    # 模拟draft_dir和pyJianYingDraft
    mock_draft_dir = "test/draft/dir"
    mock_draft_folder = mocker.patch("pyJianYingDraft.DraftFolder")
    mock_script = mocker.Mock()
    mock_draft_folder.return_value.create_draft.return_value = mock_script

    # 调用服务函数
    draft_id = create_draft_service(
        draft_dir=mock_draft_dir,
        width=1920,
        height=1080
    )

    # 验证调用
    mock_draft_folder.assert_called_once_with(mock_draft_dir)
    mock_draft_folder.return_value.create_draft.assert_called_once()
    mock_script.save.assert_called_once()
    assert draft_id is not None


def test_create_draft_api():
    """测试创建草稿的API接口"""
    response = client.post("/openapi/v1/create_draft", json={"height": 1080, "width": 1920})
    assert response.status_code == 200
    assert "message" in response.json()
    assert "draft_id" in response.json()
    assert response.json()["message"] == "草稿创建成功"


if __name__ == "__main__":
    pytest.main(["-v", "test_draft_service.py"])