import {
    useEffect,
    useMemo,
    useState,
} from "react";

import {
    getIncomes,
    createIncome,
    updateIncome,
    deleteIncome,
} from "./api";

import IncomeForm from "./components/IncomeForm";
import IncomeList from "./components/IncomeList";
import IncomeTotal from "./components/IncomeTotal";

import Spinner from "../../components/Spinner";

const IncomePage = () => {
    const [incomes, setIncomes] =
        useState([]);

    const [editingIncome, setEditingIncome] =
        useState(null);

    const [loading, setLoading] =
        useState(false);

    const [error, setError] =
        useState("");

    // 一覧取得
    const fetchIncomes = async () => {
        try {
            setLoading(true);

            const data = await getIncomes();

            setIncomes(data);

        } catch (err) {
            setError(err.message);

        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchIncomes();
    }, []);

    // 合計
    const total = useMemo(() => {
        return incomes.reduce(
            (sum, item) =>
                sum + item.amount,
            0
        );
    }, [incomes]);

    // 保存
    const handleSave = async (payload) => {
        try {
            // 更新
            if (editingIncome) {
                const updated =
                    await updateIncome(
                        editingIncome.id,
                        payload
                    );

                setIncomes((prev) =>
                    prev.map((item) =>
                        item.id === updated.id
                            ? updated
                            : item
                    )
                );

                setEditingIncome(null);

            } else {
                // 作成
                const created =
                    await createIncome(payload);

                setIncomes((prev) => [
                    created,
                    ...prev,
                ]);
            }

        } catch (err) {
            setError(err.message);
        }
    };

    // 編集
    const handleEdit = (income) => {
        setEditingIncome(income);
    };

    // 削除
    const handleDelete = async (id) => {
        const ok = window.confirm(
            "削除しますか？"
        );

        if (!ok) return;

        try {
            await deleteIncome(id);

            setIncomes((prev) =>
                prev.filter(
                    (item) => item.id !== id
                )
            );

        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div style={{ padding: "24px" }}>
            <h1>収入管理</h1>

            {error && (
                <p style={{ color: "red" }}>
                    {error}
                </p>
            )}

            <IncomeTotal total={total} />

            <IncomeForm
                editingIncome={editingIncome}
                onSave={handleSave}
                onCancel={() =>
                    setEditingIncome(null)
                }
            />

            {loading ? (
                <Spinner />
            ) : (
                <IncomeList
                    incomes={incomes}
                    onEdit={handleEdit}
                    onDelete={handleDelete}
                />
            )}
        </div>
    );
};

export default IncomePage;