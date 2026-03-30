import pytest

BASE_URL = "/api/v1/companies"


# =========================
# 正常系
# =========================

@pytest.mark.asyncio
async def test_get_companies(client, auth_headers, test_company):
    res = await client.get(BASE_URL + "/", headers=auth_headers)

    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["name"] == "Test Company"


@pytest.mark.asyncio
async def test_get_company_detail(client, auth_headers, test_company):
    res = await client.get(f"{BASE_URL}/{test_company.id}", headers=auth_headers)

    assert res.status_code == 200
    data = res.json()
    assert data["id"] == test_company.id
    assert data["name"] == "Test Company"


@pytest.mark.asyncio
async def test_create_company(client, auth_headers):
    payload = {
        "name": "New Company",
        "industry": "Finance"
    }

    res = await client.post(BASE_URL + "/", json=payload, headers=auth_headers)

    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "New Company"
    assert data["industry"] == "Finance"


@pytest.mark.asyncio
async def test_delete_company(client, auth_headers, test_company):
    res = await client.delete(f"{BASE_URL}/{test_company.id}", headers=auth_headers)
    assert res.status_code == 204

    # 削除確認
    res = await client.get(f"{BASE_URL}/{test_company.id}", headers=auth_headers)
    assert res.status_code == 404


# =========================
# 異常系
# =========================

# 認証なし
@pytest.mark.asyncio
async def test_get_companies_unauthorized(client):
    res = await client.get(BASE_URL + "/")
    assert res.status_code == 401


# 存在しないID
@pytest.mark.asyncio
async def test_get_company_not_found(client, auth_headers):
    res = await client.get(f"{BASE_URL}/999999", headers=auth_headers)
    assert res.status_code == 404


# 不正なID（型エラー）
@pytest.mark.asyncio
async def test_get_company_invalid_id(client, auth_headers):
    res = await client.get(f"{BASE_URL}/invalid", headers=auth_headers)
    assert res.status_code == 422


# 作成：バリデーションエラー（空文字）
@pytest.mark.asyncio
async def test_create_company_invalid_payload(client, auth_headers):
    payload = {
        "name": "",
        "industry": "Finance"
    }

    res = await client.post(BASE_URL + "/", json=payload, headers=auth_headers)
    assert res.status_code == 422


# 作成：必須フィールド欠損
@pytest.mark.asyncio
async def test_create_company_missing_field(client, auth_headers):
    payload = {
        "industry": "Finance"
    }

    res = await client.post(BASE_URL + "/", json=payload, headers=auth_headers)
    assert res.status_code == 422


# 削除：存在しないID
@pytest.mark.asyncio
async def test_delete_company_not_found(client, auth_headers):
    res = await client.delete(f"{BASE_URL}/999999", headers=auth_headers)
    assert res.status_code == 404


# 認証なしで作成
@pytest.mark.asyncio
async def test_create_company_unauthorized(client):
    payload = {
        "name": "Unauthorized Company",
        "industry": "IT"
    }

    res = await client.post(BASE_URL + "/", json=payload)
    assert res.status_code == 401


# 認証なしで削除
@pytest.mark.asyncio
async def test_delete_company_unauthorized(client, test_company):
    res = await client.delete(f"{BASE_URL}/{test_company.id}")
    assert res.status_code == 401


# 重複データ（ユニーク制約がある場合）
@pytest.mark.asyncio
async def test_create_company_duplicate(client, auth_headers, test_company):
    payload = {
        "name": "Test Company",
        "industry": "IT"
    }

    res = await client.post(BASE_URL + "/", json=payload, headers=auth_headers)

    # DB設計によって変わる
    assert res.status_code in (400, 409)