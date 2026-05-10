import api from "../../api/axios";

// ログイン
export const login = async (email, password) => {
    try {
        const res = await api.post("/users/login", {
            email,
            password,
        });

        return res.data;

    } catch (err) {
        throw new Error(
            err.response?.data?.detail || "ログイン失敗"
        );
    }
};

// 新規登録
export const register = async (email, password) => {
    try {
        const res = await api.post("/users/register", {
            email,
            password,
        });

        return res.data;

    } catch (err) {
        throw new Error(
            err.response?.data?.detail || "登録失敗"
        );
    }
};

// 現在ユーザー取得
export const getMe = async () => {
    try {
        const res = await api.get("/users/me");

        return res.data;

    } catch (err) {
        throw new Error("ユーザー取得失敗");
    }
};