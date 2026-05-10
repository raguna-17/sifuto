import { useEffect, useMemo, useState } from "react";

import {
    getExpenses,
    createExpense,
    updateExpense,
    deleteExpense,
} from "./api";

import { getCategories } from "../categories/api";

import ExpenseForm from "./components/ExpenseForm";
import ExpenseList from "./components/ExpenseList";
import ExpenseTotal from "./components/ExpenseTotal";

const ExpensePage = () => {
    const [expenses, setExpenses] =
        useState([]);

    const [categories, setCategories] =
        useState([]);

    const [editingExpense, setEditingExpense] =
        useState(null);

    const [loading, setLoading] =
        useState(false);

    const [error, setError] = useState("");

    // データ取得
    const fetchData = async () => {
        try {
            setLoading(true);

            const [
                expensesData,
                categoriesData,
            ] = await Promise.all([
                getExpenses(),
                getCategories(),
            ]);

            setExpenses(expensesData);
            setCategories(categoriesData);

        } catch (err) {
            setError(err.message);

        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    // 合計
    const total = useMemo(() => {
        return expenses.reduce(
            (sum, item) => sum + item.amount,
            0
        );
    }, [expenses]);

    // 保存
    const handleSave = async (payload) => {
        try {
            if (editingExpense) {
                const updated =
                    await updateExpense(
                        editingExpense.id,
                        payload
                    );

                setExpenses((prev) =>
                    prev.map((item) =>
                        item.id === updated.id
                            ? updated
                            : item
                    )
                );

                setEditingExpense(null);

            } else {
                const created =
                    await createExpense(payload);

                setExpenses((prev) => [
                    created,
                    ...prev,
                ]);
            }

        } catch (err) {
            setError(err.message);
        }
    };

    // 編集
    const handleEdit = (expense) => {
        setEditingExpense(expense);
    };

    // 削除
    const handleDelete = async (id) => {
        const ok = window.confirm(
            "削除しますか？"
        );

        if (!ok) return;

        try {
            await deleteExpense(id);

            setExpenses((prev) =>
                prev.filter((e) => e.id !== id)
            );

        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div style={{ padding: "24px" }}>
            <h1>支出管理</h1>

            {error && (
                <p style={{ color: "red" }}>
                    {error}
                </p>
            )}

            <ExpenseTotal total={total} />

            <ExpenseForm
                categories={categories}
                editingExpense={editingExpense}
                onSave={handleSave}
                onCancel={() =>
                    setEditingExpense(null)
                }
            />

            {loading ? (
                <p>読み込み中...</p>
            ) : (
                <ExpenseList
                    expenses={expenses}
                    categories={categories}
                    onEdit={handleEdit}
                    onDelete={handleDelete}
                />
            )}
        </div>
    );
};

export default ExpensePage;