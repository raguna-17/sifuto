import IncomeItem from "./IncomeItem";

const IncomeList = ({
    incomes,
    onEdit,
    onDelete,
}) => {
    return (
        <table border="1" cellPadding="8">
            <thead>
                <tr>
                    <th>タイトル</th>
                    <th>金額</th>
                    <th>作成日</th>
                    <th>操作</th>
                </tr>
            </thead>

            <tbody>
                {incomes.map((income) => (
                    <IncomeItem
                        key={income.id}
                        income={income}
                        onEdit={onEdit}
                        onDelete={onDelete}
                    />
                ))}
            </tbody>
        </table>
    );
};

export default IncomeList;