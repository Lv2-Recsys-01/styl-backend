import React, { useState } from "react";
import Modal from "react-modal";
import "./login.css";
import { NavLink } from "react-router-dom";

Modal.setAppElement("#root");

function GoToLoginLessNav() {
    return (
        <p>
            <NavLink to="/journey">로그인 없이 사용</NavLink>
        </p>
    );
}

function Login({ closeModal = () => {} }) {
    const [id, setId] = useState("");
    const [password, setPassword] = useState("");
    const [modalMode, setModalMode] = useState("login");
    const [confirm, setConfirm] = useState("");
    const [error, setError] = useState(false);
    const [title, setTitle] = useState("Login");

    const handleIdChange = (e) => {
        const value = e.target.value;
        setId(value);
    };

    const handlePasswordChange = (e) => {
        const value = e.target.value;
        setPassword(value);
    };

    const handleConfirmChange = (e) => {
        const value = e.target.value;
        setConfirm(value);
    };

    const handleToggleModalModeButton = (e) => {
        e.preventDefault();
        if (modalMode === "login") {
            setModalMode("signup");
            setTitle("Sign Up");
        } else {
            setModalMode("login");
            setTitle("Login");
        }
        clearInput(true);
    };

    const clearInput = (shouldClearId = false) => {
        if (shouldClearId) {
            setId("");
        }
        setPassword("");
        setConfirm("");
        setError("");
    };

    const checkLoginIneligibility = id.length < 4 || password.length !== 4;
    const checkSignupIneligibility =
        id.length < 4 || password.length !== 4 || confirm.length !== 4 || password !== confirm;
    const isSignUpMode = modalMode === "signup";
    const isLogInMode = modalMode === "login";

    const handleLogin = () => {
        console.log(`login => ID: ${id}, Password: ${password}`);

        if (checkLoginIneligibility) {
            clearInput();
            setError("로그인에 실패했어요");
        }
    };

    const handleSignup = () => {
        console.log(`signup => ID: ${id}, Password: ${password}`);

        if (checkSignupIneligibility) {
            clearInput();
            setError("회원가입에 실패했어요");
        }
    };

    return (
        <Modal
            isOpen={true}
            onRequestClose={closeModal}
            shouldCloseOnOverlayClick={false}
            className="modal"
            overlayClassName="modal-overlay"
        >
            <div className="background">
                <h2 className="title">{title}</h2>
                <div className="box">
                    <p className="guide">ID</p>
                    <input
                        className="user_info"
                        type="text"
                        placeholder="ID"
                        value={id}
                        onChange={handleIdChange}
                        maxLength={20}
                    />
                </div>
                <div className="box">
                    <p className="guide">Password (4자리 숫자)</p>
                    <input
                        className="user_info"
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={handlePasswordChange}
                        maxLength={4}
                    />
                </div>
                {isSignUpMode && (
                    <div className="box">
                        <p className="guide">Confirm Password</p>
                        <input
                            className="user_info"
                            type="password"
                            placeholder="Confirm Password"
                            value={confirm}
                            onChange={handleConfirmChange}
                            maxLength={4}
                        />
                    </div>
                )}

                {/* 로그인, 회원가입 제출 */}
                {isLogInMode && (
                    <div className="box">
                        <button
                            onClick={handleLogin}
                            className={`login-button ${checkLoginIneligibility ? "disabled" : ""}`}
                        >
                            로그인
                        </button>
                    </div>
                )}
                {isSignUpMode && (
                    <div className="box">
                        <button
                            onClick={handleSignup}
                            className={`signup-button ${checkSignupIneligibility ? "disabled" : ""}`}
                        >
                            회원가입
                        </button>
                    </div>
                )}

                {/* 에러 섹션 */}
                {error && <p className="error">{error}</p>}

                {/* modal Mode 전환 */}
                <div className="option">
                    <p onClick={handleToggleModalModeButton}>{isLogInMode ? "10초만에 회원가입" : "로그인"}</p>
                    <GoToLoginLessNav />
                </div>
            </div>
        </Modal>
    );
}

export default Login;
