import ExpenseItem from "./ExpenseItem";

const ExpenseList = ({
    expenses,
    categories,
    onEdit,
    onDelete,
}) => {
    return (
        <table border="1" cellPadding="8">
            <thead>
                <tr>
                    <th>タイトル</th>
                    <th>金額</th>
                    <th>カテゴリ</th>
                    <th>日付</th>
                    <th>操作</th>
                </tr>
            </thead>

            <tbody>
                {expenses.map((expense) => (
                    <ExpenseItem
                        key={expense.id}
                        expense={expense}
                        categories={categories}
                        onEdit={onEdit}
                        onDelete={onDelete}
                    />
                ))}
            </tbody>
        </table>
    );
};

export default ExpenseList;