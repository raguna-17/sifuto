import {
    useEffect,
    useState,
} from "react";

import Input from "../../../components/Input";
import Button from "../../../components/Button";

const IncomeForm = ({
    editingIncome,
    onSave,
    onCancel,
}) => {
    const [title, setTitle] =
        useState("");

    const [amount, setAmount] =
        useState("");

    // 編集時
    useEffect(() => {
        if (editingIncome) {
            setTitle(editingIncome.title);

            setAmount(editingIncome.amount);
        }
    }, [editingIncome]);

    // 送信
    const handleSubmit = async (e) => {
        e.preventDefault();

        const payload = {
            title,
            amount: Number(amount),
        };

        await onSave(payload);

        // 作成時だけリセット
        if (!editingIncome) {
            setTitle("");
            setAmount("");
        }
    };

    return (
        <form
            onSubmit={handleSubmit}
            style={{
                marginBottom: "24px",
                maxWidth: "400px",
            }}
        >
            <div>
                <Input
                    type="text"
                    placeholder="タイトル"
                    value={title}
                    onChange={(e) =>
                        setTitle(e.target.value)
                    }
                />
            </div>

            <div>
                <Input
                    type="number"
                    placeholder="金額"
                    value={amount}
                    onChange={(e) =>
                        setAmount(e.target.value)
                    }
                />
            </div>

            <div
                style={{
                    marginTop: "12px",
                }}
            >
                <Button type="submit">
                    {editingIncome
                        ? "更新"
                        : "追加"}
                </Button>

                {editingIncome && (
                    <Button
                        type="button"
                        onClick={onCancel}
                    >
                        キャンセル
                    </Button>
                )}
            </div>
        </form>
    );
};

export default IncomeForm;