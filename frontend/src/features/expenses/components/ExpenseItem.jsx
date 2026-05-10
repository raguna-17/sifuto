const ExpenseItem = ({
    expense,
    categories,
    onEdit,
    onDelete,
}) => {
    const category = categories.find(
        (c) => c.id === expense.category_id
    );

    return (
        <tr>
            <td>{expense.title}</td>

            <td>
                ¥
                {expense.amount.toLocaleString()}
            </td>

            <td>{category?.name || "-"}</td>

            <td>
                {new Date(
                    expense.created_at
                ).toLocaleDateString()}
            </td>

            <td>
                <button
                    onClick={() =>
                        onEdit(expense)
                    }
                >
                    編集
                </button>

                <button
                    onClick={() =>
                        onDelete(expense.id)
                    }
                >
                    削除
                </button>
            </td>
        </tr>
    );
};

export default ExpenseItem;