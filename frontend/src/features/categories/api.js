import api from "../../api/axios";

// 一覧取得
export const getCategories = async () => {
    try {
        const res = await api.get("/categories");

        return res.data;

    } catch (err) {
        throw new Error("カテゴリ取得失敗");
    }
};

// 作成
export const createCategory = async (name) => {
    try {
        const res = await api.post("/categories", {
            name,
        });

        return res.data;

    } catch (err) {
        throw new Error(
            err.response?.data?.detail ||
            "カテゴリ作成失敗"
        );
    }
};

// 削除
export const deleteCategory = async (id) => {
    try {
        const res = await api.delete(
            `/categories/${id}`
        );

        return res.data;

    } catch (err) {
        throw new Error("カテゴリ削除失敗");
    }
};