const ExpenseTotal = ({ total }) => {
    return (
        <h2>
            合計:
            {" "}
            ¥{total.toLocaleString()}
        </h2>
    );
};

export default ExpenseTotal;