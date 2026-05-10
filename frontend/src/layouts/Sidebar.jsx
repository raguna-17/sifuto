import { Link, useLocation } from "react-router-dom";

const Sidebar = () => {
    const location = useLocation();

    const menu = [
        { name: "ホーム", path: "/" },
        { name: "支出管理", path: "/expenses" },
        { name: "収入管理", path: "/incomes" },
        { name: "カテゴリ管理", path: "/categories" },
    ];

    return (
        <div style={styles.sidebar}>
            <h2 style={styles.title}>家計簿アプリ</h2>

            <nav>
                {menu.map((item) => {
                    const isActive = location.pathname === item.path;

                    return (
                        <Link
                            key={item.path}
                            to={item.path}
                            style={{
                                ...styles.link,
                                ...(isActive ? styles.active : {}),
                            }}
                        >
                            {item.name}
                        </Link>
                    );
                })}
            </nav>
        </div>
    );
};

const styles = {
    sidebar: {
        width: "220px",
        height: "100vh",
        background: "#1e293b",
        color: "#fff",
        padding: "20px",
        boxSizing: "border-box",
    },
    title: {
        marginBottom: "24px",
        fontSize: "22px",
        fontWeight: "bold",
    },
    link: {
        display: "block",
        padding: "12px",
        color: "#cbd5e1",
        textDecoration: "none",
        borderRadius: "8px",
        marginBottom: "10px",
        transition: "0.2s",
    },
    active: {
        background: "#3b82f6",
        color: "#fff",
        fontWeight: "bold",
    },
};

export default Sidebar;