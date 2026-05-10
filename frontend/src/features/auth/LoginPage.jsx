import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

import { login, getMe } from "./api";

const LoginPage = () => {
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const validate = () => {
        if (!email || !password) {
            return "全て入力してください";
        }

        if (!email.includes("@")) {
            return "メール形式が正しくありません";
        }

        if (password.length < 4) {
            return "パスワードは4文字以上です";
        }

        return "";
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        setError("");

        const errMsg = validate();

        if (errMsg) {
            setError(errMsg);
            return;
        }

        try {
            setLoading(true);

            const data = await login(email, password);

            localStorage.setItem(
                "token",
                data.access_token
            );

            if (data.refresh_token) {
                localStorage.setItem(
                    "refresh",
                    data.refresh_token
                );
            }

            const me = await getMe();

            console.log("ログインユーザー:", me);

            navigate("/");

        } catch (err) {
            setError(err.message);

        } finally {
            setLoading(false);
        }
    };

    return (
        <div
            style={{
                maxWidth: "400px",
                margin: "80px auto",
            }}
        >
            <h1>ログイン</h1>

            {error && (
                <p style={{ color: "red" }}>
                    {error}
                </p>
            )}

            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: "12px" }}>
                    <input
                        type="email"
                        placeholder="メールアドレス"
                        value={email}
                        onChange={(e) =>
                            setEmail(e.target.value)
                        }
                        style={{
                            width: "100%",
                            padding: "10px",
                        }}
                    />
                </div>

                <div style={{ marginBottom: "12px" }}>
                    <input
                        type="password"
                        placeholder="パスワード"
                        value={password}
                        onChange={(e) =>
                            setPassword(e.target.value)
                        }
                        style={{
                            width: "100%",
                            padding: "10px",
                        }}
                    />
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    style={{
                        width: "100%",
                        padding: "10px",
                    }}
                >
                    {loading ? "ログイン中..." : "ログイン"}
                </button>
            </form>

            <p style={{ marginTop: "16px" }}>
                アカウントがない？
                {" "}
                <Link to="/register">
                    新規登録はこちら
                </Link>
            </p>
        </div>
    );
};

export default LoginPage;