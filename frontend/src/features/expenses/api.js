import api from "../../api/axios";

// 一覧取得
export const getExpenses = async () => {
    try {
        const res = await api.get("/expenses");

        return res.data;

    } catch (err) {
        throw new Error("支出取得失敗");
    }
};

// 作成
export const createExpense = async (data) => {
    try {
        const res = await api.post(
            "/expenses",
            data
        );

        return res.data;

    } catch (err) {
        throw new Error(
            err.response?.data?.detail ||
            "支出作成失敗"
        );
    }
};

// 更新
export const updateExpense = async (
    id,
    data
) => {
    try {
        const res = await api.put(
            `/expenses/${id}`,
            data
        );

        return res.data;

    } catch (err) {
        throw new Error(
            err.response?.data?.detail ||
            "支出更新失敗"
        );
    }
};

// 削除
export const deleteExpense = async (id) => {
    try {
        await api.delete(`/expenses/${id}`);

    } catch (err) {
        throw new Error("支出削除失敗");
    }
};