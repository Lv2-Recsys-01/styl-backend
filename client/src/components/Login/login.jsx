import React, { useState } from "react";
import Modal from "react-modal";
import "./login.css";
import { NavLink, useNavigate } from "react-router-dom";
import { notification } from "antd";
import { styleAxios } from "../../utils";

Modal.setAppElement("#root");

function GoToLoginLessNav() {
    return (
        <div className='guest'>
            <NavLink to="/journey">로그인 없이 사용</NavLink>
        </div>
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

    const handleSignupSuccess = () => {
        notification.success({
            message: "회원가입에 성공했어요!",
            description: "로그인 해주세요!",
            duration: 2,
        });
    };

    const checkLoginIneligibility = id.length < 4 || password.length < 4;
    const checkSignupIneligibility = id.length < 4 || password.length < 4 || confirm.length < 4 || password !== confirm;
    const isSignUpMode = modalMode === "signup";
    const isLogInMode = modalMode === "login";

    const navigate = useNavigate();

    const handleLogin = () => {

        const LoginParams = {
            user_name: id,
            user_pwd: password,
        };

        styleAxios
            .post("/users/login", LoginParams)
            .then((response) => {
                console.log(response.data);
                navigate("/journey");
            })
            .catch((error) => {
                console.error(error);
                clearInput();
                const {
                    response: {
                        data: { detail },
                    },
                } = error;

                setError(`로그인에 실패했어요. ${detail ?? ""}`);
            });

        if (checkLoginIneligibility) {
            clearInput();
            setError("로그인에 실패했어요");
        }
    };

    const handleSignup = () => {
        console.log(`signup => ID: ${id}, Password: ${password}, ConfirmPassword: ${confirm}`);

        const SignUpParams = {
            user_name: id,
            user_pwd: password,
            confirm_pwd: confirm,
        };

        styleAxios
            .post("/users/signup", SignUpParams)
            .then((response) => {
                console.log(response.data);
                handleSignupSuccess();
                setModalMode("login");
                setTitle("Login");
                clearInput();
                navigate("/");
            })
            .catch((error) => {
                console.error(error);
                clearInput();
                const {
                    response: {
                        data: { detail },
                    },
                } = error;

                setError(`회원가입에 실패했어요! ${detail ?? ""}`);
            });

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
                        maxLength={12}
                    />
                </div>
                <div className="box">
                    <p className="guide">Password</p>
                    <input
                        className="user_info"
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={handlePasswordChange}
                        maxLength={20}
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
                            maxLength={20}
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
