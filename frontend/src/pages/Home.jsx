import { Link } from "react-router-dom";

const styles = {
    container: {
        padding: "20px",
        textAlign: "center",
    },
    title: {
        fontSize: "28px",
        marginBottom: "10px",
    },
    description: {
        color: "#555",
        marginBottom: "20px",
    },
    cardContainer: {
        display: "flex",
        gap: "15px",
        justifyContent: "center",
        flexWrap: "wrap",
    },
    card: {
        display: "block",
        padding: "15px",
        width: "200px",
        textDecoration: "none",
        border: "1px solid #ddd",
        borderRadius: "8px",
        color: "#333",
    },
};

const Home = () => {
    return (
        <div style={styles.container}>
            <h1 style={styles.title}>家計簿ダッシュボード</h1>

            <p style={styles.description}>
                支出・収入・カテゴリを管理できます。
            </p>

            <div style={styles.cardContainer}>
                <Link to="/expenses" style={styles.card}>
                    <h2>支出管理</h2>
                    <p>支出の登録・一覧表示</p>
                </Link>

                <Link to="/incomes" style={styles.card}>
                    <h2>収入管理</h2>
                    <p>収入の登録・一覧表示</p>
                </Link>

                <Link to="/categories" style={styles.card}>
                    <h2>カテゴリ管理</h2>
                    <p>カテゴリの追加・編集</p>
                </Link>
            </div>
        </div>
    );
};

export default Home;