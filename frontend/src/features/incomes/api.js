import api from "../../api/axios";

// 一覧取得
export const getIncomes = async () => {
    try {
        const res = await api.get("/incomes");

        return res.data;

    } catch (err) {
        throw new Error("収入取得失敗");
    }
};

// 作成
export const createIncome = async (data) => {
    try {
        const res = await api.post(
            "/incomes",
            data
        );

        return res.data;

    } catch (err) {
        throw new Error(
            err.response?.data?.detail ||
            "収入作成失敗"
        );
    }
};

// 更新
export const updateIncome = async (
    id,
    data
) => {
    try {
        const res = await api.put(
            `/incomes/${id}`,
            data
        );

        return res.data;

    } catch (err) {
        throw new Error(
            err.response?.data?.detail ||
            "収入更新失敗"
        );
    }
};

// 削除
export const deleteIncome = async (id) => {
    try {
        await api.delete(`/incomes/${id}`);

    } catch (err) {
        throw new Error("収入削除失敗");
    }
};