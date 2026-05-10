import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Layout from "./layouts/Layout";

import LoginPage from "./features/auth/LoginPage";
import RegisterPage from "./features/auth/RegisterPage";

import Home from "./pages/Home";

import ExpensePage from "./features/expenses/ExpensePage";
import IncomePage from "./features/incomes/IncomePage";
import CategoryPage from "./features/categories/CategoryPage";

// 仮の認証チェック
const isAuthenticated = () => {
  return !!localStorage.getItem("token");
};

// 認証ガード
const PrivateRoute = ({ children }) => {
  return isAuthenticated() ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ログイン関連 */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* 認証後ページ */}
        <Route
          path="/"
          element={
            <PrivateRoute>
              <Layout />
            </PrivateRoute>
          }
        >
          {/* ホーム */}
          <Route index element={<Home />} />

          {/* 支出 */}
          <Route path="expenses" element={<ExpensePage />} />

          {/* 収入 */}
          <Route path="incomes" element={<IncomePage />} />

          {/* カテゴリ */}
          <Route path="categories" element={<CategoryPage />} />
        </Route>

        {/* 存在しないURL */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;