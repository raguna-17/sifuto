import { useEffect, useState } from "react";

import {
    getCategories,
    createCategory,
    deleteCategory,
} from "./api";

const CategoryPage = () => {
    const [categories, setCategories] =
        useState([]);

    const [name, setName] = useState("");

    const [loading, setLoading] =
        useState(false);

    const [error, setError] = useState("");

    // 一覧取得
    const fetchCategories = async () => {
        try {
            setLoading(true);

            const data = await getCategories();

            setCategories(data);

        } catch (err) {
            setError(err.message);

        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchCategories();
    }, []);

    // 作成
    const handleCreate = async (e) => {
        e.preventDefault();

        setError("");

        if (!name.trim()) {
            setError("カテゴリ名を入力してください");
            return;
        }

        try {
            const newCategory =
                await createCategory(name);

            setCategories((prev) => [
                ...prev,
                newCategory,
            ]);

            setName("");

        } catch (err) {
            setError(err.message);
        }
    };

    // 削除
    const handleDelete = async (id) => {
        const ok = window.confirm(
            "削除しますか？"
        );

        if (!ok) return;

        try {
            await deleteCategory(id);

            setCategories((prev) =>
                prev.filter((c) => c.id !== id)
            );

        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div style={{ padding: "24px" }}>
            <h1>カテゴリ管理</h1>

            {error && (
                <p style={{ color: "red" }}>
                    {error}
                </p>
            )}

            {/* 作成フォーム */}
            <form
                onSubmit={handleCreate}
                style={{
                    marginBottom: "24px",
                }}
            >
                <input
                    type="text"
                    placeholder="カテゴリ名"
                    value={name}
                    onChange={(e) =>
                        setName(e.target.value)
                    }
                    style={{
                        padding: "8px",
                        marginRight: "8px",
                    }}
                />

                <button type="submit">
                    追加
                </button>
            </form>

            {/* ローディング */}
            {loading ? (
                <p>読み込み中...</p>
            ) : (
                <ul>
                    {categories.map((category) => (
                        <li
                            key={category.id}
                            style={{
                                marginBottom: "12px",
                            }}
                        >
                            {category.name}

                            <button
                                onClick={() =>
                                    handleDelete(category.id)
                                }
                                style={{
                                    marginLeft: "12px",
                                }}
                            >
                                削除
                            </button>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default CategoryPage;