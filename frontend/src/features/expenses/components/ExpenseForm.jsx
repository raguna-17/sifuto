import { useEffect, useState } from "react";

const ExpenseForm = ({
    categories,
    editingExpense,
    onSave,
    onCancel,
}) => {
    const [title, setTitle] = useState("");
    const [amount, setAmount] =
        useState("");

    const [categoryId, setCategoryId] =
        useState("");

    useEffect(() => {
        if (editingExpense) {
            setTitle(editingExpense.title);

            setAmount(editingExpense.amount);

            setCategoryId(
                editingExpense.category_id || ""
            );
        }
    }, [editingExpense]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const payload = {
            title,
            amount: Number(amount),
            category_id: categoryId
                ? Number(categoryId)
                : null,
        };

        await onSave(payload);

        setTitle("");
        setAmount("");
        setCategoryId("");
    };

    return (
        <form
            onSubmit={handleSubmit}
            style={{
                marginBottom: "24px",
            }}
        >
            <div>
                <input
                    type="text"
                    placeholder="タイトル"
                    value={title}
                    onChange={(e) =>
                        setTitle(e.target.value)
                    }
                />
            </div>

            <div>
                <input
                    type="number"
                    placeholder="金額"
                    value={amount}
                    onChange={(e) =>
                        setAmount(e.target.value)
                    }
                />
            </div>

            <div>
                <select
                    value={categoryId}
                    onChange={(e) =>
                        setCategoryId(
                            e.target.value
                        )
                    }
                >
                    <option value="">
                        カテゴリなし
                    </option>

                    {categories.map((cat) => (
                        <option
                            key={cat.id}
                            value={cat.id}
                        >
                            {cat.name}
                        </option>
                    ))}
                </select>
            </div>

            <button type="submit">
                {editingExpense
                    ? "更新"
                    : "追加"}
            </button>

            {editingExpense && (
                <button
                    type="button"
                    onClick={onCancel}
                >
                    キャンセル
                </button>
            )}
        </form>
    );
};

export default ExpenseForm;