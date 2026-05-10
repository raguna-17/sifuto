const IncomeItem = ({
    income,
    onEdit,
    onDelete,
}) => {
    return (
        <tr>
            <td>{income.title}</td>

            <td>
                ¥
                {income.amount.toLocaleString()}
            </td>

            <td>
                {new Date(
                    income.created_at
                ).toLocaleDateString()}
            </td>

            <td>
                <button
                    onClick={() =>
                        onEdit(income)
                    }
                >
                    編集
                </button>

                <button
                    onClick={() =>
                        onDelete(income.id)
                    }
                    style={{
                        marginLeft: "8px",
                    }}
                >
                    削除
                </button>
            </td>
        </tr>
    );
};

export default IncomeItem;